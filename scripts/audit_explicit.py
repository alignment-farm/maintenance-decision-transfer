"""Reconstruct every table version from retained evidence and audit final outputs."""
import argparse
import hashlib
import json
from pathlib import Path
import maintenance_task as t

def main():
    p=argparse.ArgumentParser();p.add_argument('--run',type=Path,default=Path('evidence/explicit-v1'))
    p.add_argument('--output',type=Path,required=True);a=p.parse_args();assert not a.output.exists()
    es=json.loads((a.run/'evidence.json').read_text());rs=json.loads((a.run/'responses.json').read_text());table={}
    for version in range(3):
        rows=[e for e in es if e['version']==version];supplied={}
        for e in rows:
            assert t.check(e['label'],e['case'],version)['complete']
            key=tuple(e['case'][x] for x in ('channel','priority','certified','stock'))
            assert key not in supplied or supplied[key]==e['label']
            supplied[key]=e['label'];table[key]=e['label']
        for c in t.cases(['audit-only-entity']):
            key=tuple(c[x] for x in ('channel','priority','certified','stock'))
            assert t.check(table[key],c,version)['complete']
    for r in rs:assert t.check(r['raw'],r['case'],2)==r['scores']
    a.output.write_text(json.dumps(dict(status='complete',checked_example_records=len(es),version_condition_checks=48,
        response_records=len(rs),same_version_conflicts=0,
        files={f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in a.run.iterdir()}),indent=2)+'\n')
    print('Explicit table audit passed')
if __name__=='__main__':main()
