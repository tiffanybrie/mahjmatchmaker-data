import re,sys
PIN='https://cdn.jsdelivr.net/gh/tiffanybrie/mahjmatchmaker-data@3cac1c6053d9c646e81d57e1c4352814ba28cdc0/site-app/fym-v82/'
def webify(h, bdir):
    h=h.replace('<script src="b23v1.js"></script>','<script src="'+PIN+'b23v1.js"></script>')
    h=re.sub(r'(["\'])t78/',lambda m:m.group(1)+PIN+'t78/',h)
    b24=open(bdir+'/b24v1.js').read()
    h=h.replace('<script src="b24v1.js"></script>','<script>'+b24+'</script>')
    return h
if __name__=='__main__':
    S=sys.argv[1]
    a=webify(open(S+'/b82/index.html').read(), S+'/b82'); b=open('/tmp/w82.html').read()
    print(a==b, len(a), len(b))
    if a!=b:
        i=next(k for k in range(min(len(a),len(b))) if a[k]!=b[k]); print(repr(a[i-150:i+150])); print(repr(b[i-150:i+150]))
