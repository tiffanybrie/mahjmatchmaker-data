"""Splice card.js into the pending FYM build (replaces the old match-card block) and add the Caprasimo font.
Idempotent: finds the card block by its start/end markers. Usage: python3 splice.py [index.html]"""
import sys,re
B=sys.argv[1] if len(sys.argv)>1 else '/tmp/claude-0/-home-claude/801d31e6-4a74-59be-8637-eb67bfa0e99e/scratchpad/fymfix2/build/index.html'
s=open(B).read();new=open(__file__.replace('splice.py','card.js')).read().rstrip()+'\n'
starts=['/* ---------- match card (Oct 18 redesign','/* ---------- match card: branded image']
i=min(s.find(m) for m in starts if s.find(m)>=0);j=s.index('async function share(',i)
s=s[:i]+new+s[j:]
if 'family=Caprasimo' not in s:s=s.replace('fonts.googleapis.com/css2?family=Bitter','fonts.googleapis.com/css2?family=Caprasimo&family=Bitter',1)
open(B,'w').write(s);print('spliced',len(new),'chars; caprasimo' if 'family=Caprasimo' in s else '')
