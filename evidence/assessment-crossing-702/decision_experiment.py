"""Paired maintenance candidates with prospectively separated paid panels."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import time
import mlx.core as mx
from mlx.utils import tree_flatten, tree_unflatten
from runtime import Runtime, resource, sha, digest
import maintenance_task as t

ARMS = ['novel', 'bridged']
FINAL = t.ACQUIRED + t.TARGETS + ['vornel', 'hespak', 'queldin', 'zartum']
VALID = ['torvek', 'jaspel']
SPARSE = [0, 2, 4, 6, 9, 11, 13, 15]

def choose(scores, history):
    return history if abs(scores['novel'] - scores['bridged']) < 1e-10 else max(scores, key=scores.get)

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--start-run', type=Path, required=True)
    p.add_argument('--seed', type=int, required=True)
    p.add_argument('--predictors', type=Path)
    p.add_argument('--verify-continuation', action='store_true')
    a = p.parse_args()
    out = a.output; out.mkdir(parents=True, exist_ok=False)
    start = time.monotonic(); wait = 0.; last = 0.; status = 'failed'
    for name in ['decision_experiment.py', 'runtime.py', 'maintenance_task.py']:
        (out/name).write_bytes(Path('scripts', name).read_bytes())
    (out/'protocol.md').write_bytes(Path('protocol/comparison-v1.md').read_bytes())
    predictors = json.loads(a.predictors.read_text()) if a.predictors else None
    if a.predictors: (out/'predictors.json').write_bytes(a.predictors.read_bytes())
    ev = (out/'events.jsonl').open('x'); rs = (out/'responses.jsonl').open('x')
    def save(n, d): (out/n).write_text(json.dumps(d, indent=2)+'\n')
    def emit(kind, **d):
        ev.write(json.dumps(dict(kind=kind, elapsed=time.monotonic()-start, **d))+'\n'); ev.flush()
    def guard():
        nonlocal wait, last
        if time.monotonic()-last > 5:
            while True:
                lines = subprocess.check_output(['ps', '-axo', 'pid,etime,rss,command'], text=True).splitlines()
                jobs = [l for l in lines if '/bin/python' in l and 'scripts/' in l and 'monitor.py' not in l and int(l.split()[0]) != os.getpid()]
                emit('resource_check', jobs=jobs)
                if not jobs: break
                tick=time.monotonic(); time.sleep(10); wait+=time.monotonic()-tick
                assert wait < 7200, 'shared-device wait limit'
            last=time.monotonic()
        assert time.monotonic()-start-wait < 3600, 'active-hour limit'
        assert mx.get_peak_memory() < 40e9, 'MLX memory limit'
    try:
        emit('revision', git=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(), dirty=subprocess.check_output(['git','status','--short'],text=True))
        for line in (a.start_run/'SHA256SUMS').read_text().splitlines():
            h,n=line.split('  ',1); assert sha(a.start_run/n)==h,n
        acqevents=[json.loads(l) for l in (a.start_run/'events.jsonl').read_text().splitlines()]
        ready=[e for e in acqevents if e['kind']=='acquisition_criterion' and e['passed'] and e['state'].startswith(f'seed{a.seed}-')]
        assert len(ready)==1, 'No usable acquired checkpoint; preserve and diagnose acquisition first'
        duration=int(ready[0]['state'].split('-A')[1])
        save('design.json', dict(seed=a.seed, start_run=str(a.start_run), acquisition_updates=duration, final=FINAL, validation=VALID, sparse=SPARSE, phase='assessment' if predictors else 'development'))
        guard(); save('resource.json',resource()); rt=Runtime()
        def evaluate(state, panel, entities, version):
            rows=[]
            for c in t.cases(entities):
                guard(); prefix=rt.encode(t.prompt(c)); r=rt.generate(prefix,limit=40)
                row=dict(state=state,panel=panel,version=version,case=c,prefix=prefix,scores=t.check(r['raw'],c,version),**r)
                rs.write(json.dumps(row)+'\n');rs.flush();rows.append(row)
            emit('evaluation',state=state,panel=panel,n=len(rows),complete=sum(r['scores']['complete'] for r in rows))
            print(state,panel,sum(r['scores']['complete'] for r in rows),len(rows),flush=True)
            return rows
        def checkpoint(name, opt=None):
            path=out/(name+'.safetensors'); mx.save_safetensors(str(path),dict(rt.snapshot()))
            emit('checkpoint',state=name,sha256=sha(path),state_hash=digest(rt.snapshot()),bytes=path.stat().st_size)
            if opt is not None:
                op=out/(name+'-optimizer.safetensors')
                mx.save_safetensors(str(op),dict(tree_flatten(opt.state)))
                emit('optimizer_checkpoint',state=name,sha256=sha(op),bytes=op.stat().st_size)
        def updates(name,support,opt,lo,hi):
            schedule=t.schedule(support,2,64,'negative')
            for idx in range(lo,hi):
                guard();source,c=schedule[idx];prefix=rt.encode(t.prompt(c));y=rt.target(prefix,t.oracle(c,2))
                emit('update',state=name,index=idx+1,source=source,case=c,version=2,**rt.step(prefix,y,opt))
        for history in ARMS:
            weights=list(mx.load(str(a.start_run/f'seed{a.seed}-{history}-v1.safetensors')).items())
            rt.restore(weights); initial_hash=digest(rt.snapshot())
            emit('reused_state',state=history+'-start',state_hash=initial_hash,sha256=sha(a.start_run/f'seed{a.seed}-{history}-v1.safetensors'))
            pre=evaluate(history+'-start','pre',VALID[:1],1)
            bits=[int(r['scores']['complete']) for r in pre]
            decisions={'constant_novel':'novel','constant_bridged':'bridged','match_history':history,'no_revision':'none'}
            if predictors:
                decisions['developed_constant']=predictors['constant']
                candidates=predictors['states']
                nearest=min(candidates,key=lambda r:(abs(duration-r['duration']),r['history']!=history))
                decisions['history_predictor']=choose(nearest['endpoints'],history)
                nearest=min(candidates,key=lambda r:(sum(x!=y for x,y in zip(bits,r['pre'])),r['history']!=history))
                decisions['pre_observation']=choose(nearest['endpoints'],history)
            emit('pre_decisions',history=history,decisions=decisions,pre=bits)
            prefix_scores={}
            for support in ARMS:
                rt.restore(weights); assert digest(rt.snapshot())==initial_hash
                name=history+'--'+support;opt=rt.optimizer()
                emit('paired_start',state=name,state_hash=digest(rt.snapshot()))
                updates(name,support,opt,0,24);checkpoint(name+'-prefix',opt)
                rows=evaluate(name,'prefix',VALID[:1],2)
                prefix_scores[support]=sum(r['scores']['complete'] for r in rows)/16
            if predictors:
                scores={s:predictors['prefix'][s]['intercept']+predictors['prefix'][s]['slope']*prefix_scores[s] for s in ARMS}
                decisions['prefix_predictor']=choose(scores,history)
                emit('prefix_decision',history=history,scores=scores,decision=decisions['prefix_predictor'])
            validation={}
            for support in ARMS:
                name=history+'--'+support
                rt.restore(list(mx.load(str(out/(name+'-prefix.safetensors'))).items()))
                opt=rt.optimizer();opt.state=tree_unflatten(list(mx.load(str(out/(name+'-prefix-optimizer.safetensors'))).items()))
                emit('optimizer_restore',state=name,step=int(opt.state['step'].item()))
                assert int(opt.state['step'].item())==24
                updates(name,support,opt,24,192);checkpoint(name)
                endpoint_hash=digest(rt.snapshot())
                validation[support]=evaluate(name,'validation',VALID,2)
                if a.verify_continuation and history==support=='novel':
                    rt.restore(weights);opt=rt.optimizer()
                    updates(name+'-continuous-audit',support,opt,0,192)
                    identical=digest(rt.snapshot())==endpoint_hash
                    emit('continuation_equivalence',state=name,identical=identical)
                    assert identical, 'Saved optimizer continuation differs from uninterrupted training'
            decisions['sparse_validation']=choose({s:sum(validation[s][i]['scores']['complete'] for i in SPARSE) for s in ARMS},history)
            decisions['full_validation']=choose({s:sum(r['scores']['complete'] for r in validation[s]) for s in ARMS},history)
            emit('endpoint_decisions',history=history,decisions=decisions)
            save(history+'-decisions.json',decisions)
            # Only after every actionable decision is recorded do we open the final suite.
            rt.restore(weights);evaluate(history+'-start','final',FINAL,2)
            for support in ARMS:
                name=history+'--'+support
                rt.restore(list(mx.load(str(out/(name+'.safetensors'))).items()))
                evaluate(name,'final',FINAL,2)
        emit('invariants',**rt.invariants());status='complete'
    finally:
        emit('finish',status=status,wall_seconds=time.monotonic()-start,wait_seconds=wait,peak_mlx_bytes=mx.get_peak_memory())
        ev.close();rs.close()
        (out/'SHA256SUMS').write_text(''.join(f'{sha(f)}  {f.name}\n' for f in sorted(out.iterdir()) if f.is_file() and f.name!='SHA256SUMS'))

if __name__=='__main__':main()
