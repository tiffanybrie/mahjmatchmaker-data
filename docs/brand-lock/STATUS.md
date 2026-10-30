# Brand-locked Find Your Mat-ch (partner perk) — status

**Her answer (HQ needs/brandlock-direction-oct29, Oct 30 2:44am ET):** "Yes, keep exploring. Where are we with it?"
So the direction is approved for exploring: partners only, "coming soon" in the perks, test with ONE partner first (Mahjong Row & Co.). Nothing public, nothing sent to a partner without her OK.

## Where it is (Oct 30)
- Built Oct 29 (commit 2113012): `builder/brand_lock/make_lock.py` + `builder/brand_lock/shop-frame.html`.
  - Lock = `?brand=<brand name>` (or `window.FYM_LOCK` in an embed). Only that brand's tile sets, mats and racks show; shop links go straight to the brand's product pages (no code, no affiliate ref); brand menus hidden; "Powered by Mahj Matchmaker ♥" badge; match card reads "<Brand> × Mahj Matchmaker".
  - Built on Version 1.7 (v103). Not published anywhere.

## Next steps (owner: Matches & Catalog, after FYM Version 1.8 is published)
1. Re-run make_lock.py on the v104 build (the new brand-logo opening screen must be hidden or skipped in lock mode: a locked app opens straight on that brand's tile sets).
2. Gate + QA in lock mode for Mahjong Row & Co.: no other brand's item visible anywhere (tiles, mats, racks, search, aerial view, Mat door), every shop link resolves to a mahjongrowco product page.
3. Private preview for her (artifact or unlisted page) + 3 phone stills (opening screen, a match card, the shop step) on an HQ need. She judges by looking.
4. Draft the perks line for /work-with-us for her OK: "Coming soon for partners: your own Find Your Mat-ch, with only your tiles, mats and racks, for your shop's website."
5. Only after her OK on the stills: ask her whether to show it to Mahjong Row & Co. (sending = her chat approval, doc 74).

Open questions to raise with the stills (once, not before): does the locked version keep MAHJMATCH/affiliate links or go plain (current sample = plain product links, since it would live on the brand's own site)? Free perk vs paid?
