# Link routes: how every shop link gets paid (Tiffany, Nov 8 2026, 6:02pm: "close the ShopMy gap once and for all")

**Truth table:** `config/link-routes.json`, one row per brand (route, commission %, store hosts, notes, source).
**Check:** `python3 scripts/checks/link_route_check.py [<build>]` (FYM gate [172] runs it with `--gate`; the Monday
`gallery_sync_check.py --links` runs it on the live gallery + website FYM). A brand with no row FAILS: add the row the day a brand comes in.

## The routes
| route | the link | lands on | pays |
|---|---|---|---|
| `code-site` | the brand's own store (auto-apply `/discount/MAHJMATCH` link where config/autoapply-hosts.json lists the host) | brand store | the brand's own program (UpPromote / GoAffPro / Collabs) |
| `shopmy-site` | `go.shopmy.us/p-<pin>` | the brand's own store (or its retailer) | ShopMy (e.g. Tala 15%, Rebecca 15%, Charleston 15%) |
| `shopmy-etsy` | `go.shopmy.us/p-<pin>` | etsy.com | ShopMy, 7% (Nov 8 link maker; was 6% Oct 29) |
| `shopmy-amazon` | `go.shopmy.us/p-<pin>`, or a direct `amzn.to` / amazon.com link with tag `heritagesig05-20` | amazon.com | her Amazon Associates tag |
| `none` | plain store link | brand store | nothing (non-partner allowed in for her taste) |

**How to tell them apart:** a ShopMy link is only a tracking wrapper. Curl it: the 302 `Location` shows the store
(`url=` on apiv3 redirect_click = a brand site, `murl=` on linksynergy = Etsy, `btn_url=` on amzlink = Amazon). The check caches
every pin's destination in `config/shopmy-redirect-cache.json` (pins never change).

**Does ShopMy pay on a store?** In her signed-in ShopMy tab: `POST https://apiv3.shopmy.us/api/Pins/get_merchant_data`
`{urls:[domains], names:[]}` (same headers the page sends). A domain that is not returned pays 0 through ShopMy (the link maker says
"This link won't earn commission"). `fullPayout` is the merchant rate; for network merchants (Impact, Rakuten, AvantLink) her share is
lower (OMM 10 -> 8%, Etsy 9 -> 7%, Bam Bird 10 -> ~4%, The Mahjong House 5 -> 4%). Checked for every brand on Nov 8.

## Partner exceptions (a partner where ShopMy pays MORE than its code)
- **Charleston Mahjong Club:** ShopMy 15% vs own 10% -> `shopmy-site`. MAHJMATCH stays on the card (works at checkout).
  24 FYM links + 14 gallery links staged in `config/link-route-fixes.json` for FYM 1.19 (`builder/fym_fix_nov08/apply_link_routes.py`).
- **Bam! Let's Mahjong:** bamletsmahjong.com is NOT on ShopMy (0%, re-checked Nov 8). ShopMy pays 15% only via retailer Printfresh
  (Nantucket, Grandmillennial, Holly Jolly mats; same $95). MAHJMATCH does not work at Printfresh, so links stay `code-site` until
  Tiffany decides (DESK "Waiting on Tiffany").
- **Ask her (own-program rate unknown):** Mahj & Vine (ShopMy 15%), Miss Mahjong (ShopMy 10%). If their own rate is lower, flip to `shopmy-site`.
- Not worth it: OMM (own 20% Q4 vs ShopMy 8%), Bam Bird (own program vs ShopMy ~4%). Mini Mahjer: ShopMy orders = UpPromote orders, never double count.

## Staged fixes
`config/link-route-fixes.json` items `"<group>|<FYM key>" -> {u, old_u, ...}`: apply in the next FYM build; the gallery follows from
that build. The daily check shows them as STAGED; gate [172] FAILS a build that does not carry them. Delete an item once live.
A brand-wide fix running elsewhere can sit on the brand row as `pending_fix` (STAGED daily, FAIL in the gate).

## Bring-in loop (Album Playbook step 10b)
"Bring it in" on a review page -> `scripts/albumreview/read_review.py` writes `config/album-records/<set>.json` `bringins[]`:
`{mat, brand, store, route, shopmy_link, shopmy_collection, amazon_saved, ops_imported, catalog_staged, ...}` (helper
`scripts/albumreview/bringins.py`), plus DESK lines. Close each loop:
1. Route from the table (by brand; otherwise etsy.com -> shopmy-etsy, amazon -> shopmy-amazon, anything else -> shopmy-site).
2. Paid link: ShopMy link maker (or `POST /api/Pins` from her tab) -> pin; Move it into the right collection (Etsy shops:
   "Etsy Mahjong Mats" or the shop's own "(Etsy)" collection). Amazon: save it in the Associates portal first, then Ops imports
   it into ShopMy (DESK "OPS:" line; an HQ needs card only if the save needs her).
3. Catalog: stage it for FYM + gallery (`config/fym-*shopmy*.json` spec; normal photo gates).
4. Fill the fields. `album_gate.py <set> --golive` FAILS until every bring-in has its paid link + catalog staging.
   The review page shows each brought-in find's status.
