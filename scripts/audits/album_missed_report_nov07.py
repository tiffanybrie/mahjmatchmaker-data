#!/usr/bin/env python3
"""Writes docs/audits/album-missed-mats-2026-11-07.{md,json} from the scored shortlist + the by-eye verdicts
(verdicts*.json: per album the shortlist numbers kept after LOOKING at the contact sheets, with a one-line why).
Usage: python3 scripts/audits/album_missed_report_nov07.py <shortlist.json> <verdicts1.json> [more verdicts...]"""
import json, os, sys
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
MOTIF = ('motif', 'dragon', 'chinoiserie', 'pagoda', 'palm', 'deco', 'Limoncello', 'lemons', 'nautical', 'fall')


def main(sl, *vfiles):
    S = json.load(open(sl)); V = {}
    for f in vfiles: V.update(json.load(open(f)))
    order = ['papaya-spritz'] + sorted(k for k in S if k != 'papaya-spritz')
    out = {'date': '2026-11-07', 'method': 'see doc', 'albums': {}}
    for slug in order:
        a = S[slug]; v = V.get(slug, {'keep': [], 'why': {}})
        rows = []
        for n in v['keep']:
            r = a['shortlist'][n - 1]; why = v['why'].get(str(n), '')
            kind = 'holiday' if r['hol'] or why.startswith('HOLIDAY') else (
                'colour + motif' if any(m.lower() in why.lower() for m in MOTIF) else 'colour')
            partner = 'partner (code)' if r['pa'] else ('non-partner, her ShopMy pick' if 'staged' in r['src'] or r['brand'] == 'Amazon'
                                                 else 'no partner code in FYM (allowed mat)')
            rows.append({'sheet_no': n, 'name': r['name'], 'brand': r['brand'], 'key': r['key'], 'url': r.get('url'),
                         'source': r['src'], 'kind': kind, 'partner': partner, 'why': why.replace('HOLIDAY: ', '').replace('HOLIDAY (Hanukkah): ', 'Hanukkah: '),
                         'score': r['score'], 'tier': (v.get('tier') or {}).get(str(n))})
        out['albums'][slug] = {'name': a['name'], 'built_cutoff': a['cutoff'], 'live_cards': a['album_cards'],
                               'never_seen_pool': a['never_seen_pool'], 'colour_qualified': a['qualified'],
                               'sheet': f'assets/qa/album-missed-nov07/{slug}.jpg', 'strong': rows,
                               'strong_count': len(rows), 'holiday_count': sum(1 for x in rows if x['kind'] == 'holiday')}
    A = out['albums']; tot = sum(x['strong_count'] for x in A.values()); hol = sum(x['holiday_count'] for x in A.values())
    staged = {(r['name'], r['brand']) for x in A.values() for r in x['strong'] if 'staged' in r['source']}
    big = sorted(A.items(), key=lambda kv: -(kv[1]['strong_count'] - kv[1]['holiday_count']))[:6]
    out['summary'] = {'albums': len(A), 'strong_total': tot, 'holiday': hol, 'year_round': tot - hol,
                      'distinct_staged_mats_in_lists': len(staged)}
    os.makedirs(os.path.join(R, 'docs/audits'), exist_ok=True)
    json.dump(out, open(os.path.join(R, 'docs/audits/album-missed-mats-2026-11-07.json'), 'w'), indent=1, ensure_ascii=False)
    L = ['# Album missed-mats audit (Nov 7, 2026)', '',
         f"**Summary.** {len(A)} live albums had **{tot} strong mats they never saw** ({tot - hol} year-round + {hol} holiday). "
         f"Every live album has at least {min(x['strong_count'] for x in A.values())}. The biggest year-round gaps: "
         + '; '.join(f"{x['name']} {x['strong_count'] - x['holiday_count']}" for _, x in big) + '. '
         "Almost all of it is catalog that arrived after the album was built: Let's Be Besties (Nov 1, 347 mats), the Oct 31 "
         "Bougie / Betty June & Jeannette / Luna EK / YOLO drops, Mahj & Moon Etsy pairings, plus new partner pieces (Bam Bird "
         "Deco Dragons + Pink on Pink plaid, Britt Mills leatherettes, PLM vegan leathers, Sunday vegan leathers, Anders Ruff). "
         f"{len(staged)} of the Nov 7 never-in-catalog ShopMy/Amazon mats made a list (Mahjong House Ruby Table, Rebecca Illustrated "
         "Canaries + White Sailboats, Case-Mate Ballet Pink, Amazon holiday tartans/snowflakes/Hanukkah). Papaya Spritz: "
         f"{A['papaya-spritz']['strong_count']} (Tiffany was right that it missed some, but its 50 cards already cover the obvious "
         "oranges; the misses are mostly newer patterned mats).", '',
         '**How.** Per album, never-considered = mats staged Nov 7 (config/fym-shopmy-nov07.json, config/fym-amazon-holiday-oct26.json) '
         '+ FYM v117 mats whose `add` tag is dated after the album was built (cutoff per album below; untagged original catalog counted '
         'as seen), minus anything already on the live album page or in its FYM match list, and minus hidden/retired/sold-out, Mahjong '
         'Studios, Paige Spearin, non-album Splash, travel/minis. Each was colour-scored against the set (measured back/signature/layer '
         'shades from config/tile-tones.json + colour-card faces, CIEDE2000, tone gate, clash penalty); top 12 year-round + top 4 holiday '
         'per album went on a contact sheet (mat full, album tiles inset), and only the ones that LOOK like a real match were kept. '
         'Motif only lifts a mat whose colours already fit (Nov 7 8:07pm). Holiday mats are listed for the holiday section only. '
         'Scripts: scripts/audits/album_missed_*_nov07.py. Sheets: assets/qa/album-missed-nov07/<album>.jpg.', '',
         '**Caveats.** Album build dates are estimates (most albums pre-date the Oct 16+ catalog growth, so for them every add-tagged mat '
         'is "never seen"). Malachite: config/tile-tones.json lists its back as blush (#d0b1b9); the album photo shows dark green malachite '
         'backs, so this audit used #445344 (fix the profile in tile-tones on her OK). Mats marked non-partner are allowed in FYM '
         '(nonpartner_allow) or are her ShopMy picks: shop link only, no code. 30 other Amazon pins in her ShopMy (not the 28 holiday '
         'picks) were not in scope. Nothing was added to any album: these are candidates for her yes/no.', '']
    for slug in order:
        x = A[slug]
        L += [f"## {x['name']}: {x['strong_count']} strong ({x['holiday_count']} holiday)",
              f"Built ~{x['built_cutoff']} · {x['live_cards']} cards live · {x['never_seen_pool']} mats it never saw, {x['colour_qualified']} colour-qualified · sheet `{x['sheet']}`", '']
        for r in x['strong']:
            tag = ' **[holiday]**' if r['kind'] == 'holiday' else ''
            L.append(f"- **{r['name']}** · {r['brand']} · {r['kind']} · {r['partner']}{tag}: {r['why']} _(#{r['sheet_no']}, {r['source']})_")
        L.append('')
    open(os.path.join(R, 'docs/audits/album-missed-mats-2026-11-07.md'), 'w').write('\n'.join(L))
    print(json.dumps(out['summary']), [(x['name'], x['strong_count']) for _, x in big])


if __name__ == '__main__':
    main(*sys.argv[1:])
