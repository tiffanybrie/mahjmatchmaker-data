"""Shared mat color model (Tiffany, Oct 19): one PRIMARY color + 0-3 SECONDARY accents + holiday flag.
Codes: pink red blue teal green purple yellow gold neutral bw dark multi."""
import colorsys
CODES=['pink','red','blue','teal','green','purple','yellow','gold','neutral','bw','dark','multi']
LABEL={'pink':'Pink','red':'Red','blue':'Blue','teal':'Teal/Aqua','green':'Green','purple':'Purple','yellow':'Yellow & Orange',
 'gold':'Gold/Mustard','neutral':'Neutral & Ivory','bw':'Black & White','dark':'Dark & Moody','multi':'Multicolor'}
def fam(hexc):
    h,l,s=colorsys.rgb_to_hls(*[int(hexc[i:i+2],16)/255 for i in (1,3,5)]);h*=360
    if l<0.16: return 'black'
    if s<0.14 or (l>0.86 and s<0.45):
        if l>0.72: return 'white'
        if l<0.3: return 'black'
        return 'neutral'
    if l<0.26: return 'dark'
    if h<12 or h>=345: return 'pink' if l>0.68 else 'red'
    if h<38: return 'pink' if (l>0.78 and h<25) else 'yellow'
    if h<55: return 'gold' if (l<0.58 and s<0.75) else 'yellow'
    if h<70: return 'yellow'
    if h<172: return 'green'
    if h<192 and h>=172 and s>0.3: return 'teal'
    if h<195: return 'green' if h<172 else 'blue'
    if h<255: return 'blue'
    if h<290: return 'purple'
    return 'pink' if l>0.45 else 'purple'
def weights(ms):
    w={}
    for hx,p in ms or []:
        f=fam(hx);w[f]=w.get(f,0)+p
    t=sum(w.values()) or 1
    return {k:v/t for k,v in w.items()}
def guess(ms,hol=False):
    """-> (primary, secondary[], ambiguity 0-1)"""
    w=weights(ms)
    white=w.pop('white',0);black=w.pop('black',0);neu=w.pop('neutral',0)
    col=sorted(w.items(),key=lambda x:-x[1])
    colored=sum(v for _,v in col)
    if white>=0.28 and black>=0.18 and colored<0.35: prim='bw'
    elif white+neu+black>=0.62 or not col:
        prim='dark' if black>white+neu else 'neutral'
    else:
        big=[k for k,v in col if v>=0.1]
        prim='multi' if (len(big)>=4 and col[0][1]<0.3) else col[0][0]
    sec=[k for k,v in col if v>=0.08 and k!=prim][:3]
    if prim not in('neutral','bw') and white+neu>=0.2 and len(sec)<3: sec.append('neutral')
    if prim!='dark' and black>=0.2 and len(sec)<3: sec.append('dark')
    vals=[v for _,v in col]+[white+neu]
    vals.sort(reverse=True)
    amb=1-(vals[0]-vals[1]) if len(vals)>1 else 0
    return prim,sec[:3],round(amb,3)
def from_mf(mf):
    m={'orange':'yellow'}
    return [m.get(x,x) for x in (mf or [])]
