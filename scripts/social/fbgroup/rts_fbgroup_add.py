"""RTS: refresh the NEW ERA Facebook group post (d-fbpublic, same id so her state carries),
add the Papaya Spritz group launch post (l-fb-papaya) and the reusable Coming soon template
(l-fb-comingsoon), all in Ready for you now under a 'Facebook group' heading.
Usage: python3 rts_fbgroup_add.py SRC.html OUT.html
Images are already in the artifact's asset store (/_blob/ urls below).
"""
import json, sys, os, html as H
SRC, OUT = sys.argv[1], sys.argv[2]
D = os.path.dirname(os.path.abspath(__file__))
rd = lambda f: open(os.path.join(D, f), encoding='utf-8').read().strip()
s = open(SRC, encoding='utf-8').read()

ALBUMS_IMG = '/_blob/bb3a03222c1453f983641c75b4f64081'
PAPAYA_IMG = '/_blob/b08b127d6c1f717150b6a887b8187ce0'
VIV_IMG = '/_blob/eddff60b5b9aaf75b34014d48c2abac4'

tpl_all = rd('coming-soon-template.txt')
tpl = tpl_all.split('=== EXAMPLE')[0].replace('=== TEMPLATE (fill the brackets; one 🗓️ block per launch, soonest first) ===', '').strip()
tpl_post, tpl_rest = tpl.split('\n\nFirst comment:\n', 1)
tpl_comment, tpl_rules = tpl_rest.split('\n\nRules for filling it:\n', 1)
ex = tpl_all.split('needs a fresh check before it\'s used) ===', 1)[1].strip()

def box(label, text):
    return (f'<div class="fbg-l">{H.escape(label)}</div><div class="fbg-cap"><pre>{H.escape(text)}</pre>'
            f'<button type="button" class="fbg-copy">Copy {H.escape(label.lower())}</button></div>')

def pic(u, alt):
    return f'<img class="pic" src="{u}" alt="{H.escape(alt)}" data-zoom="{u}" loading="lazy">'

ITEMS = {
 'd-fbpublic': dict(
  title='Facebook group: the NEW ERA announcement (updated Oct 19 with every new album)',
  html=('<div class="fbg">'
   '<p class="fbg-lead">Same approved post, brought up to date. Your note said &ldquo;We need to add&rdquo;, so now it lists every album since Heritage 2.0: the 10 new ones, plus Shangri La, Lilac Soir&eacute;e, Preppy Soir&eacute;e and Spring Love from the Oh My Mahjong vault. It also has a Papaya Spritz &ldquo;coming soon&rdquo; plug (her album is already live), Find Your Match 10.27, going public, and a follow-ask for the new Facebook Page.</p>'
   '<p class="fbg-m"><b>Timing:</b> post it <b>before Papaya Spritz launches</b> (Oh My Mahjong still says Coming Soon, no date yet), so Papaya gets plugged and the launch earns. Post it while the group is still private, so current members see it first.</p>'
   + pic(ALBUMS_IMG, 'Albums collage: 40+ tile set albums and counting') +
   '<p class="fbg-m">Photo: the albums collage (40+ tile set albums and counting).</p>'
   + box('Post', rd('new-era-post.txt')) + box('First comment', rd('new-era-first-comment.txt')) +
   '<p><b>On your yes, I post it in the group from your account (then switch the group to public a day or two later, separate yes).</b></p></div>'),
  yes='Yes, post it', no='Change something'),
 'l-fb-papaya': dict(
  title='Facebook group: Papaya Spritz launch post (Oh My Mahjong)',
  html=('<div class="fbg">'
   '<p class="fbg-lead">Her launch announcement for the group, in your headline style. It has what she looks like, her official pair (Vivienne), your first dates and racks, &ldquo;her album is already live with 50 matches&rdquo;, and code MAHJMATCH at Oh My Mahjong. Links go in the first comment.</p>'
   '<p class="fbg-m"><b>Launch date: not known yet.</b> Oh My Mahjong still shows Papaya Spritz as Coming Soon (checked Oct 19). HQ says &ldquo;week of Oct 19, date TBA&rdquo;. The post has a <b>[DATE] at [TIME]</b> placeholder. I fill it in the moment the date shows up (launch watch, email watch, or you hearing from Elizabeth) and show you before it goes up.</p>'
   '<div class="fbg-two">' + pic(PAPAYA_IMG, 'Papaya Spritz profile card') + pic(VIV_IMG, 'Vivienne mat with Papaya Spritz tiles') + '</div>'
   '<p class="fbg-m">Photo: her profile card (left). The Vivienne + Papaya photo from Oh My Mahjong (right) can go in as a second photo if you like.</p>'
   + box('Post', rd('papaya-launch-post.txt')) + box('First comment', rd('papaya-launch-first-comment.txt')) +
   '<p><b>On your yes, I post it in the group on launch day.</b></p></div>'),
  yes='Yes, post it on launch day', no='Change something'),
 'l-fb-comingsoon': dict(
  title='Facebook group: reusable "Coming soon" post (any partner brand)',
  html=('<div class="fbg">'
   '<p class="fbg-lead">A fill-in template for upcoming launches from Oh My Mahjong, Miss Mahjong or any partner brand. Dates come only from our launch watch and email watch (or from you). If there&rsquo;s no date yet, it says &ldquo;date TBA&rdquo;.</p>'
   + box('Template post', tpl_post) + box('Template first comment', tpl_comment) +
   '<details class="fbg-d"><summary>See it filled in with what\'s coming up now (from launch watch, Oct 19)</summary>' + box('Example', ex) + '</details>'
   '<p class="fbg-m">How I fill it: ' + H.escape(tpl_rules.replace('\n- ', ' ').lstrip('- ')) + '</p>'
   '<p><b>On your yes, I use this format for coming-soon posts. Each filled-in post still comes to you here for its own yes before I post it in the group.</b></p></div>'),
  yes='Yes, use this format', no='Change something'),
}

# 1) refresh the d-fbpublic DEC entry in place (same id)
k = s.find('["d-fbpublic", ')
assert k > 0, 'd-fbpublic not found'
old, n = json.JSONDecoder().raw_decode(s[k:])
assert old[0] == 'd-fbpublic' and len(old) == 5
it = ITEMS['d-fbpublic']
fallback = 'Updated Oct 19: every album since Heritage 2.0, a Papaya Spritz plug, Find Your Match 10.27, going public, and a follow-ask for the new Facebook Page.'
s = s[:k] + json.dumps(['d-fbpublic', it['title'], fallback, it['yes'], it['no']]) + s[k + n:]

# 2) add the two new items to LOOK
for ID in ('l-fb-comingsoon', 'l-fb-papaya'):
    assert f'"{ID}"' not in s, ID + ' already added'
    assert s.count('LOOK=[[') == 1
    s = s.replace('LOOK=[[', 'LOOK=[' + json.dumps([ITEMS[ID]['title'], '', '', ID]) + ',[', 1)

# 3) Ready for you now: a 'Facebook group' heading + the three items, right after the Papaya launch kit
# insert just before the 'Social: launch week' heading (h-social) in the NOW list
import re
mm = re.search(r'NOW=\[[^\]]*\]', s)
assert mm and '"h-social"' in mm.group(0) and 'h-fbgroup' not in mm.group(0)
nowtxt = mm.group(0).replace('"h-social"', '"h-fbgroup","d-fbpublic","l-fb-papaya","l-fb-comingsoon","h-social"', 1)
s = s[:mm.start()] + nowtxt + s[mm.end():]
# d-fbpublic matches the SOC (social parking) pattern; items listed in NOW stay in Ready for you now
old_soc = "if(SOC.test(id)&&el.parentNode&&el.parentNode.id!=='soclist'"
assert s.count(old_soc) == 1
s = s.replace(old_soc, "if(SOC.test(id)&&!NOW.includes(id)&&el.parentNode&&el.parentNode.id!=='soclist'", 1)

CSS = ('<style>.fbg-lead{font-weight:600;margin:6px 0}.fbg-m{color:var(--mute);font-size:14px;margin:6px 0}'
 '.fbg-l{font:700 13px "DM Sans",sans-serif;text-transform:uppercase;letter-spacing:.06em;color:var(--mute);margin:12px 0 4px}'
 '.fbg-cap{border:1px solid var(--line);border-radius:12px;background:var(--bg);margin:0 0 8px}'
 '.fbg-cap pre{white-space:pre-wrap;word-break:break-word;font:14px/1.45 "DM Sans",sans-serif;margin:0;padding:12px;max-height:320px;overflow:auto}'
 '.fbg-copy{display:block;width:100%;border:0;border-top:1px solid var(--line);background:var(--soft);color:var(--pink);font:700 14px "DM Sans",sans-serif;padding:10px;border-radius:0 0 12px 12px;cursor:pointer}'
 '.fbg-two{display:grid;grid-template-columns:1fr 1fr;gap:8px;align-items:start}.fbg-two .pic{max-width:100%;margin:4px 0}'
 '.fbg-d>summary{cursor:pointer;font-weight:700;color:var(--pink);padding:8px 0}</style>')
JS = ('<script>(function(){const IT=' + json.dumps({k: {'h': v['html'], 'y': v['yes'], 'n': v['no']} for k, v in ITEMS.items()}) + ';'
 'function head(){const nl=document.getElementById("nowlist");if(!nl||document.querySelector(\'[data-id="h-fbgroup"]\'))return;const h=document.createElement("h3");h.dataset.id="h-fbgroup";h.className="nowh";h.textContent="Facebook group: post before Papaya launches";nl.prepend(h)}'
 'function inject(){head();Object.keys(IT).forEach(id=>{const el=document.querySelector(\'.item[data-id="\'+id+\'"]\');if(!el||el.querySelector(".fbg"))return;const d=el.querySelector(".desc");if(!d)return;const w=document.createElement("div");w.innerHTML=IT[id].h;d.replaceWith(w.firstElementChild);'
 'const bs=el.querySelector(".btns");if(bs){bs.innerHTML=\'<button class="yes" data-v="ok" type="button"></button><button class="no" data-v="no" type="button"></button>\';bs.children[0].textContent=IT[id].y;bs.children[1].textContent=IT[id].n}const ta=el.querySelector("textarea");if(ta)ta.placeholder="What should change? (optional)"})}'
 'document.addEventListener("click",e=>{const c=e.target.closest(".fbg-copy");if(!c)return;e.preventDefault();e.stopPropagation();const pre=c.parentNode.querySelector("pre");const lab=c.textContent;'
 'const sel=()=>{const r=document.createRange();r.selectNodeContents(pre);const g=getSelection();g.removeAllRanges();g.addRange(r);c.textContent="Selected, tap Copy"};'
 'if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(pre.textContent).then(()=>{c.textContent="Copied ✓";setTimeout(()=>{c.textContent=lab},1500)},sel)}else sel()},true);'
 'inject();setInterval(inject,1500);})();</script>')
i = s.rfind('</body>')
s = s[:i] + CSS + JS + s[i:] if i >= 0 else s + CSS + JS
open(OUT, 'w', encoding='utf-8').write(s)
print('ok', len(s))
