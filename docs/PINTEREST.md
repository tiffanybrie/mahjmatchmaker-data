# Pinterest (pinterest.com/mahjmatchmaker)

Pace rules live in `config/pinterest/queue.json` `rules` (2 new pins/day at 13:00Z and 20:00Z on top of the 15:00/16:00Z batch; never more than 4 pins on one day; holiday pins not before Nov 1). Planoly workspace 019fc27b-964d-7279-8685-1f1bb7a7c3f5, channel 01a1184e-8a5d-7389-a935-6a156540cc08. Builder for the test pins: `scripts/pinterest/shopmy_product_pins.py` (images in `assets/social/pinterest/shopmy-test/`).

## ShopMy product pin test (Oct 21)
Tiffany approved Oct 21 5:39pm (exception to the queue.json "own work only" rule). 10 single-product pins, 1000x1500, Caprasimo/navy/pink label + small wordmark, linking to go.shopmy.us product links (except the OMM pin) (each curled: Tala/OMM land 200 on the live product page; Etsy listings redirect correctly but Etsy returns 403 to bots, so stock there is unverified). Sold-out Tala mats (Veranda, Pavilion) skipped. 1 pin/day at 18:00Z (2pm ET), because every day already carries 3 pins and the cap is 4. All #affiliate. MAHJMATCH is mentioned only on the OMM pin (Tala and Betty June & Jeannette are non-partners, no code).

| Date (18:00Z) | Pin | Board | ShopMy link | postGroupId / postId |
|---|---|---|---|---|
| Oct 22 | Pink Watercolor Floral Mahjong Mat, Betty June & Jeannette (The Kerry) | Mahjong Mats & Racks | https://go.shopmy.us/p-96114928 | 01a1606f-90b7-76aa-a6ec-87ceedab93bc / 01a1606f-90bf-721d-a8f1-bcf406975649 |
| Oct 23 | Midnight Wildflower Mahjong Mat, Tala Mahj | Mahjong Mats & Racks | https://go.shopmy.us/p-96067421 | 01a1606f-92a8-76a2-a946-863bb2fe79fb / 01a1606f-92ae-77aa-ada7-cec9b5ea3587 |
| Oct 24 | Heritage Mahjong Tile Set, Oh My Mahjong (code MAHJMATCH) | Oh My Mahjong Tile and Mat Matches | https://www.mahjmatchmaker.com/heritage-mahjong-tile-matches (Heritage match album; no OMM referral link in repo; ShopMy 8% link not used per ShopMy rule) | 01a1606f-94c6-74ef-9ba4-679c619732e5 / 01a1606f-94cb-772f-905c-4360c0e20c84 |
| Oct 25 | Orchid Hummingbird Mahjong Mat, Betty June & Jeannette (Allie) | Mahjong Mats & Racks | https://go.shopmy.us/p-94800122 | 01a1606f-970c-71db-aa27-5d30bde04298 / 01a1606f-9716-7649-9b96-0033163747dc |
| Oct 26 | Pink Striped Mahjong Mat, Tala Mahj (Cabana Pink & Ivory) | Mahjong Mats & Racks | https://go.shopmy.us/p-96304571 | 01a1606f-9a0c-76b0-bf1f-bb407ed3525a / 01a1606f-9a14-747d-815c-0e749af6812b |
| Oct 27 | Pink Poolside Mahjong Mat, Betty June & Jeannette (Brinkley) | Mahjong Mats & Racks | https://go.shopmy.us/p-96125711 | 01a1606f-9c2a-7486-aaf9-d64cf350d258 / 01a1606f-9c34-7208-8ec8-133739d716e8 |
| Oct 28 | Blue Striped Mahjong Mat, Tala Mahj (Cabana Seafoam Blue) | Mahjong Mats & Racks | https://go.shopmy.us/p-96304006 | 01a1606f-9ebb-736c-83d8-fa706345e1af / 01a1606f-9ec6-7080-8729-d9dd62391625 |
| Oct 29 | Blue Chinoiserie Mahjong Mat, Betty June & Jeannette (Nichole) | Mahjong Mats & Racks | https://go.shopmy.us/p-96125150 | 01a1606f-a0cb-737e-ac55-16ad3dd0a775 / 01a1606f-a0d7-719f-82d0-a1c6e3784f37 |
| Oct 30 | Lavender Pink Floral Mahjong Mat, Betty June & Jeannette (Livy) | Mahjong Mats & Racks | https://go.shopmy.us/p-96126853 | 01a1606f-a303-7443-b658-53e326c7f4e6 / 01a1606f-a31a-74b3-b0cb-32d12f2ecab1 |
| Nov 1 | Holiday Plaid Mahjong Mat, Tala Mahj (The Carlyle; holiday, not before Nov 1) | Christmas Mahjong Mats | https://go.shopmy.us/p-96067720 | 01a1606f-a50f-767c-946f-072c94b00780 / 01a1606f-a517-7772-ac53-93cf5aa0350f |

## Queue after the Oct 22 re-spacing (Planoly workspace 019fc27b, 159 scheduled pins)

**What happened.** On Oct 21 at 18:20-18:38Z (2:20-2:38pm ET, read from the Planoly postGroupId timestamps) 104 evergreen pins (`utm_campaign=evergreen`, the card / guide / hub pins that `autopin.py expand` and `render` produce) were bulk-created in Planoly at hourly :30 slots, 05:30Z Oct 22 through 22:30Z Oct 26, about 25 a day. They were scheduled straight in Planoly by an agent session and never recorded in queue.json, so `autopin.py` (which only prints `next` and records `mark`) never saw them, and nothing in the repo checked the 4/day rule: the rule lived only as text in queue.json `rules`. The 13 evergreen pins at 13:00Z / 20:00Z (groups 01a15eb4-*) are the normal autopin pace and were left alone. Git history has no script that does the Planoly scheduling, so the exact session is unrecorded.

**Fix (Oct 22, 05:30Z, before any burst pin published).** All 104 burst pins were moved with set_post_group_schedule (none deleted, none published, none moved earlier than their old time). They now fill the free room under 4 pins/day, oldest first, starting Oct 28 and ending Nov 30, at varied non-round minutes between 13:00Z and 23:00Z. Untouched: the 10 ShopMy test pins (18:00Z Oct 22-30 and Nov 1), the launch pins (15:00/16:00Z), the holiday pins (00:00Z Nov 2-14, none earlier than Nov 1), and the 13 autopin 13:00/20:00Z pins. No day exceeds 4 pins in UTC or in Eastern time (verified by relisting). Queue ends Mon Nov 30, 2026 (21:57Z).

**Guard.** `scripts/pinterest/autopin.py` now has `cap` (pins per day in UTC and Eastern from config/pinterest/planoly_scheduled.json plus queue.json; exit 1 if any day is over 4), `snapshot <list_post_groups json>` (refresh the snapshot), and `mark <id> scheduled <group> <iso>` refuses a date over the cap. Any agent bulk-scheduling Pinterest in Planoly must run `snapshot` then `cap`, and pick only days with room. There is no 4/day room left through Nov 30 (every day is full or has one slot), so new pins (ShopMy scale-up after Oct 24, holiday boards) mean pushing evergreen pins later, not adding on top.

Pins per day (all scheduled, UTC day; Oct 22 before = 21, Oct 23 = 26, Oct 24 = 26, Oct 25 = 26, Oct 26 = 25, Oct 27 = 4, then 3, 2, 2, 1, 2, 2 ... 1):

| Date | Before | After | | Date | Before | After |
|---|---|---|---|---|---|---|
| Oct 22 | 21 | 4 | | Nov 5 | 2 | 4 |
| Oct 23 | 26 | 4 | | Nov 6 | 2 | 4 |
| Oct 24 | 26 | 4 | | Nov 7 | 2 | 4 |
| Oct 25 | 26 | 4 | | Nov 8 | 2 | 4 |
| Oct 26 | 25 | 4 | | Nov 9 | 2 | 4 |
| Oct 27 | 4 | 4 | | Nov 10 | 1 | 4 |
| Oct 28 | 3 | 4 | | Nov 11 | 1 | 4 |
| Oct 29 | 2 | 4 | | Nov 12 | 1 | 4 |
| Oct 30 | 2 | 4 | | Nov 13 | 1 | 4 |
| Oct 31 | 1 | 4 | | Nov 14 | 1 | 4 |
| Nov 1 | 2 | 3 (4 in Eastern time) | | Nov 15-30 | 0 | 4 each |
| Nov 2-4 | 2 | 4 | | | | |

**CHECK DATE: Oct 24.** list_post_groups (workspace above, platform pinterest): confirm the Oct 22 and Oct 23 pins are `published` (not failed), open them on Pinterest to confirm they are live and not flagged/removed, and that the go.shopmy.us link still resolves. If any are flagged or the links are blocked, pause the rest (delete_post_group) and tell Tiffany. If clean, scale the test while staying under the pace above.

Not yet verified for stock: Etsy (Betty June & Jeannette) listings. Heritage pin links to the Heritage match album (OMM is a partner paying 20% via its own code program, so no ShopMy link); swap in her OMM affiliate link if she has one.
