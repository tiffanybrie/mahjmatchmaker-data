"""Mahj Matchmaker customer emails (Oct 21, 2026): one source for the copy, the HTML previews and the screenshots.

Builds:
  templates/<id>.html   600px email-style HTML (navy/pink/cream, wordmark with tagline ribbon)
  shots/<id>.png        screenshot at 600px wide (what Tiffany approves in Ready to Ship)
  emails.json           subject / preview / body text per email (what goes into Squarespace)

Copy rules: docs/BRAND-GUIDE.md (Find *Your* Mat-ch(TM) with the TM once, code line "Use code MAHJMATCH to save 💕",
no %, no other code, no Amazon links, plain "match" elsewhere). Rules for sending: docs/EMAIL.md.

Run: python3 site/email/build.py            (html + json)
     python3 site/email/build.py shots      (also screenshots, needs playwright)
"""
import json, pathlib, sys, html, re

ROOT = pathlib.Path(__file__).resolve().parent
SITE = "https://www.mahjmatchmaker.com"
NAVY, DEEP, PINK, HPINK, BLUSH, CREAM, PCREAM = "#054689", "#062a55", "#d6336c", "#f56c8c", "#fbe3ea", "#faf3ea", "#fffdfa"

FYM_HTML = 'Find&nbsp;<em>Your</em> Mat&#8209;ch&trade;'  # non-breaking hyphen: never wraps as Mat- / ch
FYM = 'Find <em>Your</em> Mat-ch'
CODE = 'Use code <b>MAHJMATCH</b> to save 💕'
SIGN = 'Happy mat-ching!<br>xo, Tiffany'
FEEDBACK = f'{SITE}/find-your-mat-ch-feedback'  # hidden page, form notifications -> mahjmatchmaker@gmail.com, Gmail label Site/FYM feedback (Claude handles)
CDN_IMG = 'https://cdn.jsdelivr.net/gh/tiffanybrie/mahjmatchmaker-data@570b99d18977107da6b3be40487d010a95b65171/site/email/assets/fym/' if 'cdn' in sys.argv else ''  # 'cdn' arg = pinned jsDelivr srcs for Squarespace; set to the pinned jsDelivr folder for Squarespace; empty = local relative paths for previews

EMAILS = [
    {
        "id": "launch",
        "name": "Launch: Find Your Mat-ch is here",
        "kind": "campaign",
        "when": "Tue Oct 27, 9:30am CT, one send",
        "to": "All subscribers (homepage signup, notify-me form and form subscribers all land there)",
        "subject": "It's here! Find Your Mat-ch is live 💕",
        "preview": "Pick your tiles, swipe your mats, meet your match.",
        "h1img": "hl-launch-h1",
        "paras": [
            f'This is a new tool I&rsquo;m rolling out just for you: <b>{FYM_HTML}</b>. This time I&rsquo;m stepping out of the matchmaker seat, and it&rsquo;s your turn to find your match.',
            'My picks are baked right in, so you&rsquo;re never swiping alone.',
        ],
        "steps_head": "hl-launch-how",
        "tutorial": True,  # 5 annotated steps from scripts/fym_promo/tutorial.json (render2.py)
        "button": ("Start swiping", f"{SITE}/find-your-match"),
        "after": [
            'Hope you love it!',
            f'Something look off or have an idea? <a href="{FEEDBACK}">Tell me here &rarr;</a>',
            CODE,
        ],
    },
    {
        "id": "welcome",
        "name": "Automation: Welcome (new subscriber)",
        "kind": "automation",
        "when": "right after someone signs up (on from launch)",
        "to": "each new subscriber",
        "subject": "Welcome to Mahj Matchmaker! 💕",
        "preview": "Three fun places to start, plus a few of my favorite reads.",
        "h1img": "hl-welcome-h1",
        "paras": [
            'I&rsquo;m so glad you&rsquo;re here! I match mahjong tiles with the mats and racks that make them shine, so your table comes together just the way you dreamed.',
        ],
        "list_head": "hl-welcome-start",
        "list": [
            f'<a href="{SITE}/find-your-match">{FYM_HTML}</a>: start with your tiles or your mat and swipe, with my picks built right in.',
            f'<a href="{SITE}/mahjong-tile-matches">My tile set albums</a>: a match card for every mat and rack I&rsquo;ve paired with each set.',
            f'<a href="{SITE}/mahjong-discount-codes">The discount codes page</a>: every partner brand that takes our code.',
        ],
        "button": ("Start swiping", f"{SITE}/find-your-match"),
        "blog": [
            ("The Mahjong Buying Guide", "How to choose tiles, mats and racks", f"{SITE}/blog/mahjong-buying-guide"),
            ("The Most Versatile Mahjong Mats", "The mats that go with almost everything", f"{SITE}/blog/most-versatile-mahjong-mats"),
            ("A Holiday Table Without a Christmas&nbsp;Mat", "Festive tables with the mat you already own", f"{SITE}/blog/holiday-mahjong-table"),
        ],
        "after": [
            f'Have an IRL photo of your table you&rsquo;d love to share with the Mahj Matchmaker community? <a href="{SITE}/share-your-table">Submit it here</a>, or join our <a href="https://www.facebook.com/groups/mahjmatchmaker">Facebook group</a> and share it there. We often pull photos from the group to feature in the tile albums!',
            CODE,
        ],
    },
    {
        "id": "album-request",
        "name": "Automation: Album request thank-you",
        "kind": "automation",
        "when": "right after someone submits Request an Album",
        "to": "the person who sent the request",
        "subject": "Got it! Your album request is in 💕",
        "preview": "The most-asked-for sets get matched first.",
        "h1img": "hl-request-h1",
        "paras": [
            'I keep a running tally of every request, and the most-asked-for sets get matched first. When yours goes live, you&rsquo;ll be the first to know.',
            f'While you wait, try <b>{FYM_HTML}</b> to see the mats and racks I&rsquo;d pair with your set. Don&rsquo;t see your set in the catalog yet? Shop by color and pick a similar colorway, and you&rsquo;ll find plenty of matches to swoon over.',
        ],
        "button": ("Start swiping", f"{SITE}/find-your-match"),
        "after": [CODE],
    },
    {
        "id": "album-exists",
        "name": "Automation: It's already in our library",
        "kind": "manual-reply",
        "when": "sent by Claude when a requested set already has an album",
        "to": "the person who sent the request",
        "subject": "Good news, it's already in our library!",
        "preview": "Your set already has an album, right this way.",
        "h1img": "hl-exists-h1",
        "paras": [
            '<b>[Tile set]</b> already has an album, packed with the mats and racks I&rsquo;d pair with it.',
        ],
        "button": ("See the album", f"{SITE}/mahjong-tile-matches"),
        "after": [CODE],
    },
    {
        "id": "album-live",
        "name": "Automation: Your album is live",
        "kind": "manual-reply",
        "when": "sent by Claude when a requested album goes live",
        "to": "everyone who requested that set",
        "subject": "Your [tile set] matches are here! 🎉",
        "preview": "You asked, I matched!",
        "h1img": "hl-live-h1",
        "paras": [
            'The <b>[Tile set]</b> album is live, with all the mats and racks I&rsquo;d pair with it.',
        ],
        "button": ("See your matches", f"{SITE}/mahjong-tile-matches"),
        "after": [CODE],
    },
]

CSS = f"""
body{{margin:0;background:{BLUSH};font-family:Georgia,'Times New Roman',serif;color:{DEEP}}}
.outer{{padding:24px 12px}}
.card{{max-width:600px;margin:0 auto;background:{PCREAM};border-radius:18px;overflow:hidden}}
.top{{background:{CREAM};text-align:center;padding:26px 24px 18px}}
.top img{{width:300px;max-width:80%;height:auto}}
.meta{{max-width:600px;margin:0 auto 10px;font:13px/1.4 -apple-system,Helvetica,Arial,sans-serif;color:{DEEP}}}
.meta b{{color:{PINK}}}
.body{{padding:8px 34px 30px;font:17px/1.55 Georgia,'Times New Roman',serif}}
.pill{{display:inline-block;background:{NAVY};color:#fff;font:700 12px/1 Helvetica,Arial,sans-serif;letter-spacing:.16em;padding:9px 16px;border-radius:999px;margin:14px 0 4px}}
h1{{font:400 38px/1.15 Georgia,serif;color:{PINK};margin:12px 0 10px}}
h1 em,p em,li em{{font-style:italic}}
p{{margin:0 0 14px}}
a{{color:{PINK}}}
.h1{{margin:18px 0 14px}} .h2{{margin:26px 0 6px}} .h3{{margin:0 0 10px}}
.hero{{margin:4px 0 14px}}
.step{{text-align:center;margin:22px 0 8px;padding:18px 14px 6px;background:{PCREAM};border:2px solid #f4e3d6;border-radius:16px}} .step p{{margin:10px auto 8px;max-width:420px}}
.legal{{opacity:.8}}
.btnw{{text-align:center;margin:22px 0 22px}}
.btn{{display:inline-block;background:{HPINK};color:#fff!important;text-decoration:none;font:700 21px/1 Helvetica,Arial,sans-serif;padding:20px 46px;border-radius:14px}}
ul{{padding-left:20px;margin:0 0 14px}} li{{margin:0 0 8px}}
.code{{text-align:center;font-size:18px;background:{CREAM};border-radius:12px;padding:12px}}
.blog{{border-top:1px solid #eadfce;margin-top:8px;padding-top:14px}}
.blog h2{{font:700 13px/1 Helvetica,Arial,sans-serif;letter-spacing:.16em;color:{NAVY};margin:0 0 10px}}
.post{{display:block;background:#fff;border-radius:12px;padding:12px 14px;margin:0 0 8px;text-decoration:none}}
.post b{{display:block;color:{DEEP};font-size:16px}} .post span{{color:{PINK};font-size:14px}}
.sign{{font-size:19px;color:{NAVY};margin-top:18px}}
.foot{{background:{DEEP};color:{BLUSH};text-align:center;font:12px/1.6 Helvetica,Arial,sans-serif;padding:16px 20px}}
.foot a{{color:{BLUSH}}}
"""


def nw(p):
    """No widows: glue the last two words of a paragraph (brand guide: no orphan words)."""
    import re
    m = re.search(r" (?=[^ <>]+(?:<[^>]+>)*[^ <>]*$)", p)
    return p[:m.start()] + "&nbsp;" + p[m.end():] if m else p


ASSETS = ROOT / "assets" / "fym"
MANI = json.loads((ASSETS / "manifest.json").read_text())  # alt text + pixel sizes, written by scripts/fym_promo/render.py
TUT = json.loads((ROOT.parent.parent / "scripts" / "fym_promo" / "tutorial.json").read_text())  # render2.py
for _t in TUT:
    MANI["sizes"][f"tut{_t['n']}.jpg"] = _t["email"]; MANI["alt"][f"tut{_t['n']}"] = _t.get("email_alt", _t["alt"])
    MANI["sizes"][f"hl-tut{_t['n']}.png"] = _t["hl"]; MANI["alt"][f"hl-tut{_t['n']}"] = f"Step {_t['n']}: " + html.unescape(_t["title"])


def img(stem, cls="", display_w=None):
    """Brand headline / app image. 2x files, shown at half width (or display_w). Every image carries descriptive alt text."""
    f = next(k for k in MANI["sizes"] if k.rsplit(".", 1)[0] == stem)
    w, hgt, _ = MANI["sizes"][f]
    dw = display_w or w // 2
    dh = round(hgt * dw / w)
    src = (CDN_IMG + f) if CDN_IMG else f"../assets/fym/{f}"
    return (f'<img class="{cls}" src="{src}" width="{dw}" height="{dh}" '
            f'alt="{html.escape(MANI["alt"][stem])}" style="display:block;margin:0 auto;max-width:100%;height:auto">')


def heading_text(e):
    return MANI["alt"][e["h1img"]] if e.get("h1img") else re.sub(r"<[^>]+>", "", e.get("h1", ""))


def render(e, with_meta=True):
    h = []
    if with_meta:
        h.append(f'<div class="meta"><b>Subject:</b> {html.escape(e["subject"])}<br><b>Preview:</b> {html.escape(e["preview"])}<br><b>When:</b> {html.escape(e["when"])}</div>')
    h.append('<div class="card"><div class="top"><img src="../../../assets/brand/mahjmatchmaker-wordmark.png" alt="Mahj Matchmaker: matching mahjong tiles, mats &amp; racks"></div><div class="body">')
    h.append(f'<div class="h1">{img(e["h1img"])}</div>')
    if e.get("hero"):
        h.append(f'<div class="hero">{img(e["hero"], display_w=480)}</div>')
    for p in e["paras"]:
        h.append(f"<p>{nw(p)}</p>")
    if e.get("tutorial"):
        h.append(f'<div class="h2">{img(e["steps_head"])}</div>')
        for t in TUT:
            n = t["n"]
            h.append(f'<div class="step"><div class="h3">{img(f"hl-tut{n}")}</div><p>{nw(t["caption"])}</p>{img(f"tut{n}", "shot", 480)}</div>')
    if e.get("list"):
        h.append(f'<div class="h2">{img(e["list_head"])}</div>')
        h.append("<ul>" + "".join(f"<li>{x}</li>" for x in e["list"]) + "</ul>")
    t, u = e["button"]
    h.append(f'<div class="btnw"><a class="btn" href="{u}">{t}</a></div>')
    if e.get("blog"):
        h.append(f'<div class="blog"><div class="h2">{img("hl-welcome-reads")}</div>' + "".join(
            f'<a class="post" href="{u}"><b>{a}</b><span>{b} &rarr;</span></a>' for a, b, u in e["blog"]) + "</div>")
    for p in e.get("after", []):
        cls = ' class="code"' if p == CODE else ""
        h.append(f"<p{cls}>{nw(p)}</p>")
    h.append(f'<p class="sign">{SIGN}</p></div>')
    h.append('<div class="foot">Mahj Matchmaker · <a href="https://www.mahjmatchmaker.com">mahjmatchmaker.com</a><br>Hooking up tiles, mats &amp; racks'
             '<br><span class="legal">[Mailing address: pending from Tiffany] · <a href="#">Unsubscribe</a> (Squarespace adds both to every send)</span></div></div>')
    return f'<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(e["name"])}</title><style>{CSS}</style></head><body><div class="outer">{"".join(h)}</div></body></html>'


def plain(e):
    def t(s):
        s = re.sub(r'<a href="([^"]+)">([^<]+)</a>', r'\2 (\1)', s)
        s = re.sub(r"<[^>]+>", "", s)
        return html.unescape(s)
    out = [f'[IMAGE heading: {heading_text(e)}]']
    if e.get("hero"):
        out.append(f'[IMAGE: {MANI["alt"]["hero"]}]')
    out += [t(p) for p in e["paras"]]
    if e.get("tutorial"):
        out.append(f'[IMAGE heading: {MANI["alt"][e["steps_head"]]}]')
        for x in TUT:
            out.append(f'[IMAGE heading: {MANI["alt"]["hl-tut" + str(x["n"])]}]\n{t(x["caption"])}\n[IMAGE: {x.get("email_alt", x["alt"])}]')
    if e.get("list"):
        out.append(f'[IMAGE heading: {MANI["alt"][e["list_head"]]}]')
        out += ["• " + t(x) for x in e["list"]]
    out.append(f'[BUTTON: {e["button"][0]} → {e["button"][1]}]')
    if e.get("blog"):
        out.append(f'[IMAGE heading: {MANI["alt"]["hl-welcome-reads"]}]')
        out += [f"• {a}: {b} ({u})" for a, b, u in e["blog"]]
    out += [t(p) for p in e.get("after", [])]
    out.append("Happy mat-ching!\nxo, Tiffany")
    out = [o.replace("\u2011", "-").replace("\xa0", " ") for o in out]
    return "\n\n".join(out)


def stats(e):
    """Deliverability numbers: live words vs images, image weight."""
    body = render(e, with_meta=False)
    stems = set(re.findall(r'assets/fym/([\w-]+\.\w+)', body))
    kb = sum(MANI["sizes"][f][2] for f in stems) / 1024 + 35  # + wordmark logo
    words = len(re.sub(r"<[^>]+>", " ", re.sub(r"<style.*?</style>|<title>.*?</title>|<div class=\"foot\">.*", "", body, flags=re.S)).split())
    return {"images": len(stems) + 1, "image_kb": round(kb), "live_words": words}


def lint():
    bad = []
    for e in EMAILS:
        s = json.dumps(e) + render(e)
        for w in ["TEACHMAHJ", "%", "amazon.", "amzn", "®", "Find Your Match", "Happy Mat-ching"]:
            if w in s.replace("100%", ""):
                if w == "%" and "%" not in plain(e) + e["subject"]:
                    continue
                bad.append((e["id"], w))
        body = render(e, with_meta=False)
        if body.count("&trade;") + body.count("™") > 1:  # one body use at most (subject may carry its own)
            bad.append((e["id"], "TM used more than once in body"))
        if e["subject"].count("!") > 1:
            bad.append((e["id"], "subject: one ! at most"))
        if re.search(r"\b[A-Z]{4,}\b", e["subject"].replace("MAHJMATCH", "")):
            bad.append((e["id"], "subject: no ALL CAPS"))
        for m in re.finditer(r"<img [^>]*>", body):
            if 'alt="' not in m.group(0) or 'alt=""' in m.group(0):
                bad.append((e["id"], "image without alt text"))
        st = stats(e)
        if st["image_kb"] > 600:
            bad.append((e["id"], f"images too heavy: {st['image_kb']} KB"))
        if st["live_words"] < 25 or st["live_words"] < 10 * st["images"]:
            bad.append((e["id"], f"too little live text for {st['images']} images: {st['live_words']} words"))
    if bad:
        raise SystemExit(f"lint failed: {bad}")


def main():
    lint()
    (ROOT / "templates").mkdir(exist_ok=True)
    data = []
    for e in EMAILS:
        (ROOT / "templates" / f'{e["id"]}.html').write_text(render(e))
        data.append({k: e[k] for k in ("id", "name", "kind", "when", "to", "subject", "preview")} | {"text": plain(e), "deliverability": stats(e)})
    (ROOT / "emails.json").write_text(json.dumps(data, indent=1, ensure_ascii=False))
    if "shots" in sys.argv:
        from playwright.sync_api import sync_playwright
        (ROOT / "shots").mkdir(exist_ok=True)
        with sync_playwright() as p:
            b = p.chromium.launch()
            for w, suf in ((640, ""), (390, "-390")):
                pg = b.new_page(viewport={"width": w, "height": 900}, device_scale_factor=2 if w == 390 else 1.5)
                for e in EMAILS:
                    pg.goto((ROOT / "templates" / f'{e["id"]}.html').as_uri())
                    pg.wait_for_load_state("networkidle")
                    sw = pg.evaluate("document.documentElement.scrollWidth")
                    assert sw <= w, (e["id"], w, sw)
                    pg.screenshot(path=str(ROOT / "shots" / f'{e["id"]}{suf}.png'), full_page=True)
            b.close()
    print("ok", [e["id"] for e in EMAILS])


if __name__ == "__main__":
    main()
