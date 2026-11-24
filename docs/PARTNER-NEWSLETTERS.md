# Partner newsletters: get mahjmatchmaker@gmail.com on every partner's list

Tiffany, Nov 6 5:22pm: "subscribe us to every newsletter for all of the partners... any we've never received a newsletter from, go back and get on their list. You have permission." Standing yes: signing up mahjmatchmaker@gmail.com to a PARTNER's email list needs no further OK (email only, never SMS/phone, never a purchase, never an account password).
Why: launches like Cabana Club (CMC) and Bam Bird's MCM Olive restock were missed because we weren't on their lists.

## How to resume (any chat or scheduled task)
1. Server-side signup does NOT work (Nov 6: every Shopify /contact POST returned 403). This is a Chrome job: one driver at a time, close your tab.
NOTE 2026-11-08: automated Chrome submits on Shopify footer forms (Amahj, Bam!, Mahj Mood) silently fail (Shopify bot protection); only popups (Klaviyo etc.) have worked. Remaining TODO rows: try only if a popup appears; otherwise it is a 10-second job for Tiffany on her phone.
2. For each row marked TODO: open the store homepage, use the footer "Subscribe / Join our list" email box (or the popup), enter mahjmatchmaker@gmail.com, submit. Decline SMS steps. If a captcha appears, stop on that brand (never solve captchas) and mark "captcha: Tiffany 10s".
3. Mark the row `signed up <date>`; then within 1 day check Gmail (from:<domain>) for a welcome/confirm email; click a double-opt-in confirm link if one comes (it's our own subscription). Mark `confirmed`.
4. Weekly (Monday desk cleanup): any partner with no email in 30 days -> recheck the signup.
5. New partner onboarding = add a row here and sign up the same day.

## Always open the www address
Middle & Main's store is live at https://www.middleandmainmahjong.com. The bare domain (no www) shows Shopify's "This store is currently unavailable" page. That page is NOT the store and does not mean they closed: Tiffany has corrected this twice (Nov 8, Nov 16). Open every brand by the www address our links use.

## Chrome method that works (Nov 8 update)
- Popups (Shopify Forms / Klaviyo): fill the email with form_input (typing into some fields triggers another browser extension's overlay that blocks the tab; navigate away to recover), click the button, decline SMS.
- Footer forms: work on stores WITHOUT the hCaptcha badge (Mahj Squad: URL gets ?customer_posted=true) and on Squarespace sites (Amanda Toppe, Wren). On Shopify stores showing the hCaptcha badge the submit is silently dropped: that is a 10-second job for Tiffany on her phone.
- Shopify double opt-in mails come from store+NNN@*.shopifyemail.com, not the brand domain: search Gmail by brand name too.

## Chrome method that works (Nov 7)
Shopify footer forms submitted by script or Enter do NOT confirm (page shows an hCaptcha badge; no customer_posted reload). Use the brand's signup POPUP instead (Klaviyo/Privy/Attentive): navigate, wait ~8s for it, screenshot, click the email box, type, click the button, then close/Escape the SMS step. ~2 browser calls per brand. If no popup shows, note it and move on.

Gmail recheck 2026-11-10: still no welcome/confirm email for Bam Bird, Let's Mahj On, Mahj Squad, Virora, Wren Mats, YMI (searched brand names + shopifyemail/klaviyo). No TODO/NOT YET rows left; FAILED rows = Tiffany 10s on her phone.

Nov 12 run: added the 5 partners from OVERDUE (YOLO, Maison Mahj, Noli June, Mahj Pit, Mahjong by SI) per step 5. Unattended scheduled runs can be stopped by the safety check at the Submit click (YOLO popup Nov 12); those rows stay TODO for an attended chat or Tiffany. Gmail recheck Nov 12: still nothing from Bam Bird, Let's Mahj On, Mahj Squad, Virora, Wren Mats, YMI.

## Status (Nov 16 night full check)
Rule from Nov 16: "receiving" means a MARKETING/newsletter email reached mahjmatchmaker@ in the last 30 days. Affiliate order, approval and payout mail, and a single old email, do not count. Every brand gets rechecked weekly.
Sources: brand list = codes-page brands (google-codes-audit/brand-pages-verified.csv) + config/brand-watch-curated.json + config/social/ig-handles.json. Last email = newest non-affiliate email from the brand in mahjmatchmaker@ (searched by domain and by brand name, since Shopify Email sends from store+NNN@*.shopifyemail.com).

| Brand | Store | Last email | Status |
|---|---|---|---|
| Mac + Miller | macandmillermahjong.com | Nov 7 | receiving |
| Britt Mills | brittmillsdesign.com | Oct 28 | receiving |
| Anders Ruff | andersruff.com | Oct 20 | receiving, but stale (only affiliate notices since). Nov 16: their AR Insiders Club signup form does not load on the site, so no re-signup possible; recheck |
| Bam Bird | bambirdboutique.com | Aug 12 | signed up 2026-11-23 ~11:20pm by Tiffany (captcha); waiting for the first email, check Nov 24 |
| Peace Love Mahjong | peacelovemahjong.com | Nov 10 | receiving |
| Miss Mahjong | missmahjong.com | Nov 10 | receiving |
| Royal Mahjong Society | theroyalmahjongsociety.com | Nov 14 | receiving |
| Oh My Mahjong | ohmymahjong.com | Oct 23 | signed up 2026-11-23 ~11:20pm by Tiffany (captcha); waiting for the first email, check Nov 24 |
| Soirée All Day | soireeallday.co | Nov 9 | receiving |
| Sweet Jojo | sweetjojomahjong.com | Nov 14 | receiving |
| I Love Mahj | ilovemahj.com | - | no newsletter: online game platform, no email box without an account (rechecked Nov 16) |
| Charleston Mahjong Club | charlestonmahjongclub.com | Nov 10 | receiving |
| Amahj | amahjline.com | none | receiving (welcome arrived Nov 23 11:2xpm) |
| Amanda Toppe | amandatoppeart.com | Nov 8 | receiving |
| Bam! Let's Mahjong | bamletsmahjong.com | none | signed up 2026-11-23 ~11:20pm by Tiffany (captcha); waiting for the first email, check Nov 24 |
| Bespoke | bespokemahjong.com | Nov 7 | receiving |
| Bird & Bamboo | birdandbamboo.com | Nov 11 | receiving |
| Fait à Main | fait-a-main.com | Nov 8 | receiving (welcome only so far) |
| Hip Hip | hiphipmahjong.com | - | no newsletter: no signup form on the site (rechecked Nov 16) |
| Let's Be Besties | letsbebesties.com | none | receiving (welcome arrived Nov 23 11:2xpm) |
| Let's Mahj On | letsmahj-on.com | none | signed up 2026-11-16 (footer form, customer_posted=true "Thanks for subscribing"); the Nov 8 popup signup never delivered |
| Mahj Mood | mahjmood.com | Oct 28 (affiliate only) | receiving (welcome arrived Nov 23 11:2xpm) |
| Mahj Squad | mahjsquad.com | none | signed up 2026-11-23 ~11:20pm by Tiffany (captcha); waiting for the first email, check Nov 24 |
| Mahj & Vine | mahjandvine.com | Nov 8 | receiving (welcome) |
| The Mahjong Co. | mahjongco.com | Nov 8 | receiving (confirmed) |
| Mahjong Register | mahjongregister.com | - | no newsletter: no signup form on the site (rechecked Nov 16) |
| Mahjong Studios | mahjongstudios.com | Nov 8 | receiving |
| Middle & Main | www.middleandmainmahjong.com | none yet | signed up 2026-11-23 ~11:20pm by Tiffany (captcha); waiting for the first email, check Nov 24 |
| Mini Mahjer | minimahjer.com | Nov 16 | signed up 2026-11-16 (popup, first name + email; SMS step skipped); welcome email arrived 11:43pm ET |
| My Fair | myfairmahjong.com | none | signed up 2026-11-23 ~11:20pm by Tiffany (captcha); waiting for the first email, check Nov 24 |
| The Mahjong Press | themahjongpress.com | none | signed up 2026-11-23 ~11:20pm by Tiffany (captcha); waiting for the first email, check Nov 24 |
| Tigre de Tartán | tigredetartan.com | affiliate only | signed up 2026-11-23 ~11:20pm by Tiffany (captcha); waiting for the first email, check Nov 24 |
| Virora | viroramahjong.com | affiliate only | needs Tiffany: Nov 8 popup signup never confirmed; site now shows no email box (popup suppressed, no footer form) |
| Wren Mats | wrenmats.com | - | no newsletter: their own form says it "needs a storage option" (signup not connected), Nov 16 |
| Splash of Color | splashofcolorco.com | none | signed up 2026-11-23 ~11:20pm by Tiffany (captcha); waiting for the first email, check Nov 24 |
| Yellow Mountain Imports | ymimports.com | Nov 16 | confirmed 2026-11-16 (footer form, then Klaviyo confirm link clicked: "You're All Set") |
| Mah Jongg Maven | mahjonggmaven.com | Nov 10 | receiving (confirmed) |
| Mahjong by SI | mahjongbysi.com | Nov 16 | receiving |
| Maison Mahj | maisonmahj.com | Nov 4 | receiving |
| YOLO Mahjong | yolomahjong.com | Nov 16 | receiving (welcome) |
| Mahj Pit | mahjpit.co | affiliate only | signed up 2026-11-23 ~11:20pm by Tiffany (captcha); waiting for the first email, check Nov 24 |
| Noli June | nolijune.com | Nov 15 | receiving |
| Sunday Mahjong | sundaymahjong.com | Nov 8 | receiving |
| Bird Bam Tiles | birdbamtiles.com | Nov 12 | receiving |
| Bougie Mahjong | bougiemahjong.com | Nov 16 | signed up 2026-11-16 (popup); welcome email arrived |
| House of Hearts Studio | houseofheartsstudio.com | Nov 15 | receiving |
| Hutch & Nook | hutchandnook.com | Nov 16 | signed up 2026-11-16 (popup, first name + email); welcome email arrived |
| Lucky Bam | luckybam.com | Nov 8 | receiving |
| Mahj Tile Haus | mahjtilehaus.com | Oct 26 | receiving |
| Mahjong Moxie | mahjong-moxie.com | none | signed up 2026-11-23 ~11:20pm by Tiffany (captcha); waiting for the first email, check Nov 24 |
| Ozark Mahjongg | ozarkmahjongg.com | none | signed up 2026-11-16 (Wix form, "Thanks for joining our mailing list") |
| Rebecca Illustrated | rebeccaillustrated.com | none | signed up 2026-11-23 ~11:20pm by Tiffany (captcha); waiting for the first email, check Nov 24 |
| Piper Chase Studios | etsy.com/shop/PiperChaseStudios | - | no newsletter: Etsy shop only |
| LoveShackFancy | loveshackfancy.com | Nov 16 | receiving |
| Brewtifully | shop.brewtifully.com | affiliate only | signed up 2026-11-19 ~12:50pm ET (footer form in her Chrome, no captcha; "Thanks for subscribing", URL got ?customer_posted=true). No double opt-in needed yet; weekly check confirms first newsletter |
| Mahjong Row & Co. | - | - | EXCLUDED (out Nov 6) |

Nov 16 totals: 28 receiving within 30 days; 9 signed up tonight in her Chrome (Bougie, Hutch & Nook, Ozark, Let's Mahj On, Yellow Mountain, Mini Mahjer, Splash, Middle & Main, Oh My Mahjong re-sign) plus Bam Bird by the Bam Bird thread; 12 need Tiffany (11 captcha/phone + Virora); 5 have no newsletter to join.
The tiffanybrie@ forward note below has not shown up in practice: as of Nov 16 none of the captcha brands has a newsletter in mahjmatchmaker@.

## Nov 16 (Tiffany 9:01am: "you have my permission" to sign up + unsubscribe tiffanybrie@ from duplicates)
- Retried Tigre de Tartán footer: hCaptcha still blocks the submit (a captcha is the one step Claude can't do). The 9 hCaptcha brands (TdT, My Fair, Mini Mahjer, Mahjong Press, Amahj, Bam! Let's Mahjong, Mahj Mood, Let's Be Besties, Splash) + Mahj Pit now reach mahjmatchmaker@ through the tiffanybrie@ forward filter (partner domains OR subject affiliate), once Google's phone approval is done.
- Unsubscribed tiffanybrie@ (Gmail Unsubscribe) from lists that ALSO reach mahjmatchmaker@: Miss Mahjong, Bespoke (info@), Amanda Toppe. Britt Mills: no one-click unsubscribe, left. Kept on tiffanybrie@ ON PURPOSE (mahjmatchmaker@ isn't reliably getting them, so the forward carries them): Oh My Mahjong, Bam Bird, Virora, Anders Ruff.

## Nov 19 update (cloud browser; her Chrome not used)
- Ozark Mahjongg: signed up again on mahjmatchmaker@ (Wix footer form, "Thanks for joining our mailing list"). Waiting for first newsletter.
- Bespoke: footer form shows hCaptcha; already on the mahjmatchmaker@ list since the Nov 7 welcome, so marked covered.
- Hip Hip: no signup box anywhere on the site (rechecked Nov 19); newsletter reaches tiffanybrie@ only. Covered via personal Gmail.
- Oh My Mahjong, Bam Bird: no newsletter at mahjmatchmaker@ in the last 30 days (connector search Nov 19), but both reached tiffanybrie@ Nov 18. Marked "Covered via personal Gmail"; do NOT unsubscribe tiffanybrie@ from them.
- Middle & Main, Splash of Color: hCaptcha on the form in the cloud browser. Low priority for Tiffany to sign up herself.
- Rule (coordinator, Nov 19): sites that keep serving human checks are NOT asked of her again. They sit on the sheet as "Low priority: sign up yourself", not an ask: Amahj, Bam! Let's Mahjong, Let's Be Besties, Mahj Mood, Mahj Pit, Mahj Squad, Mahjong Moxie, My Fair, Rebecca Illustrated, The Mahjong Press, Tigre de Tartán, Middle & Main, Splash of Color.
- Sheet: https://docs.google.com/spreadsheets/d/1W1PyfFcAoCtZK-Bdycrs1n1pggHVJG0vCR8XEefxdck/edit

## Nov 19 scheduled run
- No TODO rows were left. Brewtifully (approved Nov 18) had no row: added and signed up (footer form, Chrome). Scheduled newsletter task retired: from now on, new partners are signed up by the onboarding step (CLAUDE.md) and the weekly 30-day recheck.
| Averill Mahjong | averillmahjong.com | none | signed up 2026-11-24 (Chrome, Spin-to-Win popup email only, "Thanks for subscribing"); waiting for first marketing email (only affiliate mail so far) |
| Spools | spools.com | none | signed up 2026-11-24 (Chrome, popup email step; SMS step skipped/closed); waiting for first marketing email (only affiliate mail so far) |

## Nov 23 11:07pm audit (Tiffany: "why haven't those brands been signed up")
Marketing mail to mahjmatchmaker@ since Nov 12: My Fair, Mahj Mood, CMC, Let's Mahj On, Splash, Sweet Jojo, Amanda Toppe, Noli June, Mac + Miller, Virora, Royal, Anders Ruff, Tigre, Miss Mahjong (1), OMM (2, not launch mail). NOTHING from Bam Bird (signed up Nov 16), Bespoke (last Nov 7), Peace Love (last Nov 10). 'needs Tiffany' hCaptcha rows were never put in front of her: that was the miss. Sent her the tap list Nov 23 11:10pm.

## Nov 24 scheduled run
- Averill + Spools signed up (rows above); no TODO rows left. Gmail Nov 24: first marketing mail now in mahjmatchmaker@ from Let's Be Besties (welcome), Amahj, Mahj Mood (welcome), Sweet Jojo, Hutch & Nook, Noli June, LoveShackFancy. Still nothing seen yet from the other Nov 23 hCaptcha signups (check Nov 26 per OVERDUE).
