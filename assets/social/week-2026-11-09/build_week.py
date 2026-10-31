"""Week of Nov 9-15 storyboard sheets (stills only, for Tiffany's OK). Uses the Oct 31 FYM content bank
(assets/social/fym-bank-oct31) + scripts/social/week_storyboard.sheet(). Usage: python3 build_week.py"""
import os,sys,subprocess
from PIL import Image
H=os.path.dirname(os.path.abspath(__file__)); R=os.path.abspath(H+'/../../..'); B=R+'/assets/social/fym-bank-oct31'
sys.path.insert(0,R+'/scripts/social'); import week_storyboard as ws
ws.OUT=H
def im(p): return Image.open(os.path.join(B,p)).convert('RGB')
def feed(k,n): return [im(f'{k}/feed-{i:02d}.jpg') for i in range(1,n+1)]
def reel_frames(ts):
    out=[]
    for t in ts:
        p=f'/dev/shm/w/_r{t}.jpg'; subprocess.run(['ffmpeg','-loglevel','error','-y','-ss',str(t),'-i',B+'/reel/fym-how-it-works-reel.mp4','-frames:v','1',p],check=True); out.append(Image.open(p).convert('RGB'))
    return out
P1=['Cover: 3 real phones (pick tiles, swipe, match card)','Step 1 Pick your tiles (search)','Step 2 Swipe real mats: Papaya Spritz on Heiress','Step 3 Add racks (Middle & Main)','It\'s a match! card in the app','CTA: free, link in bio, code MAHJMATCH']
ws.sheet('mon-nov09-how-it-works.jpg','MON Nov 9 · 10am ET · How it works (carousel 6 + stories)',
 'Evergreen. Real v1.9.2 screens. OMM + Britt Mills + Middle & Main. Stories = every slide.',list(zip(feed('p1-how-it-works',6),P1)))
ws.sheet('tue-nov10-holiday-reel.jpg','TUE Nov 10 · 11am ET · REEL: Christmas table in 30s',
 'Real screen recording, 32s. Song TBD by Tiffany (by hand). Works silent. Virora, AR, B&B; Sunday + Luxe on screen.',
 list(zip(reel_frames([1,6,8.5,10.6,11.6,15.5,23,27,31]),['Hook: Got your tiles? (typing Tinselle)','Tiles + real mats together','Tap Holiday + Green','✕ The Polo Club (Luxe) flies left','♥ Evergreen & Tartan (Anders Ruff)','Pick your suitor → racks','Swipe racks: ♥ Brick Red, ✕ Dark Navy, ♥ Evergreen','It\'s a match! card','End card: Find Your Mat-ch™, link in bio'])),cols=5)
P3=['Cover: same tiles, 3 colors','The colour chips (tap again to clear)','Orange & coral: Press for (AR)','Blue & teal: Larkspur (OMM)','Green: Greenly (Mahj & Vine)','CTA']
ws.sheet('wed-nov11-color-filter.jpg','WED Nov 11 · 10am ET · Tap a color (carousel 6 + stories)',
 'Evergreen colour-chip demo on Papaya Spritz. OMM, Anders Ruff, Mahj & Vine.',list(zip(feed('p3-color-filter',6),P3)))
P6=['Cover: Tartan Tidings mat door, 3 tile sets','Tinselle (Emerald Green) on Tartan Tidings','Dear Santa (AR) on Tartan Tidings','Rackin\' Rudolph (Hip Hip) on Tartan Tidings','CTA: start with your mat']
ws.sheet('thu-nov12-tartan-tidings-mat-door.jpg','THU Nov 12 · 10am ET · Tartan Tidings mat door (5 + stories)',
 'AR mat (in stock Oct 31) → swipe tile sets. Virora, AR, Hip Hip (no IG handle: name only).',list(zip(feed('p6-tartan-tidings-matdoor',5),P6)))
P4=['Cover: tiles door vs mat door, 2 phones','Already own your tiles? Start there','Love a mat? Start with the mat','CTA']
ws.sheet('fri-nov13-two-doors.jpg','FRI Nov 13 · 10am ET · Two doors (carousel 4 + stories)',
 'Papaya Spritz ↔ Heiress from both doors. OMM + Britt Mills (mat-only maker: shares cross-brand).',list(zip(feed('p4-two-doors',4),P4)))
P2=['Cover: Christmas table in 30 seconds','0:05 Start with your tiles (Tinselle)','0:10 Tap Holiday + Green','0:15 ♥ Evergreen & Tartan','0:25 Swipe the racks','0:30 It\'s a match! (full Story card from the app)','CTA']
ws.sheet('sat-nov14-holiday-30s.jpg','SAT Nov 14 · 10am ET · Holiday table in 30s (7 + stories)',
 'Step stills of Tuesday\'s reel (swap pair if she wants variety). Virora, AR, B&B.',list(zip(feed('p2-holiday-30s',7),P2)))
S=[im('p1-how-it-works/story-01.jpg'),im('p3-color-filter/story-01.jpg'),im('p6-tartan-tidings-matdoor/story-01.jpg'),im('p4-two-doors/story-01.jpg'),im('p2-holiday-30s/story-07.jpg')]
ws.sheet('sun-nov15-story-recap.jpg','SUN Nov 15 · 10am ET · Story-only recap (reuse, auto-post)','Plain image frames, no stickers: auto-posts. Brand @mentions are in the captions/Tag people of each source post.',
 list(zip(S,['How it works','Tap a color','Start with the mat','Two doors','CTA'])),cols=5)
# overview
days=['mon-nov09-how-it-works','tue-nov10-holiday-reel','wed-nov11-color-filter','thu-nov12-tartan-tidings-mat-door','fri-nov13-two-doors','sat-nov14-holiday-30s','sun-nov15-story-recap']
th=[Image.open(f'{H}/{d}.jpg') for d in days]; w=900
th=[t.resize((w,int(t.height*w/t.width))) for t in th]
O=Image.new('RGB',(2*w+60,sum(t.height for t in th[::2])+sum(t.height for t in th[1::2])//1+80),(255,253,208))
y=[20,20]
for i,t in enumerate(th):
    c=i%2; O.paste(t,(20+c*(w+20),y[c])); y[c]+=t.height+20
O=O.crop((0,0,O.width,max(y)+10)); O.save(H+'/week-overview.jpg',quality=82); print('overview',O.size)
