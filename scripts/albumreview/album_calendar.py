#!/usr/bin/env python3
"""ALBUM CALENDAR (Tiffany Nov 11 2:27pm): the album queue as a visual week-by-week calendar, each album with its tile
photo and a readiness strip that is COMPUTED, never ticked by hand.

Readiness steps = Album Playbook (artifact 14oGH3ovycd2xMgrHbodJZ) + the Nov 10 said-vs-done audit (album rows):
  tile      her OK on the tile photo            record tile_photo.approved_at (asked_at = waiting on her)
  fym       tiles set up in Find Your Mat-ch     album_gate [1]
  colour    colour card                          album_gate [2]
  research  Facebook groups searched             album_gate [3] + [3b]
  discover  mat discovery                        album_gate [3c]
  cards     cards built (pool, by-sight, holiday, order, faces, cards, sharp)   album_gate [4]..[8b]
  review    review page sent to her              record review_url
  answered  her answers applied                  record rounds[*].applied_at
  bringins  every bring-in paid + catalogued     album_gate --golive [10b]
  week      launch week set                      config/album-launch-slots.json
  kit       launch kit in Planoly                record launch_kit.planoly_group_ids (each id must exist in Planoly)
  email     new-album email drafted              record email.campaign_id
  live      live page + announced                live page answers 200
Usage: album_calendar.py [out.html]   (default site/livepatch/album-calendar/album-calendar.html)"""
import json, os, re, sys, subprocess, base64, io, datetime, hashlib, html as H
R = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + '/'
OUT = sys.argv[1] if len(sys.argv) > 1 else R + 'site/livepatch/album-calendar/album-calendar.html'
Q = json.load(open(R + 'config/album-queue.json'))['albums']
SLOTS = json.load(open(R + 'config/album-launch-slots.json'))['slots']
CACHE = R + 'site/livepatch/album-calendar/img/'; os.makedirs(CACHE, exist_ok=True)
from PIL import Image

def thumb(src):
    key = hashlib.md5(src.encode()).hexdigest()[:12]; p = CACHE + key + '.jpg'
    if not os.path.exists(p):
        raw = None
        if src.startswith('http'):
            raw = subprocess.run(['curl', '-sL', '--max-time', '25', src + ('&' if '?' in src else '?') + 'width=500'], capture_output=True).stdout
        elif os.path.exists(R + src):
            raw = open(R + src, 'rb').read()
        if not raw: return ''
        try:
            im = Image.open(io.BytesIO(raw)).convert('RGB'); im.thumbnail((420, 420)); im.save(p, 'JPEG', quality=80)
        except Exception: return ''
    return 'data:image/jpeg;base64,' + base64.b64encode(open(p, 'rb').read()).decode()

STEPS = [('tile', 'Tile photo OK'), ('fym', 'Tiles in FYM'), ('colour', 'Colour card'), ('research', 'FB groups searched'),
         ('discover', 'Mat discovery'), ('cards', 'Cards built'), ('review', 'Review page sent'), ('answered', 'Your answers in'),
         ('bringins', 'Bring-ins paid'), ('week', 'Launch week set'), ('carousel', 'Catalog carousel in Planoly'),
         ('share', "It's a mat-ch! share card"), ('reel', 'Canva reel built (folder + music ideas)'), ('email', 'Email drafted'),
         ('finish', 'You finish the reel + Duet checks'), ('live', 'Live + announced')]

def gate(slug, golive=False):
    r = subprocess.run(['python3', R + 'scripts/checks/album_gate.py', slug] + (['--golive'] if golive else []), capture_output=True, text=True)
    return set(re.findall(r'^\s*\[(\w+)\]', r.stdout, re.M)), r.stdout

LIVE_CACHE = {}
def live(slug):
    if slug in LIVE_CACHE: return LIVE_CACHE[slug]
    code = subprocess.run(['curl', '-s', '-o', '/dev/null', '-w', '%{http_code}', '--max-time', '20',
                           f'https://www.mahjmatchmaker.com/{slug}-mahjong-tile-matches'], capture_output=True, text=True).stdout
    LIVE_CACHE[slug] = code == '200'; return LIVE_CACHE[slug]

def readiness(a):
    s = {k: 'todo' for k, _ in STEPS}; slug = a['slug']; rp = R + f'config/album-records/{slug}.json'
    if slug in SLOTS: s['week'] = 'done'
    elif a.get('week'): s['week'] = 'proposed'
    if live(slug): s['live'] = 'done'
    if not os.path.exists(rp): return s, False
    rec = json.load(open(rp)); fails, _ = gate(slug)
    tp = rec.get('tile_photo') or {}
    s['tile'] = 'done' if tp.get('approved_at') else ('waiting' if tp.get('asked_at') else 'todo')
    s['fym'] = 'todo' if '1' in fails else 'done'
    s['colour'] = 'todo' if '2' in fails else 'done'
    s['research'] = 'todo' if fails & {'3', '3b'} else 'done'
    s['discover'] = 'todo' if '3c' in fails else 'done'
    s['cards'] = 'todo' if fails & {'4', '4a', '4b', '5', '6', '7', '8', '8b'} else 'done'
    s['review'] = 'done' if rec.get('review_url') else 'todo'
    rounds = rec.get('rounds') or []
    s['answered'] = 'done' if any(r.get('applied_at') for r in rounds) else ('waiting' if rec.get('review_url') else 'todo')
    if s['cards'] == 'done':
        gf, _ = gate(slug, True); s['bringins'] = 'todo' if '10b' in gf else 'done'
    kit = rec.get('launch_kit') or {}
    s['carousel'] = 'done' if kit.get('carousel_planoly_id') else 'todo'
    s['share'] = 'done' if kit.get('share_card_planoly_id') else 'todo'
    s['reel'] = 'done' if kit.get('canva_reel_id') and kit.get('canva_folder_id') and kit.get('music_ideas') else 'todo'
    s['finish'] = 'done' if (kit.get('reel_finished_at') and kit.get('duet_checked_at')) else ('waiting' if s['reel'] == 'done' else 'todo')
    s['email'] = 'done' if (rec.get('email') or {}).get('campaign_id') else 'todo'
    return s, True

def weeklabel(d):
    d = datetime.date.fromisoformat(d); n = (d.day - 1) // 7 + 1
    return d.strftime('%b') + f' · week {n}', d.strftime('%b %-d')

cards = []
for a in Q:
    st, has_rec = readiness(a); a['_st'] = st; a['_rec'] = has_rec; a['_img'] = thumb(a['img']) if a.get('img') else ''
done_n = lambda st: sum(v == 'done' for v in st.values())

def card(a):
    st = a['_st']; pills = ''.join(
        f'<li class="st {st[k]}" title="{H.escape(lbl)}: {st[k]}"><span class="dot"></span>{H.escape(lbl)}</li>' for k, lbl in STEPS)
    nxt = next((lbl for k, lbl in STEPS if st[k] in ('todo', 'waiting', 'proposed')), 'Ready')
    wk = ''
    if a.get('week'):
        lab, day = weeklabel(a['week']); wk = f'<div class="wk">{lab} <span>Mon {day}</span>{"<em>proposed</em>" if a.get("proposed") and a["slug"] not in SLOTS else ""}</div>'
    note = f'<p class="note">{H.escape(a["note"])}</p>' if a.get('note') else ''
    img = f'<img src="{a["_img"]}" alt="{H.escape(a["name"])} tiles" loading="lazy">' if a['_img'] else '<div class="noimg">no photo yet</div>'
    return f'''<article class="alb"><div class="ph">{img}</div><div class="bd">{wk}<h3>{H.escape(a["name"])}</h3><p class="br">{H.escape(a["brand"])}</p>
<p class="why">{H.escape(a["why"])}</p>{note}<div class="prog"><b>{done_n(st)}/{len(STEPS)}</b> ready · next: <strong>{H.escape(nxt)}</strong>{"" if a["_rec"] else " · not started"}</div>
<details open><summary>Readiness</summary><ul class="steps">{pills}</ul></details></div></article>'''

sched = sorted([a for a in Q if a.get('week')], key=lambda a: a['week']); later = [a for a in Q if not a.get('week')]
months = {}
for a in sched: months.setdefault(datetime.date.fromisoformat(a['week']).strftime('%B %Y'), []).append(a)
body = ''.join(f'<section class="month"><h2>{m}</h2><div class="grid">{"".join(card(a) for a in v)}</div></section>' for m, v in months.items())
body += f'<section class="month"><h2>Queue, no week yet</h2><div class="grid">{"".join(card(a) for a in later)}</div></section>'
now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=-5))).strftime('%a %b %-d, %-I:%M %p ET')
legend = ''.join(f'<li class="st {k}"><span class="dot"></span>{t}</li>' for k, t in (('done', 'done (proven)'), ('waiting', 'waiting on you'), ('proposed', 'week proposed'), ('todo', 'not done')))
page = f'''<title>Album Calendar</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,600;1,500&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<style>
:root{{--bg:#fbf7f4;--card:#fff;--ink:#2a2226;--mute:#7a6e72;--line:#eadfe1;--accent:#c2457a;--done:#3f8f5e;--wait:#d08a1e;--prop:#7a6fd0;--todo:#d9cfd2;color-scheme:light}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#1b1719;--card:#262022;--ink:#f3ecee;--mute:#b3a6aa;--line:#3a3135;--accent:#e57aa6;--done:#5fc185;--wait:#f0aa45;--prop:#a79ef0;--todo:#4b4044;color-scheme:dark}}}}
:root[data-theme="dark"]{{--bg:#1b1719;--card:#262022;--ink:#f3ecee;--mute:#b3a6aa;--line:#3a3135;--accent:#e57aa6;--done:#5fc185;--wait:#f0aa45;--prop:#a79ef0;--todo:#4b4044;color-scheme:dark}}
body{{background:var(--bg);color:var(--ink);font:15px/1.5 Inter,system-ui,sans-serif;padding-block:20px 48px;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}}
.wrap{{max-width:1180px;margin:0 auto}}
h1{{font:600 clamp(28px,5vw,40px)/1.1 "Playfair Display",Georgia,serif;margin:0 0 6px;text-wrap:balance}}
.sub{{color:var(--mute);margin:0 0 14px;max-width:70ch}}
.legend{{display:flex;flex-wrap:wrap;gap:6px 16px;list-style:none;padding:0;margin:0 0 8px;font-size:13px}}
h2{{font:500 italic 24px "Playfair Display",Georgia,serif;margin:30px 0 12px;border-bottom:1px solid var(--line);padding-bottom:6px}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:16px}}
.alb{{background:var(--card);border:1px solid var(--line);border-radius:14px;overflow:hidden;display:flex;flex-direction:column;min-width:0}}
.ph{{aspect-ratio:4/3;background:var(--line);display:grid;place-items:center;max-width:100%;overflow:hidden;position:relative}} .ph img{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;display:block}}
.noimg{{color:var(--mute);font-size:13px}}
.bd{{padding:12px 14px 14px;display:flex;flex-direction:column;gap:4px;min-width:0}}
.wk{{font-size:12px;letter-spacing:.06em;text-transform:uppercase;color:var(--accent);font-weight:600;display:flex;gap:8px;align-items:baseline;flex-wrap:wrap}}
.wk span{{color:var(--mute);font-weight:500}} .wk em{{font-style:normal;background:color-mix(in srgb,var(--prop) 18%,transparent);color:var(--prop);border-radius:99px;padding:0 8px;letter-spacing:.03em}}
h3{{margin:2px 0 0;font:600 19px/1.25 "Playfair Display",Georgia,serif}}
.br{{margin:0;color:var(--mute);font-size:13px}} .why{{margin:4px 0 0;font-size:14px}}
.note{{margin:4px 0 0;font-size:13px;background:color-mix(in srgb,var(--wait) 14%,transparent);border-radius:8px;padding:6px 8px}}
.prog{{margin-top:6px;font-size:13px;color:var(--mute)}} .prog b{{color:var(--ink)}} .prog strong{{color:var(--ink);font-weight:600}}
details{{margin-top:4px;font-size:13px}} summary{{cursor:pointer;color:var(--accent);font-weight:500}}
.steps{{list-style:none;padding:0;margin:8px 0 0;display:grid;gap:3px}}
.st{{display:flex;align-items:center;gap:8px}} .dot{{width:10px;height:10px;border-radius:50%;background:var(--todo);flex:none}}
.st.done .dot{{background:var(--done)}} .st.waiting .dot{{background:var(--wait)}} .st.proposed .dot{{background:var(--prop)}}
.st.todo{{color:var(--mute)}}
.foot{{margin-top:36px;color:var(--mute);font-size:13px;max-width:75ch}}
</style>
<div class="wrap">
<h1>Album Calendar</h1>
<p class="sub">One album a week. Each card's readiness is checked automatically from the album's own files, the album gates and the live site, so a step only turns green when the work actually exists. Weeks marked <em>proposed</em> are my suggestion until you OK them. Updated {now}.</p>
<ul class="legend">{legend}</ul>
{body}
<p class="foot">Steps follow the Album Playbook: tile photo OK, tiles in Find Your Mat-ch, colour card, Facebook groups searched, mat discovery, cards built, review page, your answers, bring-ins paid, launch week, catalog carousel, It's a mat-ch! share card, Canva reel, email, then the last step: you finish the reel while Duet checks everything, then live + announced. Nothing goes live before its week, and never without its launch kit.</p>
</div>'''
os.makedirs(os.path.dirname(OUT), exist_ok=True); open(OUT, 'w').write(page)
print('wrote', OUT, len(page) // 1024, 'KB;', len(Q), 'albums')
for a in Q: print(f"  {a['slug']:28} {done_n(a['_st'])}/{len(STEPS)} img={'y' if a['_img'] else 'N'}")
