"""Study-owned sequential task, exact scoring, and deterministic split construction."""
import itertools,random,string,re
SCHEMA=('Return exactly one tool call, with no explanation or Markdown. '
 'Available calls: kestrel(text="...") and marten(text="..."). '
 'The input has channel, priority, and a lowercase ASCII identifier. '
 'Apply the established routing and argument protocol.')
REMINDER=('Infer a single consistent protocol from all checked calls below. '
 'Account for both input fields and all changes to the text argument '
 'when applying it to the new identifier.\n')
A_WORDS=['pelk','druvan','snebit','korvaz']
B_WORDS=['fepzan','molkit','vurbex','tasnid']
C_WORDS=['jebrun','waskel','pivnot','zomdak']
DEV_WORDS=['sulpev','ravnik','hezbom','kutlan']
def cases(words,channels=('copper','violet')):
 return [dict(channel=c,priority=p,identifier=w) for w in words for c,p in itertools.product(channels,['slow','fast'])]
def scope(c):return c['channel']=='copper' and c['priority']=='fast'
def route(c,revised=False):
 return 'marten' if revised and scope(c) else dict(copper='kestrel',violet='marten',amber='marten',teal='kestrel')[c['channel']]
def query(c):return f'channel={c["channel"]}; priority={c["priority"]}; identifier={c["identifier"]}'
def oracle(c,revised=False):return route(c,revised)+'(text="'+c['identifier'].upper()+('-Q' if c['priority']=='fast' else '')+'")'
def prompt(c,evidence=False,revised=False,clean=False,rules=False):
 extra=''
 if evidence:
  examples=cases(A_WORDS)+cases(B_WORDS,('amber','teal'))
  # Development used relabeling; final drops obsolete records and adds actual corrections.
  if revised:
   if clean:examples=[x for x in examples if not scope(x)]
   examples += [x for x in cases(C_WORDS) if scope(x)]
  extra=REMINDER+'Checked successful calls:\n'+'\n'.join(query(x)+' -> '+oracle(x,revised) for x in examples)
 if rules:
  extra=('Channel copper selects kestrel; violet selects marten; amber selects marten; teal selects kestrel. '
   +('Exception: if and only if channel is copper AND priority is fast, select marten instead of kestrel. ' if revised else '')
   +'Uppercase the identifier. Append -Q if priority is fast; append nothing if slow. Apply these rules to every identifier and combination.')
 return SCHEMA+'\n'+extra+'\n'+query(c)
def score(raw,c,revised=False):
 m=re.fullmatch(r'(kestrel|marten)\(text="([^"\n]*)"\)',raw.strip())
 d=dict(full=raw.strip()==oracle(c,revised),format=bool(m),route=False,identifier=False,suffix=False,stale=False,overgeneralized=False)
 if m:
  tool,arg=m.groups();body=arg[:-2] if arg.endswith('-Q') else arg
  d.update(route=tool==route(c,revised),identifier=body==c['identifier'].upper(),suffix=arg.endswith('-Q')==(c['priority']=='fast'),stale=revised and scope(c) and tool==route(c,False),overgeneralized=revised and c['channel']=='copper' and c['priority']=='slow' and tool=='marten')
 return d
def fresh(seed,n=24):
 rng=random.Random(seed);used=set(A_WORDS+B_WORDS+C_WORDS+DEV_WORDS);words=[]
 for i in range(n):
  length=[4,6,8,10][i%4]
  while True:
   w=''.join(rng.choice(string.ascii_lowercase) for _ in range(length))
   if w not in used:break
  words.append(w);used.add(w)
 return words
