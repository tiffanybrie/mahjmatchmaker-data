"""Round 2 (Tiffany Nov 23 5:24pm): every rack shows as ONE horizontal rack in every view
(Up close, Aerial, rack cards, picks, match card), using the Table view cut-out (D.tv.ro)
instead of the store's photo (e.g. Miss Mahjong Peach Sorbet = 4 racks stacked on an angle).
Usage: python3 single_rack.py <index.html>"""
import sys
p=sys.argv[1];s=open(p).read()
old="rackSrc=id=>IMG[R[id].im],"
if old in s:
    s=s.replace(old,"rackSrc=id=>(D.tv&&D.tv.ro&&D.tv.ro[id])||IMG[R[id].im]/*r2 Nov 23: one horizontal rack everywhere*/,")
    open(p,'w').write(s);print('patched')
else: print('already patched or pattern missing')
