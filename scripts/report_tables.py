"""Render compact inspectable tables from the independently rescored ledger."""
import argparse
from collections import defaultdict
import json
from pathlib import Path

def main():
    p=argparse.ArgumentParser();p.add_argument('analysis',type=Path);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    assert not a.output.exists()
    data=json.loads(a.analysis.read_text())
    lines=['# Complete outcomes','', '| Phase / seed | History | Support | Complete /192 | New /24 | Earlier /24 | Negative /48 | Fresh /64 | Losses | Repairs |',
           '|---|---|---|---:|---:|---:|---:|---:|---:|---:|']
    for run in data['runs']:
        d=run['design']
        for row in run['endpoints']:
            g=row['groups']
            vals=[d['phase']+' / '+str(d['seed']),row['history'],row['support'],row['complete'],g['new']['complete'],g['earlier']['complete'],g['negative']['complete'],g['fresh']['complete'],row['losses'],row['repairs']]
            lines.append('| '+' | '.join(map(str,vals))+' |')
    lines+=['','Losses and repairs concern only obligations unchanged from version 1 to 2.','',
            '## Assessment decisions','', '| Method | 701 Novel | 701 Bridged | 702 Novel | 702 Bridged | Total /768 | Regret |',
            '|---|---:|---:|---:|---:|---:|---:|']
    methods=defaultdict(list)
    for run in data['runs']:
        if run['design']['phase']!='assessment':continue
        for row in run['decisions']:methods[row['method']].append(row)
    for method,rs in methods.items():
        vals=[method]+[f"{r['support']} {r['complete']}" for r in rs]+[sum(r['complete'] for r in rs),sum(r['regret'] for r in rs)]
        lines.append('| '+' | '.join(map(str,vals))+' |')
    lines+=['','## Native investigation costs','', '| Run | Updates | Input / loss tokens | Generations | Prompt / completion tokens | Active seconds | Wait seconds | Peak MLX bytes |',
            '|---|---:|---:|---:|---:|---:|---:|---:|']
    for run in data['acquisitions']+[dict(run=r['design']['phase']+' crossing '+str(r['design']['seed']),costs=r['costs']) for r in data['runs']]:
        c=run['costs'];vals=[run['run'],c['updates'],f"{c['training_input_tokens']} / {c['loss_tokens']}",c['generations'],f"{c['prompt_tokens']} / {c['completion_tokens']}",round(c['wall_seconds']-c['wait_seconds'],2),round(c['wait_seconds'],2),c['peak_mlx_bytes']]
        lines.append('| '+' | '.join(map(str,vals))+' |')
    lines+=['','Audit probes, deterministic explicit-table costs and prior S2 development evidence are separate.','',
            'Detailed per-policy deployment token, update, observation and use costs are in the JSON ledger.','A selected prefix retains its optimizer; endpoint validation retains its chosen endpoint.','Final evaluation calls are investigation costs; the same calls provide an illustrative 192-order deployment use workload.']
    a.output.write_text('\n'.join(lines)+'\n')
if __name__=='__main__':main()
