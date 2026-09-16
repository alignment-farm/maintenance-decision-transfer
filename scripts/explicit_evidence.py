"""Retained examples, keyed by supplied condition fields; no rules at use time."""
import json
import argparse
from pathlib import Path
import time
import maintenance_task as t

def key(c): return '|'.join(str(c[k]) for k in ('channel','priority','certified','stock'))
def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=Path('evidence/explicit-v1'));a=p.parse_args()
    out=a.output;out.mkdir(exist_ok=False)
    tick=time.perf_counter();table={};evidence=[];operations=[]
    # Labels are precisely the supervised original/correction evidence, not final cases.
    for version in range(3):
        cases=t.cases(t.ACQUIRED) if version==0 else [c for source,c in t.schedule('novel',version,64,'negative') if source=='correction']
        overwritten=set()
        for c in cases:
            k=key(c);label=t.oracle(c,version)
            if k in table and table[k]!=label:overwritten.add(k)
            table[k]=label;evidence.append(dict(version=version,case=c,label=label))
        operations.append(dict(version=version,scanned=len(cases),unique_keys=len(set(map(key,cases))),overwrites=len(overwritten)))
    construction_seconds=time.perf_counter()-tick
    (out/'table.json').write_text(json.dumps(table,indent=2)+'\n')
    assert len(table)==16
    tick=time.perf_counter();rows=[]
    for c in t.cases(t.ACQUIRED+t.TARGETS+['vornel','hespak','queldin','zartum']):
        raw=table[key(c)];rows.append(dict(case=c,raw=raw,scores=t.check(raw,c,2)))
    use_seconds=time.perf_counter()-tick
    assert all(r['scores']['complete'] for r in rows)
    (out/'evidence.json').write_text(json.dumps(evidence,indent=2)+'\n')
    (out/'responses.json').write_text(json.dumps(rows,indent=2)+'\n')
    (out/'report.json').write_text(json.dumps(dict(complete=sum(r['scores']['complete'] for r in rows),n=len(rows),operations=operations,
        construction_seconds=construction_seconds,use_seconds=use_seconds,key_reads=len(rows),table_bytes=(out/'table.json').stat().st_size,
        assumptions=['entity-invariant policy','exact supplied channel/priority/certified/stock addressing','authoritative checked labels','investigator correction scope']),indent=2)+'\n')
    (out/'explicit_evidence.py').write_bytes(Path(__file__).read_bytes())
    print((out/'report.json').read_text())
if __name__=='__main__':main()
