"""CPU checks for finite task scoring, schedules and panel boundaries."""
import maintenance_task as t

def main():
    count=0
    for v in range(3):
        for c in t.cases(['test']):
            fields=t.oracle(c,v).split();assert t.check(' '.join(fields),c,v)['complete']
            alternatives=[['PASS','FAIL'],['RESERVE','SKIP'],['SHIP','SKIP'],['0','1'],['SENT','HELD','WAIT']]
            for i,values in enumerate(alternatives):
                for value in values:
                    if value==fields[i]:continue
                    changed=fields.copy();changed[i]=value
                    assert not t.check(' '.join(changed),c,v)['complete'];count+=1
    final=['vornel','hespak','queldin','zartum'];panels=['torvek','jaspel']
    assert not set(final+panels)&set(t.ACQUIRED+t.TARGETS+t.DEV)
    assert not set(final)&set(panels)
    for v in (1,2):
        a=t.schedule('novel',v,64,'negative');b=t.schedule('bridged',v,64,'negative')
        assert len(a)==len(b)==192
        for (sa,ca),(sb,cb) in zip(a,b):
            assert sa==sb and t.oracle(ca,v)==t.oracle(cb,v)
            if sa=='history':assert ca==cb
    sparse=[t.cases(['torvek'])[i] for i in [0,2,4,6,9,11,13,15]]
    assert any(t.oracle(c,2)!=t.oracle(c,1) for c in sparse)
    assert any(t.oracle(c,1)!=t.oracle(c,0) for c in sparse)
    assert any(not t.eligible(c,2) for c in sparse)
    assert len(set(c['stock'] for c in sparse))==2
    print(f'Passed {count} output-field mutations, all schedules and panel boundaries')
if __name__=='__main__':main()
