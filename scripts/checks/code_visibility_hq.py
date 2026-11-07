#!/usr/bin/env python3
"""Turn docs/status/code-visibility.json into the per-brand rows HQ's Code scorecard card reads (hq/codeScore.brands).
Usage: python3 scripts/checks/code_visibility_hq.py [out.json]  -> then ArtifactData update hq/codeScore with file_path=out.json"""
import json, sys
K=['google_organic_top3','google_ai_overview','google_ai_mode','chatgpt','gemini','claude_search']
d=json.load(open('docs/status/code-visibility.json'))
rows=[]
for b in d['brands']:
    r={'b':b['brand']}
    for k in K:
        c=b.get(k); r[k]=None if not c else [c['hits'],c['n'],c.get('last'),bool(c.get('lasthit'))]
    s=b.get('sales') or {}; r['s7']=s.get('last7'); r['p7']=s.get('prev7'); rows.append(r)
out=sys.argv[1] if len(sys.argv)>1 else 'docs/status/code-visibility-hq-brands.json'
json.dump({'brands':rows},open(out,'w')); print(out, len(rows))
