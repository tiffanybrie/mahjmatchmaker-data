#!/usr/bin/env python3
"""Find Your Mat-ch page code block (hidden /find-your-mat-ch-preview now; same block goes on /find-your-match on 10/27).

python3 build.py  ->  page-block.html   (paste into the page's single code block)

Tiffany Oct 21 2:19pm: "change whatever needs to happen over on the Find Your Match preview page. I'd like that looking a lot better."
Sections: hero (lockup, Find *Your* Mat-ch(TM), one line, big Start button, Papaya top-3 match-card fan with X + heart)
-> 3-step how it works (real app screenshots from live v69 + the app's own match card) -> the app, big, with Open full screen
-> Good to know (FAQ) -> match albums strip -> quiet disclosure.

App: static copy of the live artifact 6epA9HuEdT32zUp79Qv3kd, v69 = scratchpad build fym-oct21e (gate PASS).
  index.html pinned on branch fym-site-preview @0269672 (site-app/fym-oct21f/index.html = v70); every other file is identical to
  fym-oct21d, so <base> points at site-app/fym-oct21d/ on the same commit. jsDelivr serves .html as text/plain + nosniff,
  so the HTML is fetched and run in a same-origin srcdoc iframe.
  To ship a newer FYM build: push its index.html (and any changed files) to fym-site-preview, then update APP_INDEX/APP_BASE.
"""
import os, html, json
HERE = os.path.dirname(os.path.abspath(__file__))

CDN = 'https://cdn.jsdelivr.net/gh/tiffanybrie/mahjmatchmaker-data@'
ASSET = CDN + '44563dd1c2c4d9a00aa3deec61b1d86ccfdbcaf8/assets/site/fym-page/'
WORDMARK = CDN + '8952b136784680ba365a33d7ae13ba91a25ab561/assets/brand/mahjmatchmaker-wordmark-notag.png'
APP_COMMIT = 'c7ab351a08109a01afb84eabd0fb8a21e1e7724e'
APP_INDEX = CDN + APP_COMMIT + '/site-app/fym-v107/index.html'  # public 'Version 1.9.2' = internal v107 (Oct 31: logo breathing room, aerial circle 40% of mat, Noli terms only in note + shop list, searched mat obeys filters, no '(retired)' on card screen). Before: public 'Version 1.9.1' = internal v106 (Oct 30 eve: website photo paths fixed (1.9 broke 182 tile photos on the site), B&B racks brand filter + White Wood Stain, Noli June 5 mats, YOLO line, partner coverage gate). Before: public 'Version 1.9' = internal v105 (Oct 30 eve: step 2 photo + card touching, controls under the card, search at every step both directions, Gray Malin + Beach Club Side A/B, LBB holiday mats). Before: public 'Version 1.8' = internal v104 (Oct 30: tiles door opens on partner brand LOGOS, 30+ real tile photos replace 'Photo coming soon', 7 partner mats, 82 mats colour-ranked, Brownstone racks). Before: public 'Version 1.7' = internal v103 (Oct 29 pm: pink Shop by brand feature box, card titles = tile back colour, fill-frame Hummingbird). Before: public 'Version 1.6' = internal v102 (Oct 29: View switch by the deck, bottom-right tile inset, mat-door Aerial + Shop by brand with discount labels). Before: 'Version 1.5' = internal v101 (Oct 27 ~4am: missing partner mats added (Britt Mills House Print + leatherettes, TdT, Bespoke x Brooks Brothers, PLM vegan leather), Spirit of Christmas tiles (sold out); on top of 1.4)
APP_BASE = CDN + 'ad0675e42242c3abad40cac9f539a265220e26eb' + '/site-app/fym-v72/'  # every file but index.html is unchanged since v72; base stays on the v72 commit (warmed; jsDelivr 403'd t15/132.jpg at the new commit)

# Oct 21 3:13pm (Tiffany): the tool's promo SHOWS THE TOOL. Hero = real v69 app screens in a true-proportion iPhone
# (swipe: Papaya Spritz on Heiress, her #1 pick; behind it the two doors). How it works = 6-step tutorial, each a real screen.
# Rendered by scripts/fym_promo/render.py from scripts/fym_promo/capture.py (undo hidden, X + heart only, no %).
PHONES = CDN + 'cd8cb41d47ef16e4c242a56a0add06f768bafb97/assets/site/fym-page-v2/'
# Tiffany 3:56/3:58pm: annotated tutorial (render2.py), one step per block, at the BOTTOM of the page; app at the top.
TUT = CDN + 'fcf9fd12d382b6fa2aad7be5e83a0114033003da/assets/site/fym-tutorial/'  # v72 re-capture (Oct 21 night): 6 steps
HERO_ALT = ('Find Your Mat-ch on a phone: Papaya Spritz tiles swiping on the Heiress mat by Britt Mills with the X and heart '
            'buttons, next to the start screen where you pick Start with tiles or Start with a mat')
FEEDBACK = '/find-your-mat-ch-feedback'
STEPS = [
    ('Pick your&nbsp;door', 'Start with the tile set you own, or flip it and start with the mat you already&nbsp;love.',
     'The start screen with two doors: Start with tiles, or Start with a mat, plus Shop by color'),
    ('Swipe <span class="x">&#10005;</span> or <span class="h">&#9829;</span>', 'Tap &#9829; on the mats you love and &#10005; on the ones that aren&rsquo;t the&nbsp;one.',
     'Swiping mats for Papaya Spritz tiles: the Heiress mat by Britt Mills, marked Tiffany’s match, with the X and heart buttons'),
    ('My picks, on or&nbsp;off', '&ldquo;Showing: Tiffany&rsquo;s picks only&rdquo; shows my own matches for your set. Tap it to see every mat, and tap again to bring my picks&nbsp;back.',
     'The Tiffany’s picks button switched to Showing: all mats, so every mat in the catalog is in the swipe'),
    ('Shop by&nbsp;color', 'Tap a color dot to narrow the mats to one color. Tap it again to clear&nbsp;it.',
     'The color dots above the swipe, with Pink selected'),
    ('Choose your&nbsp;racks', 'Every couple needs a wingman. Swipe racks the same way, with Tiffany&rsquo;s rack picks&nbsp;first.',
     'The racks step: Papaya Spritz tiles on the Heiress mat with Tiffany’s rack match, Middle & Main Scalloped Beechwood'),
    ('Save your match&nbsp;card', 'Pick your view, then save it or send it to your mahj group. Every piece is linked, with code&nbsp;MAHJMATCH.',
     'The finished match card: Papaya Spritz tiles on the Heiress mat with Beechwood racks, ready to save or share'),
]
# First albums on the live albums page (Oct 21), with their live pinned covers.
ALBUMS = [
    ('papaya-spritz', 'Papaya Spritz', CDN + '3091240/assets/covers/albums/w800/00-papaya-spritz-mahjong-tiles-cover.jpg'),
    ('sunday-tile-set', 'Sunday', CDN + 'e34138fda6c04c9c524983f81e828305eb54531a/assets/cards/sunday-tile-set/00-sunday-tile-set-mahjong-tiles-cover.jpg'),
    ('coquette', 'Coquette', CDN + '27a6eb2b447221b2e11c4307064dc2f67d9a818d/assets/covers/albums/w800/00-coquette-mahjong-tiles-cover.jpg'),
    ('seabreeze', 'Seabreeze', CDN + '27a6eb2b447221b2e11c4307064dc2f67d9a818d/assets/covers/albums/w800/00-seabreeze-mahjong-tiles-cover.jpg'),
    ('talulah', 'Talulah', CDN + '27a6eb2b447221b2e11c4307064dc2f67d9a818d/assets/covers/albums/w800/00-talulah-mahjong-tiles-cover.jpg'),
    ('osler', 'Osler', CDN + '27a6eb2b447221b2e11c4307064dc2f67d9a818d/assets/covers/albums/w800/00-osler-mahjong-tiles-cover.jpg'),
]
FAQ = [
    ('Who picks the matches?',
     'Tiffany&rsquo;s picks are built right in. While the button says <b>Tiffany&rsquo;s picks: on</b>, every mat you see is her own match for your set. Tap it to swipe the whole library and make your own&nbsp;matches.'),
    ('I already have a mat. Can I start&nbsp;there?',
     'Yes. Tap <b>Start with a mat</b> and swipe through tile sets that match it, then add&nbsp;racks.'),
    ('How do I save?',
     'Use code <b>MAHJMATCH</b> to save at 30+ partner brands. Your match card links every piece, and each brand&rsquo;s code page has the&nbsp;details.'),
    ('Does it cost anything?',
     'No. Find <em>Your</em> Mat-ch is free, with nothing to sign up for. Swipe as much as you&nbsp;like.'),
]

CSS = r'''
@import url('https://fonts.googleapis.com/css2?family=Caprasimo&family=Bitter:wght@500;600;700&family=Lora:ital,wght@0,500;0,700;1,500&family=Caveat:wght@700&display=swap');
#fymx{--navy:#054689;--navy2:#062a55;--rose:#c8325f;--pink:#d6336c;--heart:#f56c8c;--blush:#f7b6c8;--pc:#fbe3ea;--cream:#faf3ea;--ink:#2a2440;
  position:relative;box-sizing:border-box;color:var(--ink);font-family:'Bitter',Georgia,serif;overflow-x:clip;background:var(--cream)}
#fymx *,#fymx *::before,#fymx *::after{box-sizing:border-box}
#fymx img{max-width:100%;display:block}
#fymx h1,#fymx h2,#fymx h3{font-family:'Caprasimo',Georgia,serif;font-weight:400;color:var(--navy);margin:0;letter-spacing:0;text-wrap:balance;line-height:1.05;text-transform:none}
#fymx h1 em,#fymx h2 em{font-style:normal;color:var(--rose)}  /* no italics in headlines (Tiffany Oct 21 6:30pm) */
#fymx p{margin:0;text-wrap:pretty}
#fymx a{color:inherit}
#fymx .nb{white-space:nowrap}
.fx-wrap{max-width:1180px;margin:0 auto;padding:0 20px}
.fx-kick{font:700 13px/1 'Bitter',Georgia,serif;letter-spacing:.18em;text-transform:uppercase;color:var(--rose);margin-bottom:12px!important}
/* hero */
.fx-hero{position:relative;padding:30px 0 26px;overflow:hidden;background:radial-gradient(circle at 78% 46%,var(--pc) 0,var(--pc) 34%,transparent 34.2%),radial-gradient(circle at 4% 100%,#fdeef2 0,#fdeef2 16%,transparent 16.2%),var(--cream)}
.fx-hero .fx-wrap{display:grid;grid-template-columns:1fr;gap:34px;align-items:center}
.fx-copy{text-align:center;position:relative;z-index:2}
.fx-lock{display:inline-flex;flex-direction:column;width:230px;margin:0 auto 22px}
.fx-lock img{width:100%;height:auto}
.fx-lock b{display:block;margin-top:.5em;background:var(--heart);color:#fff;font:700 8.3px/1 'Bitter',Georgia,serif;letter-spacing:.15em;text-align:center;white-space:nowrap;padding:.5em 0 .45em;border-radius:3px}
#fymx h1{font-size:clamp(46px,11.5vw,84px);line-height:1;word-spacing:0}
#fymx h1 em{padding-right:.08em}
#fymx h1 sup{font-family:'Bitter',Georgia,serif;font-size:.28em;vertical-align:top;line-height:1;position:relative;top:.35em;margin-left:.08em;color:var(--navy)}
.fx-lede{font:500 clamp(18px,4.6vw,22px)/1.45 'Lora',Georgia,serif;color:var(--navy2);max-width:30em;margin:18px auto 0!important}
.fx-btn{display:inline-flex;align-items:center;justify-content:center;gap:.55em;margin-top:28px;min-height:62px;padding:0 40px;border-radius:999px;background:var(--rose);color:#fff!important;text-decoration:none!important;font:700 21px/1 'Bitter',Georgia,serif;box-shadow:0 14px 30px rgba(200,50,95,.32);transition:transform .15s ease,box-shadow .15s ease;cursor:pointer;border:0}
.fx-btn:hover{transform:translateY(-2px);box-shadow:0 18px 36px rgba(200,50,95,.38)}
.fx-btn span{font-size:.95em}
.fx-under{margin-top:16px!important;font-size:15px;line-height:1.5;color:#4b4560}
.fx-under b{color:var(--navy);letter-spacing:.04em}
.fx-under a{color:var(--navy);font-weight:700;text-decoration:underline;text-decoration-color:var(--blush);text-underline-offset:3px;text-decoration-thickness:2px}
/* app phones (real v69 screens) */
.fx-phones{position:relative;width:min(100%,460px);margin:0 auto}
.fx-phones img{width:100%;height:auto}
@media (min-width:980px){
  .fx-hero{padding:40px 0 30px}
  .fx-lock{margin:0 0 26px}
  .fx-lede{margin:20px auto 0!important}
  .fx-phones{width:100%;max-width:540px}
}
/* how it works */
.fx-tut{background:#fff;padding:60px 0 66px;scroll-margin-top:var(--fx-off,0px)}
.fx-tut .fx-head{text-align:center;margin-bottom:30px}.fx-tut .fx-head p:not(.fx-kick){font-size:16px;color:#4b4560;margin-top:8px!important}
.fx-tsteps{list-style:none;margin:0 auto!important;padding:0!important;max-width:620px;display:grid;gap:44px}
.fx-tstep{margin:0!important;text-align:center}.fx-tstep::before{display:none!important}
.fx-tnum{width:46px;height:46px;border-radius:50%;background:var(--rose);color:#fff;font:400 24px/46px 'Caprasimo',Georgia,serif;margin:0 auto 10px}
.fx-tstep h3{font-size:clamp(28px,6.4vw,36px);margin-bottom:8px}
.fx-tstep p{font-size:17px;line-height:1.55;color:#4b4560;max-width:34em;margin:0 auto 16px!important}
.fx-tstep img{width:100%;height:auto;border-radius:22px;box-shadow:0 14px 34px rgba(6,42,85,.12)}
.fx-tut .fx-more{text-align:center;margin-top:40px!important}
@media (max-width:560px){.fx-tut .fx-wrap{padding:0 10px}.fx-tstep img{border-radius:14px}}
.fx-how{background:#fff;padding:64px 0 70px}
.fx-how .fx-head{text-align:center;margin-bottom:38px}
.fx-how h2,.fx-app h2,.fx-faq h2,.fx-albums h2{font-size:clamp(34px,7.4vw,50px)}
.fx-steps{display:grid;grid-template-columns:1fr;gap:26px;list-style:none;margin:0 auto!important;padding:0!important;max-width:1080px}
.fx-step{background:var(--cream);border-radius:26px;padding:22px 22px 26px;display:flex;flex-direction:column;align-items:center;text-align:center;margin:0!important}
.fx-step::before{display:none!important}
.fx-phone{width:100%;max-width:240px;margin:0 auto 14px}
.fx-phone img{width:100%;height:auto}
.fx-num{width:42px;height:42px;border-radius:50%;background:var(--navy);color:#fff;font:400 22px/42px 'Caprasimo',Georgia,serif;margin:0 auto 10px}
.fx-step h3{font-size:clamp(24px,5.4vw,28px);margin-bottom:8px}
.fx-step h3 .x{color:#8d97ad;font-family:Arial,sans-serif;font-size:.85em}
.fx-step h3 .h{color:var(--heart);font-family:Arial,sans-serif}
.fx-step p{font-size:16px;line-height:1.55;color:#4b4560;max-width:22em}
@media (min-width:560px){.fx-steps{grid-template-columns:repeat(2,1fr)}}
@media (min-width:900px){.fx-steps{grid-template-columns:repeat(3,1fr)}}
.fx-fb{text-align:center;margin-top:12px!important;font-size:15px;color:#4b4560;padding:0 16px}
.fx-fb a{color:var(--navy)!important;font-weight:700;text-decoration:underline;text-decoration-color:var(--blush);text-underline-offset:3px;text-decoration-thickness:2px}
/* app */
.fx-app{position:relative;padding:18px 0 56px;background:radial-gradient(circle at 12% 18%,var(--pc) 0,var(--pc) 13%,transparent 13.2%),radial-gradient(circle at 90% 82%,var(--pc) 0,var(--pc) 16%,transparent 16.2%),#fdf3f7;scroll-margin-top:var(--fx-off,0px)}
.fx-app .fx-head{text-align:center;margin-bottom:20px}
.fx-app .fx-head p:not(.fx-kick){font-size:16px;color:#4b4560;margin-top:8px!important}
.fx-bar{display:flex;justify-content:center;gap:10px;flex-wrap:wrap;margin:0 auto 14px;padding:0 16px}
.fx-pill{display:inline-flex;align-items:center;gap:.45em;min-height:44px;padding:0 18px;border-radius:999px;border:2px solid var(--blush);background:#fff;color:var(--navy)!important;font:700 15px/1 'Bitter',Georgia,serif;text-decoration:none!important;cursor:pointer}
.fx-pill:hover{border-color:var(--rose)}
.fx-pill svg{width:16px;height:16px}
.fx-grid{display:grid;grid-template-columns:1fr;justify-items:center;gap:20px}
.fx-side{display:none}
.fx-stage{position:relative;width:100%;height:640px;background:#fff;overflow:hidden}
.fx-stage iframe{position:absolute;inset:0;width:100%;height:100%;border:0;display:block;background:#fff}
.fx-ld{position:absolute;inset:0;display:flex;flex-direction:column;gap:14px;align-items:center;justify-content:center;font:700 17px 'Bitter',Georgia,serif;color:var(--navy);text-align:center;padding:0 24px;background:#fff;z-index:1}
.fx-ld i{width:44px;height:44px;border-radius:50%;border:4px solid var(--pc);border-top-color:var(--rose);animation:fxspin 1s linear infinite}
.fx-ld.err i{display:none}.fx-ld.err{color:var(--rose)}
@keyframes fxspin{to{transform:rotate(360deg)}}
.fx-x{display:none;position:absolute;z-index:3;top:calc(12px + env(safe-area-inset-top,0px));left:calc(12px + env(safe-area-inset-left,0px));min-height:38px;padding:0 12px;border-radius:999px;border:0;background:var(--navy);color:#fff;font:700 13px/1 'Bitter',Georgia,serif;cursor:pointer;box-shadow:0 6px 16px rgba(6,42,85,.3)}
.fx-stage.fs{position:fixed!important;inset:0!important;width:100%!important;height:100%!important;max-width:none!important;border-radius:0!important;z-index:2147483000;margin:0!important;border:0!important}
.fx-stage.fs .fx-x{display:block}
html.fx-lock-scroll,html.fx-lock-scroll body{overflow:hidden!important}
/* Oct 25 night (live check): Squarespace main.container is z-index 9 under the header (10), which trapped the full-screen tool under the header; lift the tool's ancestors while full screen */
html.fx-lock-scroll main{z-index:2147483000!important}
.fx-code{text-align:center;margin-top:18px!important;font-size:16px;color:#4b4560;padding:0 16px}
.fx-code b{color:var(--navy);letter-spacing:.04em}
@media (min-width:760px){
  .fx-stage{max-width:580px;border-radius:28px;border:8px solid #fff;box-shadow:0 26px 60px rgba(6,42,85,.18),0 4px 14px rgba(6,42,85,.08)}
}
@media (min-width:1120px){
  .fx-grid{grid-template-columns:1fr 580px 1fr;align-items:center;gap:36px;max-width:1240px;margin:0 auto;padding:0 24px}
  .fx-side{display:block;align-self:center}
  .fx-bar{display:none}
  .fx-tips{list-style:none;margin:0!important;padding:0!important;display:grid;gap:14px;justify-self:end;max-width:250px}
  .fx-tips li{margin:0!important;background:#fff;border-radius:18px;padding:14px 16px;font-size:15px;line-height:1.45;color:#4b4560;box-shadow:0 8px 20px rgba(6,42,85,.07)}
  .fx-tips li::before{display:none!important}
  .fx-tips b{display:block;color:var(--navy);font-size:16px;margin-bottom:2px}
  .fx-tips .x{color:#8d97ad;font-family:Arial,sans-serif}.fx-tips .h{color:var(--heart);font-family:Arial,sans-serif}
  .fx-side.r{justify-self:start;max-width:250px;display:grid;gap:14px}
  .fx-card{background:var(--navy);color:#fff;border-radius:22px;padding:20px 18px;text-align:center}
  .fx-card p{font-size:15px;line-height:1.5;color:#dfe7f4}
  .fx-card strong{display:block;font:400 26px/1.1 'Caprasimo',Georgia,serif;color:#fff;margin:6px 0 8px;letter-spacing:.02em}
  .fx-side.r .fx-pill{justify-content:center}
  .fx-code{display:none}
}
/* faq */
.fx-faq{background:#fff;padding:62px 0 56px}
.fx-faq .fx-head{text-align:center;margin-bottom:26px}
.fx-qs{max-width:760px;margin:0 auto;display:grid;gap:12px}
.fx-qs details{background:var(--cream);border-radius:18px;padding:0 20px}
.fx-qs summary{list-style:none;cursor:pointer;display:flex;justify-content:space-between;align-items:center;gap:16px;min-height:60px;font:700 18px/1.35 'Bitter',Georgia,serif;color:var(--navy)}
.fx-qs summary::-webkit-details-marker{display:none}
.fx-qs summary::after{content:'+';font:400 28px/1 'Caprasimo',Georgia,serif;color:var(--rose);flex:none;transition:transform .2s}
.fx-qs details[open] summary::after{transform:rotate(45deg)}
.fx-qs details p{padding:0 0 18px;font-size:16px;line-height:1.6;color:#4b4560}
.fx-qs b{color:var(--navy)}
.fx-trust{display:flex;flex-wrap:wrap;justify-content:center;gap:10px 22px;margin:30px auto 0!important;font:700 14px/1.3 'Bitter',Georgia,serif;color:var(--navy);letter-spacing:.02em;max-width:760px;text-align:center}
.fx-trust span{display:inline-flex;align-items:center;gap:.45em}
.fx-trust span::before{content:'\2665';color:var(--heart);font-family:Arial,sans-serif}
/* albums */
.fx-albums{background:var(--cream);padding:60px 0 54px}
.fx-albums .fx-head{text-align:center;margin-bottom:26px}
.fx-albums .fx-head p:not(.fx-kick){font:500 18px/1.5 'Lora',Georgia,serif;color:var(--navy2);margin-top:10px!important}
.fx-covers{display:grid;grid-template-columns:repeat(2,1fr);gap:14px;max-width:1080px;margin:0 auto}
.fx-covers a{display:block;text-decoration:none!important;border-radius:16px;overflow:hidden;background:#fff;box-shadow:0 10px 24px rgba(6,42,85,.1);transition:transform .15s ease}
.fx-covers a:hover{transform:translateY(-3px)}
.fx-covers img{width:100%;height:auto!important;aspect-ratio:4/5;object-fit:cover}
.fx-covers span{display:block;padding:10px 8px 12px;text-align:center;font:700 15px/1.2 'Bitter',Georgia,serif;color:var(--navy)}
@media (min-width:700px){.fx-covers{grid-template-columns:repeat(3,1fr)}}
@media (min-width:1000px){.fx-covers{grid-template-columns:repeat(6,1fr)}}
.fx-albums .fx-more{text-align:center;margin-top:26px!important}
.fx-albums .fx-btn{margin-top:0;background:var(--navy);box-shadow:0 12px 26px rgba(6,42,85,.24);font-size:18px;min-height:54px;padding:0 30px}
.fx-disc{text-align:center;font-size:13px;color:#6f6880;padding:22px 16px 26px;background:var(--cream);margin:0!important}
@media (prefers-reduced-motion:reduce){#fymx *{transition:none!important;animation:none!important}}
/* Squarespace section around this block */
section:has(#fymx) .section-background{background:var(--cream,#faf3ea)!important}
section:has(#fymx) .content-wrapper{padding-top:0!important;padding-bottom:0!important}
section:has(#fymx) .fe-block:has(#fymx) .sqs-block{padding:0!important}
/* Oct 25: the Squarespace grid kept the block ~720px taller than the page (empty cream gap under the albums on desktop).
   This section holds only this block, so drop the fixed grid rows and let it be exactly as tall as the content. */
section:has(#fymx) .fluid-engine{display:block!important;min-height:0!important;height:auto!important;grid-template-rows:none!important}
section:has(#fymx) .fe-block:has(#fymx){height:auto!important;min-height:0!important;grid-area:auto!important}
section:has(#fymx) .content-wrapper,section:has(#fymx) .section-border{min-height:0!important}
/* Oct 25: swipes inside the tool stay in the tool (no hand-off that flings the page to the footer) */
.fx-stage,.fx-stage iframe{overscroll-behavior:contain}
/* phone full-screen mode (PHONE_FULLSCREEN): the tool lives off-screen at full size until Start opens it */
.fx-pstart{display:none}
#fymx.pfs .fx-pstart{display:block;text-align:center}
#fymx.pfs .fx-app .fx-head,#fymx.pfs .fx-bar{display:none}
#fymx.pfs .fx-app{padding:6px 0 34px}
#fymx.pfs .fx-pstart .fx-btn{margin-top:0}
#fymx.pfs .fx-pstart small{display:block;margin-top:12px;font-size:14px;color:#4b4560}
#fymx.pfs .fx-hero .fx-pstart .fx-btn{margin-top:24px}
#fymx.pfs .fx-stage:not(.fs){position:fixed!important;left:-300vw!important;top:0!important;width:100vw!important;height:100vh!important;visibility:hidden;pointer-events:none}
#fymx.pfs .fx-stage.fs{height:100dvh!important}
'''

JS = r'''
(function(){
  var root=document.getElementById('fymx');if(!root||root.getAttribute('data-on'))return;root.setAttribute('data-on','1');
  var IDX='__IDX__',BASE='__BASE__',PFS=__PFS__;
  var stage=document.getElementById('fx-stage'),fr=document.getElementById('fx-f'),ld=document.getElementById('fx-ld'),de=document.documentElement;
  function hdr(){var h=document.querySelector('header#header,.header'),off=0;
    if(h){var cs=getComputedStyle(h),r=h.getBoundingClientRect();if((cs.position==='fixed'||cs.position==='sticky')&&r.bottom>0)off=r.height;}return off;}
  function phone(){return PFS&&de.clientWidth<760;}
  function size(){
    root.classList.toggle('pfs',phone());
    /* full bleed: stretch to the page edges whatever column the code block sits in */
    root.style.marginLeft='0px';root.style.width='';
    var pr=root.parentElement.getBoundingClientRect(),cw=de.clientWidth;
    root.style.marginLeft=(-pr.left)+'px';root.style.width=cw+'px';
    var off=hdr(),vh=window.innerHeight||de.clientHeight;root.style.setProperty('--fx-off',off+'px');
    if(stage.classList.contains('fs'))return;
    var h=cw<760?vh-off-48:Math.min(vh-off-48,940);
    stage.style.height=Math.max(cw<760?520:600,Math.round(h))+'px';
  }
  size();addEventListener('resize',size);addEventListener('load',size);[300,1000,2500].forEach(function(t){setTimeout(size,t)});
  addEventListener('orientationchange',function(){setTimeout(size,250)});
  if(window.ResizeObserver){try{new ResizeObserver(size).observe(root.parentElement)}catch(e){}}
  var started=false;
  function get(n){return fetch(IDX,{cache:'force-cache'}).then(function(r){if(!r.ok)throw r.status;return r.text()}).catch(function(e){if(n>0)return new Promise(function(ok){setTimeout(ok,1500)}).then(function(){return get(n-1)});throw e;});}
  function start(){if(started)return;started=true;
    get(4).then(function(t){
      t=t.replace(/<head>/i,'<head><base href="'+BASE+'"><style>html{scrollbar-width:thin;scrollbar-color:#f3b9cb transparent}[data-door] *{text-wrap:balance}html,body{overscroll-behavior:contain}#stage,#stage.scroll,.rail,.msr,.sheet .box{overscroll-behavior:contain}.dots,.frow,.tray .th,.rsug .th{overscroll-behavior-x:contain}</style>');
      fr.addEventListener('load',function(){ld.style.display='none';});
      var tries=0,poll=setInterval(function(){tries++;try{var d=fr.contentDocument;if(d&&d.querySelector('#app .top')){ld.style.display='none';clearInterval(poll);}}catch(e){}if(tries>200)clearInterval(poll);},300);
      fr.srcdoc=t;
    }).catch(function(){ld.className+=' err';ld.innerHTML='The app did not load. Please refresh the page.';});
  }
  if('IntersectionObserver' in window){var io=new IntersectionObserver(function(es){if(es.some(function(e){return e.isIntersecting})){start();io.disconnect();}},{rootMargin:'1400px 0px'});io.observe(stage);}
  setTimeout(start,2500);
  function go(e){if(e)e.preventDefault();if(phone()){fs(true);return;}start();size();var sec=document.getElementById('fymx-app');
    var vh=window.innerHeight||de.clientHeight,off=hdr(),r=stage.getBoundingClientRect();
    var y=r.top+(window.pageYOffset||de.scrollTop)-Math.max(off,Math.round((vh-off-r.height)/2)+off);
    window.scrollTo({top:y,behavior:'smooth'});}
  [].forEach.call(root.querySelectorAll('[data-fx-go]'),function(a){a.addEventListener('click',go)});
  [].forEach.call(root.querySelectorAll('[data-fx-tour]'),function(a){a.addEventListener('click',function(e){go(e);var n=0;(function tryT(){var b=null;try{b=fr.contentDocument&&fr.contentDocument.querySelector('[data-tour]')}catch(x){}
    if(b){setTimeout(function(){b.click()},450);}else if(n++<120){setTimeout(tryT,250);}})();})});
  [].forEach.call(root.querySelectorAll('[data-fx-how]'),function(a){a.addEventListener('click',function(e){e.preventDefault();var t=document.getElementById('fymx-how');
    window.scrollTo({top:t.getBoundingClientRect().top+(window.pageYOffset||de.scrollTop)-hdr()-8,behavior:'smooth'});})});
  function fs(on){start();stage.classList.toggle('fs',on);de.classList.toggle('fx-lock-scroll',on);if(!on)size();
    if(on)setTimeout(function(){try{fr.focus();fr.contentWindow.dispatchEvent(new Event('resize'))}catch(e){}},50);}
  [].forEach.call(root.querySelectorAll('[data-fx-start]'),function(b){b.addEventListener('click',function(e){e.preventDefault();fs(true)})});
  [].forEach.call(root.querySelectorAll('[data-fx-fs]'),function(b){b.addEventListener('click',function(e){e.preventDefault();fs(true)})});
  document.getElementById('fx-x').addEventListener('click',function(){fs(false)});
  addEventListener('keydown',function(e){if(e.key==='Escape'&&stage.classList.contains('fs'))fs(false)});
  fr.addEventListener('load',function(){try{fr.contentWindow.addEventListener('keydown',function(e){if(e.key==='Escape'&&stage.classList.contains('fs'))fs(false)})}catch(e){}});
})();
'''

FS_ICON = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M2 6V2h4M14 6V2h-4M2 10v4h4M14 10v4h-4"/></svg>'


SHOW_WALKTHROUGH = False

# Oct 25 9:11pm (Tiffany: the page "fights" the tool on her phone). PHONE_FULLSCREEN=True: under 760px wide the tool is NOT
# embedded in the page; the hero shows a big Start button and the app opens in the full-screen overlay (X to come back).
# Desktop is unchanged. Set False to go back to the in-page tool on phones.
PHONE_FULLSCREEN = False

# Oct 26 12:40am (Tiffany): the page OPENS TO THE TOOL. An app inside a scrolling page makes two scrolls fight (people scroll
# past it, or get stuck inside it). APP_FIRST=True: the page never scrolls. Desktop: the tool fills the window height under
# the site header, the intro sits in the left space and the code + albums in the right. Phone: the tool fills the screen.
# FAQ / albums strip / tutorial are not shown (albums stay one tap away). Set False to go back to the scrolling page.
APP_FIRST = True
AF_CSS = r"""
html.af,html.af body{overflow:hidden!important;overscroll-behavior:none}
#fymx.af{position:fixed!important;left:0!important;right:0!important;bottom:0!important;top:var(--af-top,0px)!important;margin:0!important;width:auto!important;background:var(--cream,#faf3ea);z-index:2147483000;overflow:hidden}
#fymx.af>section:not(.fx-app),#fymx.af>.fx-disc,#fymx.af .fx-app .fx-head,#fymx.af .fx-app .fx-bar,#fymx.af .fx-app .fx-code,#fymx.af .fx-side.r [data-fx-fs],#fymx.af .fx-pstart{display:none!important}
#fymx.af .fx-app{height:100%;padding:0!important;margin:0!important;background:transparent}
#fymx.af .fx-grid{display:grid!important;grid-template-columns:minmax(0,1fr) minmax(380px,560px) minmax(0,1fr);gap:clamp(20px,3vw,48px);height:100%;max-width:none!important;padding:16px clamp(16px,3vw,48px)!important;box-sizing:border-box;align-items:center;margin:0!important}
#fymx.af .fx-stage{height:100%!important;max-height:none!important;width:100%!important;margin:0!important}
#fymx.af .fx-side{display:flex!important;flex-direction:column;justify-content:center;gap:14px;min-width:0}
#fymx.af .fx-side.l{align-items:flex-end;text-align:right}
#fymx.af .fx-side.l .fx-hero{background:none!important;padding:0!important;margin:0!important;min-height:0!important}
#fymx.af .fx-side.l .fx-wrap,#fymx.af .fx-side.l .fx-copy{padding:0!important;margin:0!important;max-width:380px;text-align:right}
#fymx.af .fx-side.l h1{font-size:clamp(40px,3.6vw,62px)!important;line-height:1.02!important;margin:6px 0 14px!important}
#fymx.af .fx-side.l .fx-lede{font-size:clamp(17px,1.35vw,21px)!important;margin:0 0 14px!important}
#fymx.af .fx-side.l .fx-under{font-size:15px!important;margin:0!important;line-height:1.9}
#fymx.af .fx-side.l .fx-under .nb{display:block}
#fymx.af .fx-side.l .fx-under{font-size:0!important}#fymx.af .fx-side.l .fx-under>*{font-size:15px}
#fymx.af .fx-side.l .fx-afnote{font-size:13px;color:#6f6880;margin:22px 0 0;max-width:300px}
#fymx.af .fx-side.r{align-items:flex-start}
#fymx.af .af-code{display:none;font-size:16px;color:var(--navy,#06428a);margin:0 0 18px}#fymx.af .af-code b{font-size:20px;letter-spacing:.04em}
#fymx.af .fx-fb{position:absolute;left:0;right:0;bottom:6px;text-align:center;font-size:12px!important;margin:0!important;display:none}
@media (max-width:759px){
  html.af main{z-index:2147483000!important}
  #fymx.af{top:0!important}
  #fymx.af .fx-grid{display:block!important;padding:0!important}
  #fymx.af .fx-side{display:none!important}
  #fymx.af .fx-stage{border-radius:0!important;border:0!important;box-shadow:none!important;height:100dvh!important;height:100vh}
  #fymx.af .fx-stage .fx-x{display:none!important}
}
@media (min-width:760px) and (max-width:1099px){
  #fymx.af .fx-grid{grid-template-columns:minmax(0,1fr) minmax(360px,520px) minmax(0,.35fr)}
  #fymx.af .fx-side.r{visibility:hidden}
  #fymx.af .fx-side.l .af-code{display:block}
}
"""
AF_JS = r"""
(function(){
  var root=document.getElementById('fymx');if(!root||root.getAttribute('data-af'))return;root.setAttribute('data-af','1');
  var de=document.documentElement;de.classList.add('af');root.classList.add('af');
  var hero=root.querySelector('.fx-hero'),left=root.querySelector('.fx-side:not(.r)');
  if(hero&&left){left.classList.add('l');left.removeAttribute('aria-hidden');left.appendChild(hero);
    var n=document.createElement('p');n.className='fx-afnote';n.innerHTML='<span class="af-code">Use code <b>MAHJMATCH</b><br>at 30+ partner brands</span>Something look off or have an idea? <a href="/find-your-mat-ch-feedback">Tell me here&nbsp;&rarr;</a><br>Affiliate links: I may earn a commission.';left.appendChild(n);}
  function top(){var t=0;if(window.innerWidth>=760){var h=document.querySelector('header#header,.header');if(h){var r=h.getBoundingClientRect();t=Math.max(0,Math.round(r.bottom));}}
    root.style.setProperty('--af-top',t+'px');window.scrollTo(0,0);}
  top();addEventListener('resize',top);addEventListener('load',top);[200,800,2000].forEach(function(ms){setTimeout(top,ms)});
  if(window.ResizeObserver){var h=document.querySelector('header#header,.header');if(h)try{new ResizeObserver(top).observe(h)}catch(e){}}
  setTimeout(function(){try{var f=document.getElementById('fx-f');f&&f.focus()}catch(e){}},1200);
})();
"""


def build():
    T = json.load(open(os.path.join(HERE, '..', '..', '..', 'scripts', 'fym_promo', 'tutorial.json')))
    tut = ''.join(f'<li class="fx-tstep"><div class="fx-tnum">{t["n"]}</div><h3>{t["title"]}</h3><p>{t["caption"]}</p>'
                  f'<img src="{TUT}tut{t["n"]}.webp" alt="{html.escape(t["alt"])}" width="{t["page"][0]}" height="{t["page"][1]}" loading="lazy" decoding="async"></li>'
                  for t in T)
    faq = ''.join(f'<details{" open" if i == 0 else ""}><summary>{q}</summary><p>{a}</p></details>' for i, (q, a) in enumerate(FAQ))
    covers = ''.join(f'<a href="/{slug}-mahjong-tile-matches"><img src="{img}" alt="{name} mahjong tile matches album" loading="lazy" decoding="async" width="800" height="1000"><span>{name}</span></a>'
                     for slug, name, img in ALBUMS)
    # Oct 25 (Tiffany): the 30-second tour replaces the step-by-step walkthrough and the desktop tip boxes
    # (they read like buttons). PARKED, not deleted: set SHOW_WALKTHROUGH=True to bring them back.
    TIPS = f'''<ul class="fx-side fx-tips"><li><b><span class="h">&#9829;</span> Love it</b>It waits for you so you can&nbsp;compare.</li><li><b><span class="x">&#10005;</span> Not the one</b>On to the next mat, no hard&nbsp;feelings.</li><li><b>Zoom in</b>Pinch or tap + and your zoom stays put as you&nbsp;swipe.</li><li><b>Shop by color</b>Tap a color dot while swiping to narrow, tap again to&nbsp;clear.</li></ul>''' if SHOW_WALKTHROUGH else '<div class="fx-side" aria-hidden="true"></div>'
    TUTSEC = f'''<section class="fx-tut" id="fymx-how"><div class="fx-wrap">
<div class="fx-head"><p class="fx-kick">How it works</p><h2>Find your match, step by&nbsp;step</h2><p>Scroll down. Each screen shows exactly what to&nbsp;tap.</p></div>
<ol class="fx-tsteps">{tut}</ol>
<p class="fx-more"><a class="fx-btn" href="#fymx-app" data-fx-go>Start swiping <span aria-hidden="true">&#9829;</span></a></p>
</div></section>''' if SHOW_WALKTHROUGH else ''
    body = f'''<div id="fymx">
<section class="fx-hero"><div class="fx-wrap">
<div class="fx-copy">
<p class="fx-kick">New from Mahj Matchmaker</p>
<h1><span class="nb">Find Your</span> <span class="nb">Mat-ch<sup>&trade;</sup></span></h1>
<p class="fx-lede">Start with tiles or a mat. Swipe. Find your&nbsp;match.</p>
<div class="fx-pstart"><button type="button" class="fx-btn" data-fx-start>Start swiping <span aria-hidden="true">&#9829;</span></button><small>Opens full screen. Tap &#10005; Close to come back.</small></div>
<p class="fx-under"><a href="#fymx-app" data-fx-tour>Take the 30-second tour&nbsp;&darr;</a> &nbsp;&middot;&nbsp; <span class="nb">Free, nothing to sign up&nbsp;for</span></p>
</div>
</div></section>
<section class="fx-app" id="fymx-app">
<div class="fx-wrap fx-head"><p>Tap &#9829; to add a mat to your shortlist, &#10005; for not the&nbsp;one.</p></div>
<div class="fx-bar"><button type="button" class="fx-pill" data-fx-fs>{FS_ICON}Open full screen</button></div>
<div class="fx-grid">
{TIPS}
<div class="fx-stage" id="fx-stage"><div class="fx-ld" id="fx-ld"><i></i>Loading your matchmaker&hellip;</div><button type="button" class="fx-x" id="fx-x">&#10005; Close</button><iframe id="fx-f" title="Find Your Mat-ch" allow="web-share; clipboard-write; fullscreen"></iframe></div>
<div class="fx-side r"><div class="fx-card"><p>Use code</p><strong>MAHJMATCH</strong><p>to save at 30+ partner&nbsp;brands</p></div><button type="button" class="fx-pill" data-fx-fs>{FS_ICON}Open full screen</button><a class="fx-pill" href="/mahjong-tile-matches">Browse the albums</a></div>
</div>
<p class="fx-code">Use code <b>MAHJMATCH</b> to save at 30+ partner&nbsp;brands</p>
<p class="fx-fb">Something look off or have an idea? <a href="{FEEDBACK}">Tell me here&nbsp;&rarr;</a></p>
</section>
<section class="fx-faq"><div class="fx-wrap">
<div class="fx-head"><p class="fx-kick">Good to know</p><h2>Questions, <em>answered</em></h2></div>
<div class="fx-qs">{faq}</div>
<p class="fx-trust"><span>Every &ldquo;Tiffany&rsquo;s match&rdquo; is her own pick</span><span>Code MAHJMATCH at 30+ partner brands</span><span>Free to use</span></p>
</div></section>
<section class="fx-albums"><div class="fx-wrap">
<div class="fx-head"><p class="fx-kick">Prefer to browse?</p><h2>The match <em>albums</em></h2><p>Tiffany&rsquo;s matches for each tile set, with racks and a link to&nbsp;shop.</p></div>
<div class="fx-covers">{covers}</div>
<p class="fx-more"><a class="fx-btn" href="/mahjong-tile-matches">See all match&nbsp;albums</a></p>
</div></section>
{TUTSEC}
<p class="fx-disc">Something look off or have an idea? <a href="{FEEDBACK}">Tell me here&nbsp;&rarr;</a><br>Affiliate links: I may earn a commission.</p>
</div>
<style>{CSS}{AF_CSS if APP_FIRST else ''}</style>
<script>{JS.replace('__IDX__', APP_INDEX).replace('__BASE__', APP_BASE).replace('__PFS__', 'true' if PHONE_FULLSCREEN else 'false')}{AF_JS if APP_FIRST else ''}</script>
'''
    out = os.path.join(HERE, 'page-block.html')
    open(out, 'w').write(body)
    print(out, len(body))


if __name__ == '__main__':
    build()
