"""Join audited artifacts and native costs without treating paired orders as samples."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
from analyze import checked,dump

def main():
    p=argparse.ArgumentParser();p.add_argument('--analysis',type=Path,required=True)
    p.add_argument('--audits',nargs='+',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    assert not a.output.exists()
    data=json.loads(a.analysis.read_text());audit_reports=[];audited={}
    for audit in a.audits:
        for line in (audit/'SHA256SUMS').read_text().splitlines():
            h,n=line.split('  ',1);assert hashlib.sha256((audit/n).read_bytes()).hexdigest()==h
        report=json.loads((audit/'report.json').read_text());assert report['status']=='complete'
        audit_reports.append(report)
        for run in report['runs']:
            assert run['run'] not in audited
            audited[run['run']]=run
    paths=[Path(r['run']) for r in data['acquisitions']]
    paths += [Path(r['source_run']) for r in data['runs']]
    assert set(map(str,paths))==set(audited)
    all_costs=[r['costs'] for r in data['acquisitions']+data['runs']]
    checks=[]
    for run in paths:
        events,rows=checked(run)
        assert len(rows)==audited[str(run)]['responses']
        assert sum(e['kind']=='update' for e in events)==audited[str(run)]['updates']
        assert all(e['base_unchanged'] and e['reset_max_logit_delta']==0 for e in events if e['kind']=='invariants')
        checks.extend(e for e in events if e['kind']=='resource_check')
    frozen=Path('evidence/frozen-predictors-v1.json').read_bytes()
    assert frozen==subprocess.check_output(['git','show','735f941:evidence/frozen-predictors-v1.json'])
    assessment=[r for r in data['runs'] if r['design']['phase']=='assessment']
    assert {r['design']['seed'] for r in assessment}=={701,702}
    for run in assessment:assert (Path(run['source_run'])/'predictors.json').read_bytes()==frozen
    totals={k:sum(c[k] for c in all_costs) for k in ['updates','training_input_tokens','loss_tokens','training_seconds','generations','prompt_tokens','completion_tokens','generation_seconds','wall_seconds','wait_seconds','checkpoint_bytes']}
    totals['active_seconds']=totals['wall_seconds']-totals['wait_seconds']
    totals['peak_mlx_bytes']=max(c['peak_mlx_bytes'] for c in all_costs)
    assert totals['updates']<=6720
    assert totals['peak_mlx_bytes']<40e9
    methods={}
    for run in assessment:
        for r in run['decisions']:
            z=methods.setdefault(r['method'],dict(complete=0,n=0,gap_to_two_support_oracle=0))
            z['complete']+=r['complete'];z['n']+=192;z['gap_to_two_support_oracle']+=r['regret']
    oracle=sum(max(e['complete'] for e in run['endpoints'] if e['history']==h and e['support']!='none') for run in assessment for h in ['novel','bridged'])
    audit_totals={k:sum(r[k] for r in audit_reports) for k in ['probes','prompt_tokens','completion_tokens','generation_seconds','wall_seconds','wait_seconds']}
    explicit=json.loads(Path('evidence/explicit-audit.json').read_text());assert explicit['status']=='complete'
    for name,h in explicit['files'].items():assert hashlib.sha256((Path('evidence/explicit-v1')/name).read_bytes()).hexdigest()==h
    dump(a.output,dict(status='complete',source_analysis_sha256=hashlib.sha256(a.analysis.read_bytes()).hexdigest(),
        revision=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),totals=totals,audit_totals=audit_totals,
        audit_runs=audited,assessment_methods=methods,assessment_two_support_oracle=dict(complete=oracle,n=768),
        resource_checks=len(checks),checks_with_visible_competing_jobs=sum(bool(e['jobs']) for e in checks),
        predictor_freeze_revision='735f941',explicit_control=json.loads(Path('evidence/explicit-v1/report.json').read_text())))
    print(a.output.read_text())
if __name__=='__main__':main()
