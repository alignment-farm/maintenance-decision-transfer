"""Finite work-order environment and independently executed response checker."""
import itertools
import re

SCHEMA = ('Execute the established work-order policy. Reply with exactly five space-separated fields: '
          'eligibility (PASS or FAIL), reservation (RESERVE or SKIP), shipment (SHIP or SKIP), '
          'final stock (0 or 1), status (SENT, HELD or WAIT). No explanation.\n')
ACQUIRED = ['daxen', 'miptor', 'velsun', 'robnak']
TARGETS = ['fenzal', 'kudrem', 'sovpik', 'tarnex']
DEV = ['lusbek', 'navrit']
CONDITIONS = list(itertools.product(['copper', 'violet'], ['slow', 'fast'], [0, 1], [0, 1]))

def cases(entities):
    return [dict(entity=e, channel=c, priority=p, certified=q, stock=s)
            for e in entities for c,p,q,s in CONDITIONS]

def eligible(c, version):
    return bool(c['certified'] or (version >= 1 and c['channel']=='copper' and c['priority']=='fast')
                or (version >= 2 and c['channel']=='violet' and c['priority']=='slow'))

def oracle(c, version):
    if not eligible(c, version): return f"FAIL SKIP SKIP {c['stock']} HELD"
    if not c['stock']: return 'PASS SKIP SKIP 0 WAIT'
    return 'PASS RESERVE SHIP 0 SENT'

def rules(version):
    return ('Authoritative policy, applying to EVERY entity: Certification is required for eligibility. '
            + ('Waive certification exactly for copper/fast orders. ' if version==1 else
               'Waive certification exactly for copper/fast and violet/slow orders. ' if version==2 else '')
            + 'If ineligible: FAIL, SKIP reservation, SKIP shipment, leave stock unchanged, HELD. '
            'If eligible with stock 0: PASS, SKIP reservation, SKIP shipment, stock 0, WAIT. '
            'If eligible with stock 1: PASS, RESERVE one unit (stock becomes 0), SHIP that unit, SENT.\n')

def prompt(c, version=None):
    return SCHEMA + (rules(version) if version is not None else '') + '; '.join(f'{k}={v}' for k,v in c.items())

def check(raw, c, version):
    fields=raw.strip().split()
    correct=oracle(c,version).split()
    names=['eligibility','reservation','shipment','stock','status']
    result={n:len(fields)==5 and fields[i]==correct[i] for i,n in enumerate(names)}
    result['format']=bool(re.fullmatch(r'(PASS|FAIL) (RESERVE|SKIP) (SHIP|SKIP) [01] (SENT|HELD|WAIT)',raw.strip()))
    result['exact']=raw.strip()==oracle(c,version)
    # Simulator deliberately does not call eligible() or use the canonical output.
    allowed=c['certified']==1
    if version in (1,2) and (c['channel'],c['priority'])==('copper','fast'): allowed=True
    if version==2 and (c['channel'],c['priority'])==('violet','slow'): allowed=True
    stock=c['stock']; reserved=False; sent=False; valid=result['format']
    if valid:
        gate,reserve,ship,claimed_stock,status=fields
        valid &= (gate=='PASS')==allowed
        if reserve=='RESERVE':
            valid &= allowed and stock>0
            stock-=1;reserved=True
        if ship=='SHIP':
            valid &= allowed and reserved
            sent=True;reserved=False
        expected_status='HELD' if not allowed else 'SENT' if c['stock'] else 'WAIT'
        valid &= int(claimed_stock)==stock and status==expected_status and not reserved
        valid &= sent==(allowed and c['stock']>0)
    result['complete']=bool(valid)
    result['stale']=version>0 and oracle(c,version)!=oracle(c,version-1) and raw.strip()==oracle(c,version-1)
    return result

def schedule(arm, version, blocks=64, boundary_mode='all'):
    entities=TARGETS if arm=='novel' else ACQUIRED[:2]+TARGETS[:2]
    changed=[c for c in cases(entities) if oracle(c,version)!=oracle(c,version-1)]
    boundary=[c for c in cases(entities) if oracle(c,version)==oracle(c,version-1)]
    if boundary_mode=='negative': boundary=[c for c in boundary if not eligible(c,version)]
    elif boundary_mode!='all': raise ValueError(boundary_mode)
    history=[c for c in cases(ACQUIRED) if oracle(c,version)==oracle(c,version-1)]
    return [(source,pool[i%len(pool)]) for i in range(blocks)
            for source,pool in [('correction',changed),('boundary',boundary),('history',history)]]
