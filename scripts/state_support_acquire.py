"""Fresh acquisitions and revision-1 histories for the state/support assessment."""
import argparse
import json
import os
from pathlib import Path
import random
import subprocess
import time
import mlx.core as mx
from runtime import Runtime, resource, sha, digest
import maintenance_task as task


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--phase',choices=['final'],default='final')
    p.add_argument('--seeds',nargs='+',type=int,default=[501,502])
    p.add_argument('--blocks',type=int,default=64)
    p.add_argument('--boundary-mode',choices=['all','negative'],default='negative')
    args=p.parse_args();out=args.output;out.mkdir(parents=True,exist_ok=False)
    start=time.monotonic();wait=0.;last=0.;status='failed'
    for n in ['maintenance_task.py','state_support_acquire.py','runtime.py','task.py']:
        (out/n).write_bytes(Path('scripts',n).read_bytes())
    (out/'protocol.md').write_bytes(Path('protocol/state-support-final-v1.md').read_bytes())
    def save(n,d): (out/n).write_text(json.dumps(d,indent=2)+'\n')
    events=(out/'events.jsonl').open('x');responses=(out/'responses.jsonl').open('x')
    def emit(kind,**data):
        events.write(json.dumps(dict(kind=kind,elapsed=time.monotonic()-start,**data))+'\n');events.flush()
    def guard():
        nonlocal last,wait
        if time.monotonic()-last>5:
            while True:
                lines=subprocess.check_output(['ps','-axo','pid,etime,rss,command'],text=True).splitlines()
                jobs=[l for l in lines if '/bin/python' in l and 'scripts/' in l and 'monitor.py' not in l and int(l.split()[0])!=os.getpid()]
                emit('resource_check',jobs=jobs)
                if not jobs: break
                t=time.monotonic();time.sleep(10);wait+=time.monotonic()-t
                assert wait<7200,'shared hardware wait limit'
            last=time.monotonic()
        assert time.monotonic()-start-wait<3600,'active hour ceiling'
        assert mx.get_peak_memory()<40e9,'MLX allocation ceiling'
    fresh=task.DEV if args.phase=='development' else ['zelvon','barmek','nustal','pelrik']
    assert not set(fresh)&set(task.ACQUIRED+task.TARGETS)
    if args.phase=='final': assert not set(fresh)&set(task.DEV)
    save('design.json',dict(phase=args.phase,seeds=args.seeds,blocks=args.blocks,fresh=fresh,
                           acquired=task.ACQUIRED,targets=task.TARGETS,boundary_mode=args.boundary_mode,
                           repeat_entities=[task.ACQUIRED[0],fresh[0]] if args.phase=='final' else task.ACQUIRED+task.TARGETS+fresh))
    try:
        emit('revision',git=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),
             dirty=subprocess.check_output(['git','status','--short'],text=True))
        guard();save('resource.json',resource());rt=Runtime(seed=args.seeds[0])
        def evaluate(name,version,entities,rule=False,passes=1):
            summaries=[]
            for repeat in range(passes):
                counts={};n=0
                repeat_entities=entities if repeat==0 or args.phase!='final' else [task.ACQUIRED[0],fresh[0]]
                for c in task.cases(repeat_entities):
                    guard();prefix=rt.encode(task.prompt(c,version if rule else None));r=rt.generate(prefix,limit=40)
                    scores=task.check(r['raw'],c,version)
                    for k,v in scores.items(): counts[k]=counts.get(k,0)+int(v)
                    n+=1
                    responses.write(json.dumps(dict(state=name,version=version,repeat=repeat,case=c,
                        rule=rule,prefix=prefix,expected=task.oracle(c,version),scores=scores,**r))+'\n');responses.flush()
                summary=dict(n=n,**counts);summaries.append(summary)
                emit('evaluation',state=name,version=version,repeat=repeat,summary=summary)
                print(name,version,repeat,summary,flush=True)
            return summaries[0]
        def checkpoint(name):
            path=out/(name+'.safetensors');mx.save_safetensors(str(path),dict(rt.snapshot()))
            emit('checkpoint',state=name,sha256=sha(path),state_hash=digest(rt.snapshot()),bytes=path.stat().st_size)
        def update(name,i,source,c,v,opt):
            guard();prefix=rt.encode(task.prompt(c));y=rt.target(prefix,task.oracle(c,v))
            emit('update',state=name,index=i,source=source,case=c,version=v,**rt.step(prefix,y,opt))
        all_entities=task.ACQUIRED+task.TARGETS+fresh
        for seed in args.seeds:
            rt.reinitialize(seed);seedname=f'seed{seed}'
            opt=rt.optimizer();rng=random.Random(seed);order=[]
            for _ in range(16):
                cycle=task.cases(task.ACQUIRED);rng.shuffle(cycle);order+=cycle
            acquired=None
            for i,c in enumerate(order,1):
                update(seedname+'-acquisition',i,'acquisition',c,0,opt)
                if i in (256,512,1024):
                    name=seedname+f'-A{i}';checkpoint(name)
                    recall=evaluate(name,0,task.ACQUIRED);transfer=evaluate(name+'-new',0,task.DEV)
                    passed=recall['complete']>=60 and transfer['complete']/transfer['n']>=.875
                    emit('acquisition_criterion',state=name,passed=passed,recall=recall,transfer=transfer)
                    if passed: acquired=rt.snapshot();break
            if acquired is None:
                emit('acquisition_failed',seed=seed);continue
            for arm in ('novel','bridged'):
                rt.restore(acquired)
                emit('paired_start',state=seedname+'-'+arm,state_hash=digest(rt.snapshot()))
                for version in (1,):
                    name=seedname+'-'+arm+f'-v{version}';opt=rt.optimizer()
                    maintenance_tick=time.monotonic();old=task.cases(task.ACQUIRED)
                    obsolete=[c for c in old if task.oracle(c,version)!=task.oracle(c,version-1)]
                    emit('maintenance',state=name,scanned=len(old),excluded=len(obsolete),
                         authority='investigator',obsolete=obsolete,
                         prior_revision_relabels=sum(task.oracle(c,version-1)!=task.oracle(c,0) for c in old),
                         history_maintenance_seconds=time.monotonic()-maintenance_tick)
                    for i,(source,c) in enumerate(task.schedule(arm,version,args.blocks,args.boundary_mode),1):
                        update(name,i,source,c,version,opt)
                    checkpoint(name);evaluate(name,version,all_entities,passes=2)
            emit('invariants',seed=seed,**rt.invariants())
        status='complete'
    finally:
        emit('finish',status=status,wall_seconds=time.monotonic()-start,wait_seconds=wait,
             peak_mlx_bytes=mx.get_peak_memory())
        events.close();responses.close()
        (out/'SHA256SUMS').write_text(''.join(f'{sha(f)}  {f.name}\n' for f in sorted(out.iterdir()) if f.is_file() and f.name!='SHA256SUMS'))

if __name__=='__main__':main()
