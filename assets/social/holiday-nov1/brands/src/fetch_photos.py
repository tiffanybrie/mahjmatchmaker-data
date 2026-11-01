import json,urllib.request,os,sys
items={ # slug: (product url, variant id or None, nimgs)
 'ar-classic':('shop.andersruff.com/products/classic-very-merry-mahj-mahjong-mat',None),
 'ar-tidings':('shop.andersruff.com/products/tartan-tidings-mahjong-mat',None),
 'ar-toile':('shop.andersruff.com/products/tartan-toile-noel-mahjong-mat',None),
 'ar-mail':('shop.andersruff.com/products/santas-mahjong-mail-mahjong-mat',None),
 'ar-candy':('shop.andersruff.com/products/candy-cane-lane-mahjong-mat',None),
 'ar-water':('shop.andersruff.com/products/watercolor-christmas-tree-mahjong-mat',None),
 'ar-ever':('shop.andersruff.com/products/evergreen-tartan-mahjong-mat',None),
 'ar-pink':('shop.andersruff.com/products/very-merry-mahj-mahjong-mat',None),
 'ar-dearsanta':('shop.andersruff.com/products/dear-santa-mahjong-tile-set',None),
 'vir-tinselle':('www.viroramahjong.com/products/tinselle-emerald-green',None),
 'bbb-holiday':('www.bambirdboutique.com/products/holiday-neoprene-mahjong-mat',None),
 'omm-yuletide':('ohmymahjong.com/products/yuletide-mat-in-tube',None),
 'bam-hjmat':('www.bamletsmahjong.com/products/holly-jolly-mahjong-mat',None),
 'bam-hjtiles':('www.bamletsmahjong.com/products/holly-jolly-christmas-mahjong-tiles',None),
 'hh-rudolph':('www.hiphipmahjong.com/products/rackin-rudolph-mahjong-mat',None),
 'mr-letters':('mahjongregister.com/products/preorder-letters-to-santa-premium-mahjong-mat-33-estimated-ship-oct-1st-2026',None),
 'mr-wreath':('mahjongregister.com/products/preorder-moonlit-crane-premium-mahjong-mat-33-estimated-ship-aug-20th-copy',None),
 'plm-hol':('peacelovemahjong.com/products/mahjong-mats-holiday',None),
 'omm-clara':('ohmymahjong.com/products/clara-mat-in-tube',None),
 'omm-merriment':('ohmymahjong.com/products/merriment-mat-in-tube',None),
 'omm-sugarplum':('ohmymahjong.com/products/sugarplum-mat',None),
 'omm-winterberry':('ohmymahjong.com/products/winterberry-mat-in-tube',None),
 'ms-candypink':('mahjsquadshop.com/products/candy-cane-pink-wonderland-mahjong-mat',None),
 'ms-clara':('mahjsquadshop.com/products/claras-dream',None),
 'bm-nutcracker':('brittmillsdesign.com/products/nutcracker-neoprene-mahjong-mat-arriving-late-october',None),
}
os.makedirs('img',exist_ok=True); meta={}
for slug,(u,_) in items.items():
  try:
    p=json.load(urllib.request.urlopen(urllib.request.Request('https://'+u+'.js',headers={'User-Agent':'Mozilla/5.0'}),timeout=30))
  except Exception as e: print('ERR',slug,e); continue
  meta[slug]={'title':p['title'],'available':p['available'],'variants':[(v['id'],v['title'],v['available'],(v.get('featured_image') or {}).get('src')) for v in p['variants']]}
  imgs=p['images'][:6] if slug not in('plm-hol','bam-hjtiles') else p['images'][:20]
  for i,s in enumerate(imgs):
    s=('https:'+s if s.startswith('//') else s).split('?')[0]
    fn=f'img/{slug}-{i}.jpg'
    if not os.path.exists(fn):
      try:
        data=urllib.request.urlopen(urllib.request.Request(s+'?width=1600',headers={'User-Agent':'Mozilla/5.0'}),timeout=30).read(); open(fn,'wb').write(data)
      except Exception as e: print('imgERR',slug,i,e)
  print(slug,p['available'],len(imgs))
json.dump(meta,open('prodmeta.json','w'),indent=1)
