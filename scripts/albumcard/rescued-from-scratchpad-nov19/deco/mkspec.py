import json
S='/tmp/claude-0/-home-claude/05549d34-8fe3-5ca9-a6a5-308991cb9a78/scratchpad/deco/'
R='/home/claude/mahjmatchmaker-data/'
p=json.load(open(S+'picks.json'));mf=json.load(open(S+'matfiles.json'))
LOWRES={'SoHo','Evergreen','Tiger Fans','Mulberry and Sage','Year of the Snake','Burgundy Grove','Midnight Peacock'}
W={'deco-lagoon':{
'Reba':"Your favorite Deco pairing. The deep teal field holds her Lagoon backs, and the pink frame and bouquet pick up her mulberry and rose faces.",
'Wren':"A dark lagoon center inside a mulberry scalloped frame, with a plum paisley border. Her back color plus her faces' second color, like it was made for her.",
'Deco Dragon (Mulberry)':"Bam Bird Boutique's own Deco Dragon mat, in her sister color. Same deco lines and dragons as the tiles, and the mulberry plays off the teal instead of copying it.",
'Caroline in Peacock':"A peacock teal center inside a frame of berry and magenta blooms. Both of her colors at full strength.",
'Gilded Peacock':"Art deco on art deco: gold fan lines and peacock feathers on deep teal, with an ivory center like her faces.",
'Peony Sociale Premium':"Deep teal medallions with hot pink peonies. Teal for the backs, berry pink for the craks.",
'Spring Blooms Premium':"A lagoon-teal center framed in plum and gold flowers: the backs, the crak frames and the gold palm all at once.",
'Viola':"A deep teal center inside a black floral border of pinks and plums. Moody, and very her.",
'Mahj In Bloom Mat':"Deep teal with lilac and pink roses, in a lilac frame. Soft berry on her teal.",
'Year of the Snake':"Lagoon-blue ground with a pink frame and pink snakes; the sage center keeps it soft.",
'Ocean Florals':"A dark teal center ringed in coral, rose and blue blooms, close to her rose crak frames.",
'Plum Panda Premium':"Teal-green with a plum border and little pink flowers. The orange trim is the only stretch.",
'Petals After Dark':"Black with teal and pink petals: her teal bams and mulberry faces on a night sky.",
'Eden':"A deep teal frame around a garden of blues and corals; the pond in the middle picks up her periwinkle stars.",
'SoHo':"Oh My Mahjong's deco sunburst in teal, blue and green. Retired, but a match if you already own it.",
'Gatsby Glow':"Deco fans and a gold sunburst, from the same era as the tiles. The blue-teal fans carry the backs; the rust sun is the one wild card.",
'Crown Jewels':"Navy with jewel-tone flowers and a gold line border. The navy picks up her dots and numbers.",
'Midnight Peacock':"Deep teal-green with gold palms, a quiet echo of the gold palm on every back.",
'Royal Peacock':"A lagoon-blue center framed in pink, with peacock feathers like her wind tiles.",
'Imperial Peacock':"A peacock and pink lotuses on ivory. Lighter than she is, but it carries every face color.",
'Imperial Koi Pond':"Deep navy-teal with coral koi and a gold frame.",
'Indigo Reef':"Navy-teal sea, gold fretwork and an ivory center. The gold frame matches her palm.",
'Crane & Moon':"Deep teal with a gold moon, cranes and coral flowers. The crane is a twin of her 1 Bam.",
'Teal Tapestry':"A teal, gold and rust medallion on ivory, like a deco tile floor.",
'Garden Party – Mulberry':"A berry center with a teal edge and lilac scallops. The tiles bring the teal, the mat brings the berry.",
'Hawthorne':"A plum center inside navy and gold. Rich and dark, so her mulberry crak frames come forward.",
'Pretty in Plum Premium':"Plum, lilac and ivory with a scalloped deco pattern in the middle: her mulberry faces, big.",
'Deco Dragon (Indigo)':"Bam Bird Boutique's navy Deco Dragon. It matches her navy dots and numbers, and the dragons match hers.",
'Community Joy':"Lagoon stripes and a raspberry star. Brighter and more preppy than the tiles, but the teal and berry line up exactly.",
'Purple & Aqua Marble':"Aqua and purple marble with gold veins. Lighter than the tiles; the gold veins pick up the palm."},
'deco-mulberry':{
'Viola':"Your Mulberry pairing from October: a deep teal center for her teal bams, inside pink and plum florals on black that echo her backs.",
'Caroline in Peacock':"A peacock teal center in a frame of berry and magenta blooms: her back color and her teal bams, both at full strength.",
'Deco Dragon (Lagoon)':"Bam Bird Boutique's own Deco Dragon mat, in her sister color. Bam Bird shoots Mulberry tiles on it, and the gold palms glow against the teal.",
'Wren':"A deep teal center, a mulberry scalloped frame and a plum paisley border. All of her colors in one mat.",
'Spring Blooms Premium':"A teal center with plum, pink and gold flowers: the backs, the bams and the gold palm.",
'Tiger Fans':"Plum deco fans around a jewel-tone tiger tapestry. The fan shape is pure art deco, and the plum is her back. Sold on Etsy.",
'Peony Sociale Premium':"Deep teal with hot pink peonies; the pink sits right next to her berry backs.",
'Deco Neoprene':"Bam Bird Boutique's teal neoprene with gold deco corners, the plain sister of the Dragon mat.",
'Dark Teal Cocktail Hour':"A dark teal solid with a fine gold border. Simple, so the berry backs do the talking.",
'Jade':"Oh My Mahjong's deep teal and blue botanical. The berry backs pop right off it.",
'Emerald Cove Mat':"Dark teal-green watercolor with a mint edge. Moody, jewel-toned, and the opposite of berry.",
'Evergreen':"Deep teal with ferns and a gold fretwork corner.",
'Year of the Snake':"A deep teal ground with a pink frame; the pink bridges the teal and her berry.",
'Mahj In Bloom Mat':"Deep teal with lilac and pink roses: berry-adjacent flowers on her teal.",
'The Mariner':"Teal marbled paper around a deep green center. Old-library deco.",
'Pretty in Plum Premium':"Plum, lilac and ivory with a scalloped center: her back color, softened.",
'Fall Fling Mat':"Black with pink, plum and sage flowers. The plum ties in her backs.",
'Flourish Neoprene':"Plum and magenta florals around a slate center.",
'Regal Bloom Neoprene':"A lilac center with a tiger, framed in dark plum florals.",
'Mulberry and Sage':"Mulberry stripes around a sage center, and the same name. The sage keeps it from being berry on berry.",
'Garden Party – Mulberry':"My Fair Mahjong's mulberry center with a teal edge: her back color plus her bams.",
'YOTD Raspberry':"Raspberry with pink roses and a blue-teal dragon that could be her green dragon's cousin.",
'Burgundy Grove':"A wine center inside an ivory floral frame. Close to her back, a little warmer.",
'Gilded Peacock':"Art deco gold lines and peacock feathers on deep teal: deco on deco.",
'Hawthorne':"A plum center with a navy and gold border: her berry back with her navy dots.",
'Crown Jewels':"Navy with jewel-tone blooms and gold lines.",
'Peacock Flair':"A deep purple circle with teal peacock feathers. The purple runs a little cooler than her berry.",
'Purple & Aqua Marble':"Purple and aqua marble with gold veins.",
'Plum Scallop':"Ivory with a plum scalloped border. Clean, and it lets the tiles shine.",
'Petals After Dark':"Black with teal and pink petals: her teal bams and berry backs on a night sky."}}
G={'deco-lagoon':{'top':'Top three','best':'Among the best','teal':'Deep teal + berry','deco':'Art deco, like her','peacock':'Peacocks + night gardens','contrast':'Her mulberry, on the mat','bright':'Brighter, still two colors'},
   'deco-mulberry':{'top':'Top three','best':'Among the best','teal':'Deep teal, so the berry pops','berry':'Berry + a teal accent','jewel':'Jewel box','quiet':'Quiet + clean'}}
import re
for s,L in p.items():
    mats=[]
    for c in L:
        nm=re.sub(r'\s*\(retired\)','',c['name'])
        mats.append(dict(group=c['group'],name=nm,brand=c['brand'],img=mf[c['key']]['file'],why=W[s][nm],retired=bool(c['rt']),fym=c['key'],lowres=nm in LOWRES))
    json.dump({'_note':f"{s} album DRAFT (Nov 7): Claude's own picks, Tiffany's Nov 7 7:03pm ask ('You take them, just like you did this one'). Groups in order; 'lowres' = best photo we have is under ~800px.",'groups':G[s],'mats':mats},open(R+f'scripts/albumcard/specs/{s}_nov07.json','w'),indent=1,ensure_ascii=False)
    print(s,len(mats))
