# Partner email check: website vs email list vs app (Oct 26)

Read-only audit for Tiffany's 8:38am ask (ANSWERS 2026-10-26 08:38). Nothing sent, nothing changed on Squarespace, nothing published.

Sources:
- **Website:** `https://www.mahjmatchmaker.com/mahjong-discount-codes` ("All 35 mahjong discount codes at a glance", 35 brand-page links) + sitemap.xml (36 `*-discount-code` pages = the 35 + Sunday Mahjong "honorary partner, no code" page). `/fait-a-main-discount-code` = 404.
- **Email list:** `config/partner-brands-squarespace-import.csv` (36 rows, 35 brands; Bam Bird has 2 people) + `config/partner-brand-contacts.csv` (39 rows).
- **App:** FYM v93 (live; site/livepatch/fym-preview-oct21/README line 4), build `scratchpad/fym/b93/index.html`. Counts = items without `hid`. Tile counts include "Photo coming soon" (`soon`) cards, shown in brackets. b94 (unpublished) has the same counts for the brands below.

Email checks: no duplicate addresses, none malformed. Mac + Miller is `Partnerships@` in contacts vs `partnerships@` in import (same address, fine).

| Brand | On website | Email(s) | In Squarespace import | Visible tiles / mats / racks (v93) | Issues |
|---|---|---|---|---|---|
| Oh My Mahjong | yes | info@ohmymahjong.com (+ teach@ohmymahjong.com in contacts) | yes (info@ only) | 37 / 57 / 12 | teach@ not in import; decide if the teacher contact should get it |
| Mahjong Row & Co. | yes | bradk@mahjongrowandco.com | yes | 8 / 9 / 7 | |
| Miss Mahjong | yes | hello@missmahjong.com | yes | 10 (4 soon) / 21 / 11 | general inbox |
| My Fair Mahjong | yes | smiles@myfairmahjong.com | yes | 20 / 21 / 24 | |
| Bam Bird Boutique | yes | instructors@ + courtney@bambirdboutique.com | yes (2 rows) | 16 / 31 / 19 | 2 rows = they get 2 copies (intended) |
| Bespoke Mahjong | yes | partnerships@bespokemahjong.com | yes | 22 (3 soon) / 50 / 7 | |
| Peace Love Mahjong | yes | info@peacelovemahjong.com | yes | 8 / 53 / 28 | |
| Charleston Mahjong Club | yes | info@charlestonmahjongclub.com | yes | 5 / 15 / 4 | |
| Tigre de Tartán | yes | affiliates@tigredetartan.com | yes | 4 (3 soon) / 27 / 5 | only 1 tile set has a real photo |
| Britt Mills | yes | hello@brittmillsdesign.com | yes | 0 / 55 / 0 | mats-only brand, OK |
| Amanda Toppe | yes | amanda@amandatoppeart.com | yes | 0 / 9 / 0 | mats-only brand, OK |
| Amahj | yes | shop@amahjline.com | yes | 11 (1 soon) / 8 / 0 | their 1 rack is hidden |
| Mac + Miller Mahjong | yes | partnerships@macandmillermahjong.com | yes | 5 (2 soon) / 5 / 1 | |
| Middle & Main Mahjong | yes | info@middleandmainmahjong.com | yes | 5 / 10 / 7 | |
| Mahj Mood | yes | mahjmood@gmail.com | yes | 8 (1 soon) / 15 / 14 | |
| Mahj Squad | yes | mahjsquad@gmail.com | yes | 5 / 20 / 0 | |
| Bird & Bamboo | yes | emilyk@birdandbamboo.com | yes | 6 / 16 / 92 | |
| Let's Mahj On | yes | info@letsmahj-on.com | yes | 9 / 19 / 2 | |
| Splash of Color | yes | deidrasplashofcolor@gmail.com | yes | 0 / 42 / 0 | **sells tile sets + racks (products.json: e.g. Polo Match, Mod About You tiles; Extended scalloped racks); none in app** |
| Bam! Let's Mahjong | yes | info@bamletsmahjong.com | yes | 18 (3 soon) / 14 / 8 | |
| Mini Mahjer | yes | marian@minimahjer.com | yes | **0 / 0 / 0** | **not in app** (sells mini tile sets "Just the Tiles"/Complete Game editions, Travel Mat, Travel Racks & Pusher; held in config/fym_extra_brands.json) |
| Wren Mats | yes | catherine@wrenmats.com | yes | 1 (1 soon) / 24 / 0 | its only tile set is Photo coming soon |
| Mahj & Vine | yes | mahjandvine@gmail.com | yes | 0 / 16 / 0 | mats-only, OK |
| Hip Hip Mahjong | yes | affiliate@hiphipmahjong.com | yes | 10 (5 soon) / 14 / 4 | half its tiles are Photo coming soon |
| Virora Mahjong | yes | **none** | **NO** | 16 / 12 / 7 | **no email anywhere** (site has contact form only; Gmail has only GoAffPro no-reply sale emails; site pages have no address). Ask via IG @viroramahjongofficial / contact form, or the GoAffPro dashboard message |
| Yellow Mountain Imports | yes | hello@ymimports.com | yes | 42 (1 soon) / 0 / 12 | |
| Mahjong Co. | yes | info@mahjongco.com | yes | **0 / 0 / 0** | **not in app**: their store has 1 product, Kaleidoscope Mahjong Tiles (held in fym_extra_brands.json) |
| I Love Mahj | yes | support@ilovemahj.com | yes | 0 / 0 / 0 | online game, nothing to put in the app: decide whether to send it to them or send a tailored line |
| Anders Ruff | yes | joanna@andersruff.com | yes | 7 (3 soon) / 58 / 7 | |
| Mahjong Studios | yes | info@mahjongstudios.com | yes | 28 (2 soon) / 0 / 40 | mats excluded on purpose (Oct 20 rule) |
| The Mahjong Press | yes | hello@themahjongpress.com | yes | 0 / 0 / 0 | sells only American Mahjong cards (7 products), nothing to put in the app: same decision as I Love Mahj |
| The Royal Mahjong Society | yes | info@theroyalmahjongsociety.com | yes | 12 / 8 / 2 | |
| Soirée All Day | yes | hello@soireeallday.co | yes | 0 / 11 / 0 | |
| Mahjong Register | yes | hello@mahjongregister.com | yes | 0 / 33 / 11 | |
| Let's Be Besties | yes | laurie@letsbebesties.com (+ lauriegoldstein1204@gmail.com in contacts) | yes (laurie@ only) | 0 / 41 / 0 | also sells Holiday Soirée tiles + acrylic/tortoise racks, not in app (minor) |
| Fait à Main | **NO** (no page, not on the codes list; /fait-a-main-discount-code 404) | info@fait-a-main.com | yes | **0 / 0 / 0** | **partner (UpPromote approved Oct 20) but not on website and not in app**; sells ~8 mats (Round Top Mon Amour, Saint-Rémy, Le Drip Summer Colors, Texas Mon Amour Peach/Cream, ...) + Scalloped acrylic racks. HQ already has "Fait à Main link + code" waiting |
| Sunday Mahjong | honorary page only, "not a partner brand" | none | no | 6 / 12 / 5 | not a partner: leave off unless Tiffany wants it to get the email |

Not partners but in the app (no action, FYI): Tala Mahj, House of Hearts Studio, Sophie Clima, Betty June & Jeannette, Rebecca Illustrated, Mahjong by SI, Ozark, Mahj & Moon/Maison Mahj/Mahj Tile Haus/Hutch & Nook/Luxe matched mats, Mahjong Moxie (2).

## Must fix before send
1. **Virora Mahjong** is a website partner with **no email** and is **not in the Squarespace list**. Get an address (IG DM @viroramahjongofficial, site contact form, or GoAffPro message) and add it.
2. **Fait à Main** is in the email list but **not on the website and not in the app**. Either add its brand page + products (≈8 mats, racks) before sending, or hold it off this send.
3. **Mini Mahjer: 0 products in app** (mini tiles, travel mat, travel racks). Add them or they'll write back "we don't see ourselves".
4. **Mahjong Co.: 0 products in app** (1 product: Kaleidoscope tiles). Add it.
5. **The Mahjong Press (cards) and I Love Mahj (online game)** can't appear in the app. Tiffany decides: leave them off this email, or send them a version without "find yourself in the app".
6. **Splash of Color** tiles + racks missing (mats only in app). Strongly suggested.
7. Decide on the extra contacts: OMM teach@ and Let's Be Besties' Gmail are in contacts but not imported. Sunday Mahjong is not a partner, so it stays off.
