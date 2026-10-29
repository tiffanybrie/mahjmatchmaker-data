# ShopMy intake: Tiffany drops a note in HQ, we act (set up Oct 29)

**Why:** Tiffany adds mats/collections on ShopMy in real time (e.g. mats for the Sunday Mahjong album). She should not wait for the Monday check or hunt for the right chat. HQ has a **ShopMy tab** with one box. What she types lands in HQ db collection `shopmy` (doc `s<ms>`: `{text, at, status:"new", kind?}`). Status flow: new → working → done (Claude sets `reply` = one plain line of what was done, `doneAt`).

**Pickup:** scheduled task "ShopMy requests from HQ" (every 2 hours 9am–9pm ET) lists collection `shopmy` (ArtifactData list, url https://claude.ai/artifact/Cor6pKtesou4mFRQ41P6Ye); no `new` docs = finish at once. Any attended chat (Ops) also checks it at the start of a reply. The Monday weekly check (trigger trig_01NpQoJYSYh2GCLwcHNpkDiU) still runs as the safety net.

## Doing a request (Ops/Chrome; set status "working" first)
1. Read ShopMy (her collections): `GET https://apiv3.shopmy.us/api/Collections/<id>` works from a shopmy.us tab with `credentials:'include'` (pins list inside). Collections are found via shopmy.us/links (collection name is a link). Pin image URLs on S3 return 403 from the shell; use the retailer's original (Etsy: i.etsystatic.com).
2. **New mats in an existing collection / a new collection:** follow the weekly check prompt (FYM staging after photo gates; Amazon never auto-enters FYM). Put a DESK line for Matches & Catalog.
3. **Mats for a match album (e.g. Sunday Mahjong):** write them in docs/MATCH-INBOX.md (album, mat names, ShopMy collection/link) the same turn and a DESK line "Matches & Catalog:" so they come into the album/FYM.
4. **New collection = cover + description + shelf, always (a collection with no Section_id shows on NO shelf):**
   - Name: Etsy-shop collections end in " (Etsy)" (her rule Oct 29).
   - Cover: 1000x1500 portrait, six pictures 3x2. `scripts/shopmy/make_covers_portrait.py` (`makeP(id,slug,title,tagline,kicker,accent,6,[pinIds])`, see Luna run in git history); photos cropped to the mat; LOOK at it; she does not need to approve (Oct 29: "just get it done"). Commit + push, warm the jsDelivr URL pinned to the commit (curl 3x, expect 200).
   - Capture ShopMy's request headers: in the shopmy.us tab hook fetch/XHR, type a description in "Describe your collection" (a real save), read the captured PUT headers (X-CSRF-Token, X-Session-Id, x-apicache-bypass).
   - `PUT https://apiv3.shopmy.us/api/Collections/<id>` with those headers: `{image:<jsDelivr URL>}` (ShopMy re-hosts it), then `{Section_id:4705121, sortOrderRank:<rank of the collection it should follow>+1}` (4705121 = the public Shelves section; shelf is Square layout; 6+ items).
   - Verify: GET shows image/Section_id; https://shopmy.us/shop/mahjmatchmaker?Section_id=4705121&tab=collections lists it.
5. Close your Chrome tab. Set the `shopmy` doc status done + reply. Log in HQ (area "ShopMy").

Cover set: Luna EK Studio Mats (Etsy) id 8614817 done Oct 29 (cover assets/shopmy/covers-portrait/luna-ek-studio-mats.jpg).
