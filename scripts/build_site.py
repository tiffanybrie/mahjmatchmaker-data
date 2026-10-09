import re,json
s=open('/home/claude/mb/build/index.html').read()
s=s.replace('<meta charset="utf-8">\n','')
s=re.sub(r'<title>.*?</title>\n','',s)
fonts=re.search(r'<link rel="preconnect"[^>]*>\n<link rel="stylesheet"[^>]*>\n',s).group(0); s=s.replace(fonts,'')
css=re.search(r'<style>(.*?)</style>',s,re.S).group(1)
markup=re.search(r'</style>\n(.*?)<script>',s,re.S).group(1)
js=re.search(r'<script>(.*?)</script>',s,re.S).group(1)
css=css.replace(':root{',':host{').replace('html,body{background:var(--cream);color:var(--navy)}','')
old_body='body{font-family:var(--body);font-size:16px;line-height:1.5;padding-inline:16px;padding-block:0 40px;margin:0}'
assert old_body in css
css=css.replace(old_body,'.app{font-family:var(--body);font-size:16px;line-height:1.5;padding-inline:16px;padding-block:0 40px;background:var(--cream);color:var(--navy);border-radius:24px}')
reps=[("const $=s=>document.querySelector(s);","const $=s=>ROOT.querySelector(s);"),("document.querySelectorAll(","ROOT.querySelectorAll("),("document.querySelector('.seg')","ROOT.querySelector('.seg')"),("document.body.appendChild(","ROOT.appendChild("),("fetch('data.json')","fetch(BASE+'data.json')"),("fetch('catalog.json')","fetch(BASE+'catalog.json')"),("let SP=null; try{const r=await fetch('sprites.json'); if(r.ok) SP=await r.json();}catch(e){}","let SP=null;")]
for a,b in reps:
    assert a in js,a; js=js.replace(a,b)
assert 'document.querySelector' not in js
code=('<!-- mm-match-builder (Matchmaking Table). Data: github.com/tiffanybrie/mahjmatchmaker-data, refreshed daily -->\n'+fonts+
'<div id="mmt-host" style="max-width:1180px;margin:0 auto"></div>\n<script>\n(function(){\nvar host=document.getElementById("mmt-host"); if(!host||host.shadowRoot) return;\nvar ROOT=host.attachShadow({mode:"open"});\nROOT.innerHTML='+
json.dumps('<style>'+css+'</style>')+'+\'<div class="app wrap">\'+'+json.dumps(markup)+'+\'</div>\';\nvar BASE="https://cdn.jsdelivr.net/gh/tiffanybrie/mahjmatchmaker-data@main/";\n'+js+'\n})();\n</script>\n<!-- /mm-match-builder -->\n')
open('code-block.html','w').write(code)
open('/tmp/cb.js','w').write(re.findall(r'<script>(.*?)</script>',code,re.S)[0])
json.dump(code,open('code-block.json','w'))
print(len(code))
