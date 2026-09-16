"""Manifest/token/schedule audit and separate-process checkpoint probes."""
import argparse
from collections import defaultdict
import json
import os
import random
from pathlib import Path
import subprocess
import time
import mlx.core as mx
from runtime import Runtime,resource,sha,digest
from analyze import checked,dump
import maintenance_task as t

def main():
    p=argparse.ArgumentParser();p.add_argument('--runs',nargs='+',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    a.output.mkdir(parents=True,exist_ok=False)
    for name in ['audit.py','analyze.py','runtime.py','maintenance_task.py']:
        (a.output/name).write_bytes(Path('scripts',name).read_bytes())
    start=time.monotonic();wait=0.;last=0.
    checks=[]
    def guard():
        nonlocal last,wait
        if time.monotonic()-last>5:
            while True:
                lines=subprocess.check_output(['ps','-axo','pid,etime,rss,command'],text=True).splitlines()
                jobs=[l for l in lines if '/bin/python' in l and 'scripts/' in l and 'monitor.py' not in l and int(l.split()[0])!=os.getpid()]
                checks.append(dict(seconds=time.monotonic()-start,jobs=jobs))
                if not jobs:break
                tick=time.monotonic();time.sleep(10);wait+=time.monotonic()-tick;assert wait<7200
            last=time.monotonic()
        assert time.monotonic()-start-wait<3600 and mx.get_peak_memory()<40e9
    guard();res=resource();rt=Runtime();reports=[];probes=[]
    probe_file=(a.output/'probes.jsonl').open('x')
    for run in a.runs:
        ev,rows=checked(run);design=json.loads((run/'design.json').read_text())
        # Full token accounting, independent rescoring already performed by checked().
        for r in rows:
            assert rt.encode(t.prompt(r['case']))==r['prefix']
            text=rt.tokenizer.decode(r['ids'][:-1] if r['ended'] else r['ids'])
            assert text==r['raw']
            assert len(r['prefix'])==r['prompt_tokens'] and len(r['ids'])==r['completion_tokens']
        updates=defaultdict(list)
        for e in ev:
            if e['kind']!='update':continue
            prefix=rt.encode(t.prompt(e['case']));target=rt.target(prefix,t.oracle(e['case'],e['version']))
            assert len(target)==e['loss_tokens'] and len(prefix)+len(target)-1==e['input_tokens']
            updates[e['state']].append(e)
        for name,records in updates.items():
            assert [e['index'] for e in records]==list(range(1,len(records)+1))
            if '--' in name:
                support=name.split('--')[1].split('-continuous')[0]
                assert len(records)==192
                expected=t.schedule(support,2,64,'negative')
                assert [(e['source'],e['case']) for e in records]==expected
            elif name.endswith('-v1'):
                support=name.split('-')[1]
                assert [(e['source'],e['case']) for e in records]==t.schedule(support,1,64,'negative')
            elif name.endswith('-acquisition'):
                seed=int(name.split('-')[0][4:]);rng=random.Random(seed);expected=[]
                for _ in range(16):
                    cycle=t.cases(t.ACQUIRED);rng.shuffle(cycle);expected+=cycle
                assert [e['case'] for e in records]==expected[:len(records)]
        if 'validation' in design:
            for h in ['novel','bridged']:
                decision_idx=next(i for i,e in enumerate(ev) if e['kind']=='endpoint_decisions' and e['history']==h)
                final_idx=min(i for i,e in enumerate(ev) if e['kind']=='evaluation' and e.get('panel')=='final' and e['state'].startswith(h))
                assert decision_idx<final_idx
                starts=[e['state_hash'] for e in ev if e['kind']=='paired_start' and e['state'].startswith(h)]
                assert len(starts)==2 and len(set(starts))==1
        for e in ev:
            if e['kind']!='checkpoint':continue
            name=e['state'];path=run/(name+'.safetensors')
            assert sha(path)==e['sha256'];rt.restore(list(mx.load(str(path)).items()))
            assert digest(rt.snapshot())==e['state_hash']
            if name.endswith('-prefix'):
                matching=[r for r in rows if r['state']==name[:-7] and r.get('panel')=='prefix']
            else:matching=[r for r in rows if r['state']==name and r.get('repeat',0)==0 and r.get('panel','final')=='final']
            assert matching,name
            # One entity's entire finite condition set plus every distinct failed output.
            selected=[r for r in matching if r['case']['entity']==matching[0]['case']['entity']]
            seen={(r['raw'],r['scores']['complete']) for r in selected}
            for r in matching:
                signature=(r['raw'],r['scores']['complete'])
                if not r['scores']['complete'] and signature not in seen:selected.append(r);seen.add(signature)
            for r in selected:
                guard();new=rt.generate(r['prefix'],limit=40);assert new['raw']==r['raw'],(name,r['case'])
                record=dict(run=str(run),state=name,case=r['case'],**new)
                probe_file.write(json.dumps(record)+'\n');probe_file.flush();probes.append(record)
        reports.append(dict(run=str(run),responses=len(rows),updates=sum(map(len,updates.values())),checkpoints=sum(e['kind']=='checkpoint' for e in ev)))
        print('audited',run,reports[-1],flush=True)
    probe_file.close()
    dump(a.output/'report.json',dict(status='complete',revision=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),runs=reports,
        probes=len(probes),prompt_tokens=sum(r['prompt_tokens'] for r in probes),completion_tokens=sum(r['completion_tokens'] for r in probes),
        generation_seconds=sum(r['seconds'] for r in probes),wall_seconds=time.monotonic()-start,wait_seconds=wait,
        peak_mlx_bytes=mx.get_peak_memory(),resource=res,resource_checks=checks))
    (a.output/'SHA256SUMS').write_text(''.join(f'{sha(f)}  {f.name}\n' for f in sorted(a.output.iterdir()) if f.is_file() and f.name!='SHA256SUMS'))
if __name__=='__main__':main()
