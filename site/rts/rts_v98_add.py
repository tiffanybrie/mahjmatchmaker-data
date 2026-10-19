import json, re, sys
SRC = sys.argv[1]; OUT = sys.argv[2]
s = open(SRC, encoding='utf-8').read()
CAP = open('/tmp/claude-0/-home-claude/801d31e6-4a74-59be-8637-eb67bfa0e99e/scratchpad/tr3/caption.txt', encoding='utf-8').read().strip()

def esc(x):
    return x.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

VID = '/_blob/7c47edbf19096471894606c9d73c6aa0'
COVER = '/_blob/17c5186bd5cb2cff2447c79e01926afd'
CD = [('7', 'Tue 10/20', '/_blob/7560a4c6e486f16a51684dde86986871', 'Your tiles are about to get a dating app.'),
      ('6', 'Wed 10/21', '/_blob/2925f8daaa6bfe2450b86c741912677f', 'His bio says “not into matching.” We\'ll see.'),
      ('5', 'Thu 10/22', '/_blob/96c49d952c0c9c4ae368d79bb20320e9', 'Single tiles in your area are looking for a mat.'),
      ('4', 'Fri 10/23', '/_blob/9ce65f7b7c7d05f93e1551822fd90b8e', 'Already own a mat? It\'s been getting matches too.'),
      ('3', 'Sat 10/24', '/_blob/aad4c60e8e75b0b249bb9410cd067923', 'Racks are invited. Obviously.'),
      ('2', 'Sun 10/25', '/_blob/71ab18970cdd6ec986e09b8ad7c38389', 'Hundreds of mats are fixing their hair right now.'),
      ('1', 'Mon 10/26', '/_blob/0d5a1978c114e90dad4750cc6ebf10bd', 'Tomorrow, your tiles meet their match.'),
      ('LIVE', 'Tue 10/27', '/_blob/3547831b82cf5eefeb2841d0b557991e', 'Find Your Match is here. Link in bio.')]

def jk(item, key, label, a, b):
    return (f'<div class="jk" data-item="{item}" data-key="{key}"><div class="jkl">{label}</div>'
            f'<button type="button" class="jkb" data-pick="A"><b>A</b> {a}<i>in the video now</i></button>'
            f'<button type="button" class="jkb" data-pick="B"><b>B</b> {b}</button></div>')

TRAILER = f'''
<div class="pp">
<p class="ppl">This is the FIRST post of launch week. Everything you need is on this card, in order.</p>
<h4>1. The video (43 seconds, silent until you add the song)</h4>
<video class="vid" controls playsinline preload="metadata" src="{VID}"></video>
<p><a class="dl" href="{VID}" download="mahj-matchmaker-2-0-trailer.mp4">Download the video</a></p>
<p class="mut">What changed since you watched it: every match now shows its racks the same way (rack photo across the bottom of the mat + a rack line under it), and Coquette's part is now a set of dating profiles. Everything else is exactly what you liked.</p>
<table class="pt"><tr><th>Match</th><th>Racks shown</th><th>Why these racks</th></tr>
<tr><td>Fleur (LoveShackFancy)</td><td>Oh My Mahjong Pink Quartz</td><td>Rack #1 on Fleur's card in the Coquette album, and one of Coquette's 3 final racks.</td></tr>
<tr><td>Martha &amp; Mae (Middle &amp; Main)</td><td>Middle &amp; Main White Lace</td><td>Unchanged. Your "PERFECT" rack for Coquette (Oct 16).</td></tr>
<tr><td>Chantilly (Oh My Mahjong)</td><td>Bird &amp; Bamboo Lilac</td><td>On Chantilly's album card, one of Coquette's 3 final racks, and it picks up Chantilly's lilac.</td></tr></table>

<h4>2. Pick the jokes (A is in the video now)</h4>
<p class="mut">Tap the one you like for each card. If you pick any B, I re-render the video with it and swap it in here.</p>
{jk("post-trailer","coquette","Coquette's profile · DEALBREAKER","“Isn't that a lot of pink?”","LOVE LANGUAGE: “Bows. More bows.”")}
{jk("post-trailer","fleur","Fleur + Pink Quartz racks · HOW WE MET","“Our moms set us up.” (Her official pair. Obviously.)","“Same designer. It's basically arranged.”")}
{jk("post-trailer","mm","Martha &amp; Mae + White Lace racks · FIRST DATE","“Wore scallops. Brought lace.” She had to sit down.","GREEN FLAG: “Brought lace to the first date.”")}
{jk("post-trailer","ch","Chantilly + Lilac racks · PEOPLE ALWAYS ASK","“Are you two related?” Same lilac. Same powder blue.","FIRST DATE: “Showed up in her exact lilac and powder blue. Total coincidence.”")}

<h4>3. The caption (exactly what goes in Planoly)</h4>
<pre class="cap" id="cap-trailer">{esc(CAP)}</pre>
<button type="button" class="cpy" data-copy="cap-trailer">Copy caption</button>
<p class="mut">It's already pasted into the Planoly draft for you. No discount code in this one, so no #ad needed.</p>

<h4>4. The song</h4>
<div class="song"><b>“Love Shack” by The B-52's</b><br>Yes, the Love Shack song (a wink at LoveShackFancy, since Coquette is the star).<br>Start the clip at the chorus, the part where they sing <i>“Love shack, baby, love shack!”</i></div>
<p class="mut">Backup if Love Shack doesn't show up in Instagram's music search: <b>“Kiss Me” by Sixpence None the Richer</b>, starting at the first chorus.</p>
<p class="mut">Why you add it in Instagram: Planoly can't attach music to this account (the Instagram connection doesn't include Instagram's music library), so the song goes on in the Instagram app right before you share.</p>

<h4>5. The details</h4>
<table class="pt">
<tr><td>Post date</td><td><b>Tuesday, October 20, 11:30 AM</b> (your time, Eastern)</td></tr>
<tr><td>Where</td><td>Instagram Reel, shown on your grid (not Reels-only). Then share it to your Story and save it to a Highlight.</td></tr>
<tr><td>Cover</td><td>The opening frame: “Mahj Matchmaker 2.0 is here.” (shown below; it's already set as the cover in Planoly). In Instagram, it's the frame at about 0:02.</td></tr>
<tr><td>Link in bio</td><td>Before you post, make sure your bio link is https://www.mahjmatchmaker.com/mahjong-tile-matches (the caption says "link in bio").</td></tr>
<tr><td>Planoly</td><td><b>Already in Planoly as an UNSCHEDULED DRAFT</b> (video + caption + cover). It's a reminder post, so Planoly won't publish it by itself. It just pings your phone at 11:30 so you can add the song and share.</td></tr>
</table>
<img class="pic" src="{COVER}" alt="Cover frame" style="max-width:220px">

<h4>6. Tap by tap</h4>
<p class="mut"><b>Today (2 minutes):</b></p>
<ol class="steps">
<li>Open the Planoly app (or planoly.com) and go to the <b>Mahj Matchmaker</b> workspace.</li>
<li>Open <b>Drafts</b> (unscheduled posts). Tap the trailer draft (the one that starts “Mahj Matchmaker 2.0 is here 💘”).</li>
<li>Tap the date and pick <b>Tue, Oct 20, 11:30 AM</b>.</li>
<li>Leave it as a <b>reminder</b> (auto-publish off), then tap <b>Schedule</b>.</li>
</ol>
<p class="mut"><b>Tuesday at 11:30 when Planoly pings you:</b></p>
<ol class="steps" start="5">
<li>Tap the Planoly notification, then tap <b>Post to Instagram</b> (Planoly copies the caption for you).</li>
<li>Instagram opens. Choose <b>Reel</b> and pick the trailer video.</li>
<li>Tap the <b>music note</b> (Audio), search <b>Love Shack</b>, and pick the one by <b>The B-52's</b>.</li>
<li>Drag the clip slider to the chorus (“Love shack, baby, love shack!”), then tap <b>Done</b>, then <b>Next</b>.</li>
<li>Tap <b>Edit cover</b> and slide to the opening “2.0 is here.” frame. Tap <b>Done</b>.</li>
<li>Press and hold in the caption box and tap <b>Paste</b>. Check it starts with “Mahj Matchmaker 2.0 is here 💘”.</li>
<li>Leave “Share to Reels” and “Also share to feed” on. Tap <b>Share</b>.</li>
<li>When it's up, tap the paper airplane under the reel, then <b>Add to story</b>, then <b>Your story</b>.</li>
<li>Open that story, tap <b>Highlight</b>, and save it to a new Highlight called <b>2.0</b>.</li>
</ol>
<p class="mut">Tap the green button when it's posted (or if you'd rather I re-render with any B jokes first, pick them above and tap the pink button).</p>
</div>'''

cdgrid = ''.join(f'<figure class="cdf"><img class="pic" src="{u}" alt="Countdown {n}"><figcaption><b>{d}</b> · {"LIVE" if n=="LIVE" else n+(" day" if n=="1" else " days")}<br><a class="dl" href="{u}" download="countdown-{n}.jpg">Download</a></figcaption></figure>' for n, d, u, l in CD)
cdrows = ''.join(f'<tr><td><b>{d}</b></td><td>{"LIVE today" if n=="LIVE" else n+(" day" if n=="1" else " days")}</td><td>{l}</td></tr>' for n, d, u, l in CD)

COUNT = f'''
<div class="pp">
<p class="ppl">A daily Instagram story from the trailer to launch day. One graphic a day + Instagram's Countdown sticker. About a minute a day.</p>
<h4>The plan</h4>
<table class="pt">
<tr><td>Starts</td><td><b>Tue 10/20</b>, right after the trailer goes up (7 days out). Last countdown story Mon 10/26. Launch-day story Tue 10/27.</td></tr>
<tr><td>Where</td><td>Instagram Stories only. No extra feed posts: launch week already has the trailer, Pippa and Smith, so this stays light.</td></tr>
<tr><td>When</td><td>Any time that day. Easiest: right after lunch. On trailer day, post it after the trailer.</td></tr>
<tr><td>Sticker</td><td><b>Countdown</b> sticker. Title: <b>FIND YOUR MATCH</b>. End: <b>Tue, Oct 27, 2026 · 9:00 AM</b> (when the finale posts). Make it once on day 1; every other day you re-use the same one.</td></tr>
<tr><td>Why it works</td><td>People who tap “Remind me” on the sticker get an Instagram alert at 9:00 AM on launch day. Each card teases a little (dating app, swiping, racks, "already own a mat?") without showing Find Your Match itself.</td></tr>
</table>
<h4>The 8 graphics (tap to see big, or download)</h4>
<div class="cdg">{cdgrid}</div>
<h4>What each one says</h4>
<table class="pt"><tr><th>Day</th><th>Big number</th><th>Text on the card</th></tr>{cdrows}</table>
<p class="mut">The text is on the graphic, so you don't type anything except the sticker title on day 1.</p>
<h4>Tap by tap</h4>
<p class="mut"><b>Once, today:</b> download all 8 graphics to your phone (the Download links above).</p>
<p class="mut"><b>Day 1, Tue 10/20 (making the sticker):</b></p>
<ol class="steps">
<li>In Instagram, tap <b>+</b> then <b>Story</b>, and pick <b>countdown-7</b> from your camera roll.</li>
<li>Tap the <b>sticker</b> icon (the square smiley at the top) and tap <b>Countdown</b>.</li>
<li>Type the title: <b>FIND YOUR MATCH</b></li>
<li>Tap the date, set <b>October 27, 2026</b>, turn off “All day”, and set <b>9:00 AM</b>. Tap <b>Done</b>.</li>
<li>Drag the sticker into the empty space between the text and the mahjmatchmaker logo. Pinch it so it fits.</li>
<li>Tap <b>Your story</b> to share.</li>
</ol>
<p class="mut"><b>Days 2 to 7 (Wed 10/21 to Mon 10/26):</b></p>
<ol class="steps" start="7">
<li>Tap <b>+</b>, <b>Story</b>, and pick that day's graphic (countdown-6, then 5, 4, 3, 2, 1).</li>
<li>Tap the <b>sticker</b> icon, tap <b>Countdown</b>, and tap your <b>FIND YOUR MATCH</b> countdown under “Your countdowns” (don't make a new one).</li>
<li>Drag it into the empty space and tap <b>Your story</b>.</li>
</ol>
<p class="mut"><b>Launch day, Tue 10/27 (no countdown, it ends at 9:00):</b></p>
<ol class="steps" start="10">
<li>After 9:00 AM, tap <b>+</b>, <b>Story</b>, and pick <b>countdown-LIVE</b>.</li>
<li>Tap the <b>sticker</b> icon, tap <b>Link</b>, paste <b>https://www.mahjmatchmaker.com</b>, and change the sticker text to <b>FIND YOUR MATCH</b>.</li>
<li>Drag it into the empty space and tap <b>Your story</b>.</li>
</ol>
<p class="mut">Optional: save all of them to the <b>2.0</b> Highlight with the trailer. Nothing here is scheduled or posted for you; Instagram stickers can only be added in the app. It's also on the HQ launch plan for each day so it doesn't get forgotten.</p>
</div>'''

EPJ = f'''
<div class="pp">
<p class="ppl">Same humor bar as the trailer, for the other three launch-week episodes. These are new lines for the cards in each video. Tap A or B for each one; I re-render the episode with your picks before its post day. (The videos on their own cards still show the old lines.)</p>
<h4>Pippa · Ep 6 “Two Suitors” · Thu 10/22</h4>
{jk("ep-jokes","pippa-bio","Pippa's profile (under her name)","IDEAL FIRST DATE: “A margarita. Second date: another margarita.”","“Will RSVP yes to anything with a salt rim.”")}
{jk("ep-jokes","pippa-hampton","Suitor 1 · Hampton (now: “Lime, turquoise, garden party. I make your backs pop.”)","“I'm a garden party.” Pippa: “Love that. Is there tequila?”","“Brought garden party energy. Wore loafers. To a margarita party.”")}
{jk("ep-jokes","pippa-delilah","Suitor 2 · Delilah (now: “Turquoise and red, babe. I'm basically a fiesta.”)","“I'm basically a fiesta.” Pippa: “Say less.”","“Turquoise and red. Showed up with a piñata.”")}
{jk("ep-jokes","pippa-think","Thought bubble (now: “Garden party or fiesta? Somebody pour me a margarita.”)","“Garden party or fiesta? …Garden fiesta?”","“Two suitors. One party girl. Zero chill.”")}
{jk("ep-jokes","pippa-fruit","Plus one · Fruit Stand (now: “Lemons, limes, sunny stripes. I showed up with snacks.”)","“Brought lemons AND limes to a margarita party. Marry him.”","“Showed up with snacks. Game over.”")}
<h4>Smith · Ep 8 “Swipe Right on Smith” · Sat 10/24</h4>
{jk("ep-jokes","smith-bio","Smith's profile (under his name)","“Woodgrain backs. Owns six navy quarter-zips.”","“Looking for someone who appreciates a good grain.”")}
{jk("ep-jokes","smith-hampton","Hampton, swiped left (now: “Gorgeous, just not his type. Next!”)","“Gorgeous. But he's a navy guy. Respectfully, left.”","“She wanted brunch. He wanted a duck blind.”")}
{jk("ep-jokes","smith-hawthorne","Hawthorne (now: “Navy and plum? Smith is blushing.”)","“Navy AND plum? He had to loosen his tie.”","“Navy and plum. He's texting his mom.”")}
{jk("ep-jokes","smith-pair","It's a match (now: “It's a match! Smith + Hawthorne, the official pair.”)","“The official pair. Their moms already booked the venue.”","“The official pair. Obviously.”")}
{jk("ep-jokes","smith-nvl","Navy Vegan Leather (now: “Tall, dark and tailored.”)","“Tall, dark, tailored. Also vegan.”","“Matches his quarter-zip. Instant chemistry.”")}
{jk("ep-jokes","smith-end","Last card (now: “Smith has 26 matches. Come meet them all.”)","“26 matches. Somebody tell his mom.”","“26 matches. He's going to need a bigger calendar.”")}
<h4>Coquette finale · Ep 13 “Meet the Parents” · Tue 10/27</h4>
{jk("ep-jokes","coq-parents","The parents ask (now: “So… who's the lucky mat?”)","“So… what does this mat do for a living?”","“Is she… a nice mat?”")}
{jk("ep-jokes","coq-fleur","Fleur (now: “The official pair mat. A garden of pinks.”)","“Same designer. Mom basically raised her.”","“Official pair. Dad already likes her more than Coquette.”")}
{jk("ep-jokes","coq-lace","White Lace rack (now: “The one we all want. It sold out and ghosted us.”)","“Sold out. Ghosted us. Came back. Mom: ‘I like this one.’”","“The rack everyone wants is back. Act natural.”")}
{jk("ep-jokes","coq-wink","The bubble (now: “Nice rack. *wink*”)","Keep “Nice rack. *wink*”","Dad: “Sturdy.” Mom: “Lace!” Coquette: “I KNOW.”")}
{jk("ep-jokes","coq-end","Last line (now: “And they lived happily ever after.”)","“And they lived happily ever after. Racks included.”","“Happily ever after. The racks moved in first.”")}
<p class="mut">Heads up on the finale: an earlier note of yours says it shouldn't star Fleur (the official pair) and should feature Martha &amp; Mae, like your own Coquette reel. Right now it still stars Fleur. Tell me in the box if you want that fixed in the re-render too.</p>
</div>'''

EXTRA = {'post-trailer': TRAILER, 'post-countdown': COUNT, 'ep-jokes': EPJ}

new_dec = [
    ["post-trailer", "Post this reel · Tue 10/20 11:30am · Mahj Matchmaker 2.0 trailer", "", "Looks good, I'll post it", "Change something"],
    ["post-countdown", "Countdown · daily stories Tue 10/20 to launch day", "", "Got it, I'll post them", "Change something"],
    ["ep-jokes", "Funnier profiles for Pippa, Smith and the Coquette finale (pick A or B)", "", "Use my picks", "Change something"],
]
dec_js = ','.join(json.dumps(x) for x in new_dec) + ','
assert s.count('const DEC=[') == 1
s = s.replace('const DEC=[', 'const DEC=[' + dec_js, 1)
# videos: register new blob as a video
s = s.replace('isVid=u=>/\\.mp4$/i.test(u)||/_blob\\/(84855|', 'isVid=u=>/\\.mp4$/i.test(u)||/_blob\\/(7c47e|84855|', 1)
assert '7c47e|84855' in s
# NOW list: new items replace the old trailer item; old trailer item hidden
old = 'NOW=["h-social", "s2-trailer", '
assert s.count(old) == 1
s = s.replace(old, 'NOW=["h-social", "post-trailer", "post-countdown", "ep-jokes", ', 1)
s = s.replace('HIDE=/^(d-ep00|', 'HIDE=/^(s2-trailer|d-ep00|', 1)
assert 'HIDE=/^(s2-trailer|' in s

css = ('<style>.pp h4{font:400 19px Caprasimo,serif;color:#064587;margin:18px 0 6px}.pp p{margin:6px 0}.ppl{font-weight:700}.mut{color:var(--mute);font-size:14px}'
       '.pt{width:100%;border-collapse:collapse;font-size:14px;margin:6px 0}.pt td,.pt th{border-top:1px solid var(--line);padding:7px 6px;text-align:left;vertical-align:top}.pt th{font-size:12px;text-transform:uppercase;letter-spacing:.05em;color:var(--mute)}'
       '.cap{white-space:pre-wrap;word-break:break-word;background:var(--bg);border:1px solid var(--line);border-radius:12px;padding:12px;font:14px/1.45 "DM Sans",sans-serif;user-select:all;-webkit-user-select:all;margin:6px 0}'
       '.cpy{border:0;border-radius:99px;padding:10px 18px;font:700 14px "DM Sans",sans-serif;background:#064587;color:#fff;cursor:pointer}'
       '.song{background:var(--soft);border-radius:12px;padding:12px 14px;font-size:15px}.dl{font-weight:700;color:var(--pink)}'
       '.steps{padding-left:22px;margin:6px 0}.steps li{margin:6px 0}'
       '.jk{border:1px solid var(--line);border-radius:12px;padding:10px;margin:8px 0}.jkl{font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:.05em;color:var(--mute);margin-bottom:6px}'
       '.jkb{display:block;width:100%;text-align:left;border:1px solid var(--line);background:var(--bg);color:var(--ink);border-radius:10px;padding:9px 10px;margin:5px 0;font:15px/1.35 "DM Sans",sans-serif;cursor:pointer}.jkb b{color:var(--pink);margin-right:6px}.jkb i{display:block;font-size:12px;color:var(--mute);font-style:normal}.jkb.on{border-color:var(--pink);box-shadow:0 0 0 2px rgba(226,70,143,.35)}'
       '.cdg{display:grid;grid-template-columns:repeat(4,1fr);gap:8px}.cdf{margin:0}.cdf img.pic{margin:0;border-radius:8px}.cdf figcaption{font-size:12px;line-height:1.3;margin-top:3px}@media(max-width:480px){.cdg{grid-template-columns:repeat(2,1fr)}}</style>')

js = ('<script>(function(){const X=' + json.dumps(EXTRA) + ';'
      'function inject(){Object.keys(X).forEach(id=>{const el=document.querySelector(\'.item[data-id="\'+id+\'"]\');if(!el||el.querySelector(".pp"))return;const d=el.querySelector(".desc");const w=document.createElement("div");w.innerHTML=X[id];d.replaceWith(w.firstElementChild);marks()})}'
      'function marks(){document.querySelectorAll(".jk").forEach(j=>{const st=(typeof state!=="undefined"&&state[j.dataset.item])||{};const p=((st.jokes||{})[j.dataset.key])||"";j.querySelectorAll(".jkb").forEach(b=>b.classList.toggle("on",b.dataset.pick===p))})}'
      'document.addEventListener("click",e=>{const c=e.target.closest("[data-copy]");if(c){e.preventDefault();const t=document.getElementById(c.dataset.copy).textContent;const ok=()=>{c.textContent="Copied ✓";setTimeout(()=>c.textContent="Copy caption",1800)};if(navigator.clipboard)navigator.clipboard.writeText(t).then(ok,()=>{});else{const r=document.createRange();r.selectNodeContents(document.getElementById(c.dataset.copy));const sl=getSelection();sl.removeAllRanges();sl.addRange(r);document.execCommand("copy");ok()}return}'
      'const a=e.target.closest("a.dl");if(a){e.preventDefault();const lab=a.textContent;a.textContent="Getting it…";(async()=>{try{const dl=await claude.use("downloads");if(!dl){a.textContent="Press and hold the picture to save it";return}const bl=await (await fetch(a.getAttribute("href"))).blob();await dl.save({filename:a.getAttribute("download"),data:bl});a.textContent="Saved ✓"}catch(x){a.textContent=(x&&x.code==="declined")?lab:"Could not save, try again"}setTimeout(()=>{a.textContent=lab},4000)})();return}'
      'const b=e.target.closest(".jkb");if(!b)return;e.preventDefault();const j=b.closest(".jk");const id=j.dataset.item;const st=(state[id]||{});const jo=Object.assign({},st.jokes||{});jo[j.dataset.key]=b.dataset.pick;save(id,{jokes:jo});marks()},true);'
      'inject();setInterval(()=>{inject();marks()},1500);})();</script>')

i = s.rfind('</body>')
s = s[:i] + css + js + s[i:]
open(OUT, 'w', encoding='utf-8').write(s)
print('ok', len(s))
