# Brand watch rules (binding; read FIRST every partner-watch run; overrides the task prompt)
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
d. Album sets / Find Your Mat-ch items also get the story frames (existing restock playbook).
No hype: never "goes fast"/"sells out"; "Set your alarms!" is fine.

## 3. Checks
- scripts/checks/launch_48h_check.py (front door, every chat, every message) lists partner items within 48h that are not posted/skipped.
