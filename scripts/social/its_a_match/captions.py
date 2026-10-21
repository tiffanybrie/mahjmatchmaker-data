"""Build assets/social/its-a-match/reference-picks.json: per-set 'It's a match' pick + caption draft (Oct 21).

REFERENCE ONLY (Tiffany, Oct 21 11:30): "It's a match" is the middle grid post of each set's launch row (doc 89),
not a standalone series. When a set's row is built, take its pick + caption from here, re-check the live album
(order and count can change) and render with render.py. Nothing here is scheduled or in Planoly.
Usage: python3 captions.py <picks.json> <skipped.json>
"""
import json, sys
R = '/home/claude/mahjmatchmaker-data'
picks = json.load(open(sys.argv[1])); skipped = json.load(open(sys.argv[2]))
TAGS = '#mahjong #mahjongmat #mahjongtiles #mahjmatchmaker #affiliate'
# one funny line per pair, about the pair (no colour theory)
LINE = {
 ('amara', 'Chinoiserie Songbird'): "If Amara is the Lilly Pulitzer of tiles, she just found her plus one for every garden party this season.",
 ('birdie', 'Chinoiserie Denim'): "A birdie and a songbird-worthy mat. She didn't even have to tweet first.",
 ('coquette', 'Martha & Mae Vintage Quilt'): "A bow girl meets a quilt girl. Grandma approves of this one.",
 ('cypress-forest', 'Knox'): "Cypress showed up in a quarter-zip and Knox didn't even blink. Strong silent types.",
 ('drake', 'Hunt Club'): "Drake has been to the Hunt Club exactly zero times but somehow knows everyone there.",
 ('emerald', 'Jardín de Los Jefes'): "Emerald walked into the garden and the garden said, finally.",
 ('gatsby', 'Hunt Club'): "Old money tiles meet an old money mat. Someone pour the Arnold Palmers.",
 ('gemma', 'Preppy Pink Garden'): "Gemma said she wanted someone preppy. She meant it.",
 ('glitterville', 'Jardín de Los Jefes'): "Glitterville brought the sparkle, the garden brought the snacks. Perfect party.",
 ('glow-wild', 'Lucky Charms Watercolor'): "Glow Wild got lucky. Like, actually lucky.",
 ('heritage-2-0', 'Hunt Club'): "Heritage 2.0 and the Hunt Club. He already owns the loafers.",
 ('heritage', 'Hydrangea Bliss'): "Turns out the classic guy has a soft spot for hydrangeas. Who knew.",
 ('jade', 'Pink Winds'): "Jade just wanted a pink mat that wouldn't play it safe. Done.",
 ('jasmine', 'Dahlia'): "Jasmine and Dahlia. Two flower girls, one table, zero drama.",
 ('la-fete', 'Posy Pop Watercolor'): "La Fete means party, and Posy Pop showed up with the flowers.",
 ('lagoon', 'Aria'): "Lagoon took one look at Aria and started planning the beach wedding.",
 ('limoncello', 'YOTD Raspberry'): "Limoncello and raspberry. That's not a mahj table, that's dessert.",
 ('lola', 'Chinoiserie Denim'): "Lola in denim is a whole mood. Casual Friday, but make it mahj.",
 ('luminaire', 'Secret Garden'): "Luminaire found the Secret Garden. Don't tell anyone where it is.",
 ('malachite', 'Petalwood'): "Malachite, the strong green type, falls for a floral. Classic.",
 ('moonlight', 'Cottage Bloom'): "Moonlight in the cottage garden. Somebody light a candle.",
 ('nantucket', 'Handbook Plaid'): "Nantucket in plaid. She packed for the ferry and the club.",
 ('palm-royale', 'French Mural'): "Palm Royale took a trip to France and came back with a mural.",
 ('papaya-spritz', 'Heiress'): "A party girl tile meets a party girl mat, one of my favorite matches for her!",
 ('pearlescent', 'Rally in Pink'): "Pearls and pink, for a good cause. Pearlescent said yes before the question.",
 ('pippa', 'Fruit Stand'): "Pippa showed up with snacks. Game over.",
 ('seabreeze', 'Aria'): "Seabreeze and Aria. Windows down, playlist on, mahj at 2.",
 ('sierra', 'Nantucket Basket'): "Sierra brought the basket. Sierra always brings the basket.",
 ('smith', 'Hunt Club'): "Smith owns six navy quarter-zips and the Hunt Club approves of all of them.",
 ('solara', 'Chinoiserie Elephant'): "Solara and the elephant. Big personality, bigger table presence.",
 ('sorbet', 'Posy Pop Watercolor'): "Sorbet and a bouquet. That's the whole summer, right there.",
 ('sunset', 'Cheetah Couture'): "Sunset in cheetah print. She's going out out.",
 ('talulah', 'Viola'): "Talulah and Viola. That's a garden club with a waitlist.",
 ('tortoise', 'Elysium'): "Tortoise has been slow and steady with her matches. Elysium was worth the wait.",
 ('willow', 'Hunt Club'): "Willow went to the Hunt Club for the scenery. Stayed for the mat.",
 ('heritage-2-0', 'Spring Awakening W'): "He's a classic guy, but even classic guys need a spring awakening.",
 ('heritage', 'YOTD White'): "Heritage in crisp white. He irons his pocket squares.",
 ('coquette', 'Parrotia'): "Coquette and Parrotia. Bows meet birds and the whole table chirps.",
 ('papaya-spritz', 'Press for Mahjong'): "She pressed the button. Papaya Spritz, party of four.",
 ('gatsby', 'Spring Awakening Warm Honey'): "Gatsby throws the party, Warm Honey sets the table.",
 ('willow', 'Hydrangea Bliss'): "Willow and hydrangeas. That's the porch in June.",
 ('drake', 'Vegan Leather'): "Drake in leather. Vegan, obviously. He's a gentleman.",
 ('lagoon', 'Pink Winds'): "Lagoon in pink. She's on vacation and the out of office is ON.",
 ('glow-wild', 'Aria'): "Glow Wild and Aria. She glows, Aria sings.",
 ('solara', 'Heiress'): "Solara met the Heiress and now she's in the will.",
}
out = []
for p in picks:
    who = 'him' if p['pron'] == 'his' else 'her'
    line = LINE.get((p['set'], p['mat']))
    tile_tag = '@' + p['tile_ig'] if p.get('tile_ig') else p['tile_brand']
    mat_tag = '@' + p['ig'] if p.get('ig') else p['mat_brand']
    cap = (f"It's a match! 💗 {line} {tile_tag} {p['tile']} + {p['mat']} by {mat_tag} 💕 "
           f"Who would you match {who} with? 👇 All {p['count']} of {p['pron']} matches are at the link in bio. "
           f"Code MAHJMATCH 💗\n\n{TAGS}")
    out.append({**{k: p[k] for k in ('rank', 'set', 'tile', 'tile_brand', 'tile_ig', 'tile_img', 'count', 'pron', 'order',
                                    'mat', 'mat_brand', 'ig', 'key', 'f', 'album_img')},
                'fym_mat_photo': 'FYM artifact 6epA9HuEdT32zUp79Qv3kd published file ' + p['f'],
                'handle_needed': None if p.get('ig') else f"{p['mat_brand']}: no verified IG handle in config/social/ig-handles.json",
                'caption': cap})
doc = {'_about': __doc__.strip().split('\n')[0] + ' Picks come only from the live album pages (Oct 21 11:15 snapshot), '
       'first partner, non-official-pair, non-retired, non-holiday, FYM-visible mat in her album order, preferring brands '
       'with a verified IG handle. rank 2 = second card for the 10 OMM sets with the most matches.',
       'status': 'REFERENCE ONLY, not rendered, not in Planoly (Tiffany Oct 21: It\'s a match = middle post of each set row, doc 89)',
       'cards': out, 'skipped': [{'set': s, 'why': w} for s, w in skipped]}
json.dump(doc, open(f'{R}/assets/social/its-a-match/reference-picks.json', 'w'), indent=1, ensure_ascii=False)
caps = {f"{c['set']}--{c['mat']}": c['caption'] for c in out}
json.dump(caps, open(f'{R}/assets/social/its-a-match/captions.json', 'w'), indent=1, ensure_ascii=False)
print(len(out), 'missing lines:', [k for k in caps if LINE.get(tuple(k.split('--'))) is None])
