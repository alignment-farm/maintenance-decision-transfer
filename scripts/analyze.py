"""Independent rescoring, selector fitting and complete outcome/cost ledger."""
import argparse
from collections import defaultdict
import hashlib
import json
from pathlib import Path
import time
import maintenance_task as t

ARMS=['novel','bridged']
def read(path): return [json.loads(l) for l in path.read_text().splitlines()]
def dump(path,value): path.write_text(json.dumps(value,indent=2)+'\n')
def key(c): return tuple(c[k] for k in ('entity','channel','priority','certified','stock'))
def checked(run):
    for line in (run/'SHA256SUMS').read_text().splitlines():
        h,n=line.split('  ',1)
        assert hashlib.sha256((run/n).read_bytes()).hexdigest()==h,(run,n)
    events=read(run/'events.jsonl');rows=read(run/'responses.jsonl')
    assert events[-1]['kind']=='finish' and events[-1]['status']=='complete'
    for r in rows: assert r['scores']==t.check(r['raw'],r['case'],r['version'])
    return events,rows
def groups(rows):
    g=defaultdict(list)
    for r in rows:g[r['state'],r['panel']].append(r)
    return g
def verify_decisions(run,g,design):
    """Recompute choices using only their permitted observations, never final rows."""
    def pick(values,h):
        return h if abs(values['novel']-values['bridged'])<1e-10 else max(values,key=values.get)
    for h in ARMS:
        expected=dict(constant_novel='novel',constant_bridged='bridged',match_history=h,no_revision='none')
        expected['sparse_validation']=pick({s:sum(g[h+'--'+s,'validation'][i]['scores']['complete'] for i in [0,2,4,6,9,11,13,15]) for s in ARMS},h)
        expected['full_validation']=pick({s:sum(r['scores']['complete'] for r in g[h+'--'+s,'validation']) for s in ARMS},h)
        if design['phase']=='assessment':
            predictor=json.loads((run/'predictors.json').read_text())
            expected['developed_constant']=predictor['constant']
            nearest=min(predictor['states'],key=lambda r:(abs(design['acquisition_updates']-r['duration']),r['history']!=h))
            expected['history_predictor']=pick(nearest['endpoints'],h)
            observed=[int(r['scores']['complete']) for r in g[h+'-start','pre']]
            nearest=min(predictor['states'],key=lambda r:(sum(x!=y for x,y in zip(observed,r['pre'])),r['history']!=h))
            expected['pre_observation']=pick(nearest['endpoints'],h)
            predicted={s:predictor['prefix'][s]['intercept']+predictor['prefix'][s]['slope']*sum(r['scores']['complete'] for r in g[h+'--'+s,'prefix'])/16 for s in ARMS}
            expected['prefix_predictor']=pick(predicted,h)
        assert expected==json.loads((run/(h+'-decisions.json')).read_text())
def fit(run,out):
    tick=time.monotonic();events,rows=checked(run);g=groups(rows)
    design=json.loads((run/'design.json').read_text()); assert design['phase']=='development'
    states=[]
    for h in ARMS:
        states.append(dict(history=h,duration=design['acquisition_updates'],
            pre=[int(r['scores']['complete']) for r in g[h+'-start','pre']],
            endpoints={s:sum(r['scores']['complete'] for r in g[h+'--'+s,'final'])/192 for s in ARMS}))
    constant=max(ARMS,key=lambda s:sum(r['endpoints'][s] for r in states))
    prefix={}
    for s in ARMS:
        xs=[sum(r['scores']['complete'] for r in g[h+'--'+s,'prefix'])/16 for h in ARMS]
        ys=[row['endpoints'][s] for row in states]
        xm=sum(xs)/2;ym=sum(ys)/2
        slope=sum((x-xm)*(y-ym) for x,y in zip(xs,ys))/(1+sum((x-xm)**2 for x in xs))
        prefix[s]=dict(intercept=ym-slope*xm,slope=slope,x=xs,y=ys)
    dump(out,dict(source_run=str(run),source_sha256=hashlib.sha256((run/'SHA256SUMS').read_bytes()).hexdigest(),
        constant=constant,states=states,prefix=prefix,fit_seconds=time.monotonic()-tick,
        calibration_acquisitions=1,calibration_endpoint_calls=768,calibration_prefix_calls=64))
def summarize(run):
    events,rows=checked(run);g=groups(rows);design=json.loads((run/'design.json').read_text())
    verify_decisions(run,g,design)
    result=dict(source_run=str(run),design=design,endpoints=[],decisions=[])
    for h in ARMS:
        pre={key(r['case']):r for r in g[h+'-start','final']}
        assert len(pre)==192
        totals={}
        for s in ['none']+ARMS:
            selected=list(pre.values()) if s=='none' else g[h+'--'+s,'final']
            assert len(selected)==192
            masks={
                'new':[r for r in selected if t.oracle(r['case'],1)!=t.oracle(r['case'],2)],
                'earlier':[r for r in selected if t.oracle(r['case'],0)!=t.oracle(r['case'],1)],
                'unchanged':[r for r in selected if t.oracle(r['case'],1)==t.oracle(r['case'],2)],
                'negative':[r for r in selected if not t.eligible(r['case'],2)],
                'fresh':[r for r in selected if r['case']['entity'] in design['final'][-4:]],
                'familiar':[r for r in selected if r['case']['entity'] in t.ACQUIRED+t.TARGETS]}
            total=sum(r['scores']['complete'] for r in selected);totals[s]=total
            result['endpoints'].append(dict(history=h,support=s,complete=total,n=192,
                components={k:sum(r['scores'][k] for r in selected) for k in selected[0]['scores']},
                groups={k:dict(n=len(v),complete=sum(r['scores']['complete'] for r in v)) for k,v in masks.items()},
                losses=sum(t.check(pre[key(r['case'])]['raw'],r['case'],1)['complete'] and not r['scores']['complete'] for r in masks['unchanged']),
                repairs=sum(not t.check(pre[key(r['case'])]['raw'],r['case'],1)['complete'] and r['scores']['complete'] for r in masks['unchanged']),
                start_v1_complete=sum(t.check(r['raw'],r['case'],1)['complete'] for r in pre.values())))
        decisions=json.loads((run/(h+'-decisions.json')).read_text())
        for method,s in decisions.items():
            result['decisions'].append(dict(history=h,method=method,support=s,complete=totals[s],regret=max(totals[s] for s in ARMS)-totals[s]))
    result['costs']=costs(events,rows,run)
    return result
def costs(events,rows,run):
    updates=[e for e in events if e['kind']=='update']
    return dict(updates=len(updates),training_input_tokens=sum(e['input_tokens'] for e in updates),loss_tokens=sum(e['loss_tokens'] for e in updates),
        training_seconds=sum(e['seconds'] for e in updates),generations=len(rows),prompt_tokens=sum(r['prompt_tokens'] for r in rows),
        completion_tokens=sum(r['completion_tokens'] for r in rows),generation_seconds=sum(r['seconds'] for r in rows),
        wall_seconds=events[-1]['wall_seconds'],wait_seconds=events[-1]['wait_seconds'],peak_mlx_bytes=events[-1]['peak_mlx_bytes'],
        checkpoint_bytes=sum(p.stat().st_size for p in run.glob('*.safetensors')),
        panels={panel:dict(generations=sum(r.get('panel','acquisition_characterization')==panel for r in rows),
            prompt_tokens=sum(r['prompt_tokens'] for r in rows if r.get('panel','acquisition_characterization')==panel),
            completion_tokens=sum(r['completion_tokens'] for r in rows if r.get('panel','acquisition_characterization')==panel))
            for panel in sorted(set(r.get('panel','acquisition_characterization') for r in rows))})
def deployment(run):
    events,rows=checked(run);g=groups(rows);design=json.loads((run/'design.json').read_text())
    result=[]
    for h in ARMS:
        decisions=json.loads((run/(h+'-decisions.json')).read_text())
        for method,s in decisions.items():
            selected=[];observed=[]
            if method in ('sparse_validation','full_validation'):
                selected=[e for e in events if e['kind']=='update' and e['state'] in [h+'--'+v for v in ARMS]]
                for arm in ARMS:
                    panel=g[h+'--'+arm,'validation']
                    observed+=panel if method=='full_validation' else [panel[i] for i in [0,2,4,6,9,11,13,15]]
            elif s!='none':
                selected=[e for e in events if e['kind']=='update' and e['state']==h+'--'+s]
                if method=='prefix_predictor':
                    other=next(v for v in ARMS if v!=s)
                    selected += [e for e in events if e['kind']=='update' and e['state']==h+'--'+other and e['index']<=24]
                    observed=g[h+'--novel','prefix']+g[h+'--bridged','prefix']
                elif method=='pre_observation':observed=g[h+'-start','pre']
            use=g[h+'-start' if s=='none' else h+'--'+s,'final']
            result.append(dict(history=h,method=method,support=s,revision_updates=len(selected),
                training_input_tokens=sum(e['input_tokens'] for e in selected),loss_tokens=sum(e['loss_tokens'] for e in selected),
                observed_training_seconds=sum(e['seconds'] for e in selected),observation_calls=len(observed),
                observation_prompt_tokens=sum(r['prompt_tokens'] for r in observed),observation_completion_tokens=sum(r['completion_tokens'] for r in observed),
                observed_observation_seconds=sum(r['seconds'] for r in observed),use_calls=len(use),
                use_prompt_tokens=sum(r['prompt_tokens'] for r in use),use_completion_tokens=sum(r['completion_tokens'] for r in use),
                observed_use_seconds=sum(r['seconds'] for r in use),shared_prior_acquisition_updates=design['acquisition_updates'],shared_prior_revision_updates=192,
                calibration_required=method in ('developed_constant','history_predictor','pre_observation','prefix_predictor')))
    return result
def main():
    p=argparse.ArgumentParser();p.add_argument('--fit',type=Path);p.add_argument('--runs',nargs='*',type=Path,default=[])
    p.add_argument('--acquisitions',nargs='*',type=Path,default=[]);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    assert not a.output.exists(), 'Preserve existing analysis'
    if a.fit:fit(a.fit,a.output);return
    results=[summarize(r) for r in a.runs];acquisitions=[]
    for run in a.acquisitions:
        events,rows=checked(run)
        acquisitions.append(dict(run=str(run),criteria=[e for e in events if e['kind']=='acquisition_criterion'],costs=costs(events,rows,run)))
    dump(a.output,dict(runs=results,acquisitions=acquisitions,deployment={str(run):deployment(run) for run in a.runs}))
    for r in results:
        print(r['design']['seed'],[(v['history'],v['support'],v['complete']) for v in r['endpoints']])
if __name__=='__main__':main()
