# Brand watch rules (binding; read FIRST every partner-watch run; overrides the task prompt)

## 0. WHO TALKS TO TIFFANY (Tiffany Nov 10 8:02am: "I don't go to partner watch... They've got to report back to someone like you who then reports to me.")
The partner watch is a background worker. It NEVER messages Tiffany (no SendUserMessage, no PushNotification, overriding any line in its task prompt). It writes:
- the list (config/brand-watch-curated.json + HQ Brand Watch tab),
- NOW items + their draft group posts into config/launch-actions.json ("drafted") and docs/social/,
- one line at the TOP of docs/DESK.md "Main: brand watch <time>: N NOW items ready (launch-actions.json)".
The MAIN chat reports to her: its front door shows every NOW item (scripts/checks/launch_48h_check.py), and Main checks in after each watch run (9:23am, 1:23pm, 6:23pm) and brings her the drafts for a yes.
Tiffany Nov 10 7:59am, after TdT Domino Blonde (caught Mon 1:30pm, drops Tue 4pm CT) was filed and never acted on:
"something that is launching today at 4 p.m. that gets caught the day before can't go on next week's partner launch document. So the partner watch has to understand dates and urgency... people are expecting us to do it for them... this is a test right now to see if you guys can actually keep up with how fast this world moves."

## 1. Every item gets a date and an urgency, every run
For each partner item found (store, email, Instagram): compute hours until it happens (drop / restock / preorder open / sale end) in America/New_York.
- **NOW: live already, or happening within 48h.** ACT THIS RUN (section 2). Never only file it.
- **SOON: 2 to 7 days.** Goes in this week's watch + the next Monday codes post if Monday is before it; if Monday's post already went out, it gets its own group post the day before.
- **LATER: more than 7 days or undated.** Watch tab + calendar only.
A Monday codes post that already went out does NOT cover anything caught after it. "We already posted codes" is never a reason to skip.

## 2. What ACT means (NOW items)
a. Draft a same-day FACEBOOK GROUP post: docs/social/<brand-slug>-<product-slug>-<date>.post.txt with the brand's own photos (assets/social/<brand-slug>-<product-slug>/), the drop time, buy links to the BRAND's product page with our code/affiliate link (never our own page), and the code typed: "use code MAHJMATCH to save X%". The Tigre de Tartán image-only rule is for the WEBSITE/Google only; in our own group the code and name are typed (Tiffany Nov 10 7:49am).
b. Add it to config/launch-actions.json as "drafted" (key = scripts/checks/launch_48h_check.py's key) so every chat's front door shows it until it is posted or she says skip.
c. Message Tiffany the same run: first line "<Brand> <product> drops <day time>. Group post ready for your yes:" + the text + photos. Day before AND morning of.
d. NO STORY FRAMES, REELS OR GRAPHICS unless Tiffany asks for them for that item (Tiffany Nov 10 8:01am: "you guys are then just immediately building a story frame, which I don't believe I ever told you to do... burning up usage... It's not, let's go build a story frame, but not tell Tiffany. That is absolutely out of order."). The list and the group post come first; she reshares brand content herself from the list.
No hype: never "goes fast"/"sells out"; "Set your alarms!" is fine.

## 3. Checks
- scripts/checks/launch_48h_check.py (front door, every chat, every message) lists partner items within 48h that are not posted/skipped.

## 4. Where everything goes (the flow)
Sources (3x daily): partner stores (products.json diff), email (mahjmatchmaker@ + tiffanybrie@), partner Instagram (Planoly), Sunday release page.
1. LIST FIRST: config/brand-watch-curated.json (this_week / coming_soon / just_dropped / sales), each with date, time, brand, what, buy link (brand page + our code), source link (their post, for her reshares), urgency NOW / SOON / LATER.
2. HQ Brand Watch tab (hq/brandWatch) mirrors the list. This is her social cheat sheet: brand post links she can reshare.
3. WEBSITE "Brand Watch" page (planned, Tiffany Nov 10): the same list, live, public; group + email list + page = where people get it.
4. GROUP: Monday codes post carries the week; NOW items caught after Monday get their own group post (section 2), on her yes.
5. Tiffany is told the same run for NOW items (one message: what, when, draft post). SOON/LATER: list only, no message.
Nothing else gets built automatically.
