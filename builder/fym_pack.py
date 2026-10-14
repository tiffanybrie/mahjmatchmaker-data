import json,re,os,base64,shutil
SP='/tmp/claude-0/-home-claude-mahjmatchmaker-data/801d31e6-4a74-59be-8637-eb67bfa0e99e/scratchpad/sw2'
t=open(SP+'/index.html').read()
fs=sorted(set(re.findall(r'"(m/\d+\.\w+)"',t)),key=lambda x:int(x[2:].split('.')[0]))
os.makedirs(SP+'/mc',exist_ok=True)
ch={}
for f in fs:
    c=int(f[2:].split('.')[0])//12;ext=f.rsplit('.',1)[1];mime='image/webp' if ext=='webp' else 'image/jpeg'
    b=open(SP+'/'+f,'rb').read()
    if b[:4]==b'RIFF': mime='image/webp'
    elif b[:3]==b'\xff\xd8\xff': mime='image/jpeg'
    elif b[:4]==b'\x89PNG': mime='image/png'
    ch.setdefault(c,{})[f]='data:%s;base64,'%mime+base64.b64encode(b).decode()
for c,o in ch.items(): json.dump(o,open(f'{SP}/mc/{c}.json','w'),separators=(',',':'))
shutil.rmtree(SP+'/m')
print(len(fs),len(ch))
