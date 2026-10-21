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
import json, pathlib, sys, html

ROOT = pathlib.Path(__file__).resolve().parent
SITE = "https://www.mahjmatchmaker.com"
NAVY, DEEP, PINK, HPINK, BLUSH, CREAM, PCREAM = "#054689", "#062a55", "#d6336c", "#f56c8c", "#fbe3ea", "#faf3ea", "#fffdfa"

FYM_HTML = 'Find&nbsp;<em>Your</em> Mat&#8209;ch&trade;'  # non-breaking hyphen: never wraps as Mat- / ch
FYM = 'Find <em>Your</em> Mat-ch'
CODE = 'Use code <b>MAHJMATCH</b> to save 💕'
SIGN = 'Happy mat-ching!<br>xo, Tiffany'
FEEDBACK = f'{SITE}/find-your-mat-ch-feedback'  # hidden page, form notifications -> mahjmatchmaker@gmail.com, Gmail label Site/FYM feedback (Claude handles)
CDN_IMG = ''  # set to the pinned jsDelivr folder for Squarespace; empty = local relative paths for previews

EMAILS = [
    {
        "id": "launch",
        "name": "Launch: Find Your Mat-ch is here",
        "kind": "campaign",
        "when": "Tue Oct 27, 9:30am CT, one send",
        "to": "All subscribers (homepage signup, notify-me form and form subscribers all land there)",
        "subject": "It's here! Find Your Mat-ch™ is live 💕",
        "preview": "Pick your tiles, swipe your mats, meet your match.",
        "h1img": "hl-launch-h1",
        "hero": "hero",
        "paras": [
            f'This is a new tool I&rsquo;m rolling out just for you: <b>{FYM_HTML}</b>. This time I&rsquo;m stepping out of the matchmaker seat, and it&rsquo;s your turn to find your match.',
            'My picks are baked right in, so you&rsquo;re never swiping alone.',
        ],
        "steps_head": "hl-launch-how",
        "steps": [
            'Start with the tiles you own, or flip it and start with the mat you already love.',
            'Tap &hearts; on the mats you love and &#10005; on the ones that aren&rsquo;t the one.',
            '&ldquo;Showing: Tiffany&rsquo;s picks only&rdquo; means you&rsquo;re seeing my own matches for your set. Tap it to see every mat, and tap again to bring my picks back.',
            'Tap a color dot to narrow the mats to one color. Tap it again to clear it.',
            'Every couple needs a wingman. Swipe racks the same way, with my rack picks first.',
            'Pick your view, then save it or send it to your mahj group. Every piece is linked.',
        ],
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
.hero{{display:block;width:100%;height:auto;margin:6px 0 4px}}
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


def render(e, with_meta=True):
    h = []
    if with_meta:
        h.append(f'<div class="meta"><b>Subject:</b> {html.escape(e["subject"])}<br><b>Preview:</b> {html.escape(e["preview"])}<br><b>When:</b> {html.escape(e["when"])}</div>')
    h.append('<div class="card"><div class="top"><img src="../../../assets/brand/mahjmatchmaker-wordmark.png" alt="Mahj Matchmaker: matching mahjong tiles, mats &amp; racks"></div><div class="body">')
    if e.get("pill"):
        h.append(f'<div style="text-align:center"><span class="pill">{e["pill"]}</span></div>')
    h.append(f'<h1 style="text-align:center">{e["h1"]}</h1>')
    if e.get("hero"):
        h.append(f'<img class="hero" src="../{e["hero"]}" alt="Match cards fanned out with a heart and an X, swipe-style">')
    for p in e["paras"]:
        h.append(f"<p>{nw(p)}</p>")
    if e.get("list"):
        h.append("<ul>" + "".join(f"<li>{x}</li>" for x in e["list"]) + "</ul>")
    t, u = e["button"]
    h.append(f'<div class="btnw"><a class="btn" href="{u}">{t}</a></div>')
    if e.get("blog"):
        h.append('<div class="blog"><h2>A FEW OF MY FAVORITE READS</h2>' + "".join(
            f'<a class="post" href="{u}"><b>{a}</b><span>{b} &rarr;</span></a>' for a, b, u in e["blog"]) + "</div>")
    for p in e.get("after", []):
        cls = ' class="code"' if p == CODE else ""
        h.append(f"<p{cls}>{nw(p)}</p>")
    h.append(f'<p class="sign">{SIGN}</p></div>')
    h.append('<div class="foot">Mahj Matchmaker · <a href="https://www.mahjmatchmaker.com">mahjmatchmaker.com</a><br>Hooking up tiles, mats &amp; racks</div></div>')
    return f'<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(e["name"])}</title><style>{CSS}</style></head><body><div class="outer">{"".join(h)}</div></body></html>'


def plain(e):
    import re
    def t(s):
        s = re.sub(r'<a href="([^"]+)">([^<]+)</a>', r'\2 (\1)', s)
        s = re.sub(r"<[^>]+>", "", s)
        return html.unescape(s)
    out = [t(e["h1"])] + [t(p) for p in e["paras"]]
    out += ["• " + t(x) for x in e.get("list", [])]
    out.append(f'[BUTTON: {e["button"][0]} → {e["button"][1]}]')
    if e.get("blog"):
        out.append("A few of my favorite reads:")
        out += [f"• {a}: {b} ({u})" for a, b, u in e["blog"]]
    out += [t(p) for p in e.get("after", [])]
    out.append("Happy mat-ching!\nxo, Tiffany")
    out = [o.replace("\u2011", "-").replace("\xa0", " ") for o in out]
    return "\n\n".join(out)


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
    if bad:
        raise SystemExit(f"lint failed: {bad}")


def main():
    lint()
    (ROOT / "templates").mkdir(exist_ok=True)
    data = []
    for e in EMAILS:
        (ROOT / "templates" / f'{e["id"]}.html').write_text(render(e))
        data.append({k: e[k] for k in ("id", "name", "kind", "when", "to", "subject", "preview")} | {"text": plain(e)})
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
