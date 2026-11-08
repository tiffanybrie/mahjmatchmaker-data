# Racks refresh, Nov 8 2026 (for FYM 1.19 and album rack picks)

Asked for by Tiffany at 2:12pm (docs/ANSWERS.md): find a replacement for Mahjong Row Scalloped Tortoise, and check what's new in partner racks so the rack picks don't go stale.
Sources: each partner store's live `/products.json` (Nov 8, ~2:15pm ET), config/brand-watch-curated.json, docs/brand-social/*, and the live FYM build v118 (`D.racks`).
Prices and stock are for the base variant without a rack bag.

## Job 1: replacement for Mahjong Row & Co. Scalloped Tortoise

Contact sheet (current FYM cut-outs on white AND navy, plus each brand's best product image along the bottom row):
`docs/research/racks-refresh-2026-11-08-tortoise.jpg`

| Candidate | Partner | Scalloped | Price | Stock (Nov 8) | Length | Photo in FYM | Verdict |
|---|---|---|---|---|---|---|---|
| **Mahjong Register Tortoise Club Scalloped** | yes (14% commission; the 10% MAHJMATCH code excludes racks) | yes | $135 ($145 with bag) | IN STOCK | 20" | clean single-rack cut-out, sm + HD, reviewed ok; checked again at full size on navy: no halo | **RECOMMENDED** |
| Mahjong Register Blonde Tortoise Scalloped | yes | yes | $135 | IN STOCK | 20" | clean single-rack cut-out | runner-up: the blonde version (light, spotted) |
| Mahjong Register Emerald Tortoise Scalloped | yes | yes | $135 | IN STOCK | 20" | clean single-rack cut-out | green tortoise, not the classic look |
| Mahj Mood Scalloped Tortoise Acrylic | yes | yes | $125 | **SOLD OUT** (already flagged `oos`) | 20" | 4 racks stacked on marble; brand has only marble shots | out while sold out. Mahj Mood sells tortoise scalloped PUSHERS alone (in stock, $42) |
| Tigre de Tartan Tortoise Acrylic Scalloped | yes (link-only, no code) | yes | $175 | IN STOCK (handle still says "february-preorder") | 20" | room/lifestyle photo (racks on a mat with tiles) | all 16 brand images are lifestyle shots on patterned mats, so no clean cut-out is possible |
| Mahjong Row & Co. Scalloped Tortoise (old pick) | **program ended** | yes | $130 | in stock | 20" | was the best photo | parked hidden (Nov 6 removed_brands) |

Checked for a SCALLOPED tortoise at other partners (products.json):
- Anders Ruff: Tortoise (blonde) acrylic, **straight pushers only**, $205, 20", in stock. No scalloped tortoise. Its scalloped line (Pistachio, MAHJenta, Clear) has no tortoise.
- Miss Mahjong: Dark Tortoise Classic ($150), Blonde Tortoise Classic ($150), Dark Tortoise & Brass ($175), all "Classic" (straight). Blonde Tortoise & Brass is SOLD OUT. No scalloped tortoise. The Tue 11/10 drop is solid colours.
- Oh My Mahjong: Tortoise Shell and Blond Tortoise, both $110, 18.5", straight. No scalloped tortoise.
- My Fair Mahjong: Tortoiseshell acrylic racks ($150, 20") come with rectangular pushers. They sell a **Wavy-Tortoiseshell pusher add-on** ($55), so the set can be made wavy for $205.
- Also seen: Fait à Main (partner) "The Scalloped Rack – Pink Tortoise", $175, in stock. It's PINK tortoise, has lifestyle photos only, and isn't in FYM. YOLO Tortoiseshell acrylic ($128, straight, in FYM). Charleston Mahjong Club Tortoise **travel** racks ($60, new Oct 29).

**Recommendation: Mahjong Register Tortoise Club Scalloped.** It has the same classic warm amber and dark-brown tortoise as the Mahjong Row rack, the same scalloped top, and a clean straight-on single-rack photo that's already in FYM and approved on white and navy. It's in stock, at $135 against Mahjong Row's $130. The partner pays 14% on racks even though the code doesn't apply.
No re-cut is needed: the current cut-out comes from the brand's "Front View" infographic strip and is clean.
Proportions: it's 20" (Mahjong Row's was 20" too), so it pairs with other 20" racks on a card.

## Job 2: new partner racks in the last ~60 days (since Sep 9)

Legend: **STAGED** = in config/fym-rack-adds-nov08.json for FYM 1.19 (builder/fym_fix_nov08/racks119.py). Every image was cut, LOOKED AT on white + navy and approved in builder/fym_flags/rack_image_review.json.

### New colourways not in FYM before today
| Brand | Rack | Price | Stock | Status |
|---|---|---|---|---|
| Mahjong Register | Celestial Collection: Celestial Tide (aqua, scalloped) | $139 | in stock | **STAGED** |
| Mahjong Register | Celestial: Cosmic Lilac (scalloped) | $139 | in stock | **STAGED** |
| Mahjong Register | Celestial: Solar Coral (scalloped) | $139 | in stock | **STAGED** |
| Mahjong Register | Celestial: Pink Nova (scalloped, translucent hot pink) | $119 | in stock | **STAGED** |
| Mahjong Register | Celestial: Moon Marble (white/grey marble, straight) | $139 | in stock | **STAGED** |
| Mahjong Register | Signature Pearl: White Opal (scalloped) | $135 | in stock | **STAGED** |
| Mahjong Register | Signature Pearl: Imperial Jade (scalloped, green marble) | $135 | in stock | **STAGED** |
| Mahjong Register | Cane Cabana real rattan in acrylic (new Oct 25) | $149 | in stock | **STAGED** |
| My Fair Mahjong | Confetti Pink / Green / Purple / Blue acrylic (new Nov 5) | $150 each | "available", but a short preorder that delivers mid-Nov per their Nov 4 post | **STAGED** (house stack shot like the other MFM racks; c:false) |
| Mahj Mood | Luxe Jade acrylic, scalloped (new Oct 30) | $130 | in stock | **STAGED** (brand close-up photo, c:false, like the other Luxe racks; all brand shots are on concrete) |
| Mahjong Row & Co. | Oxblood Burgundy, Midnight Blue (Nov 5) | $60 | in stock | not staged: partner program ended |
| Charleston Mahjong Club | Acrylic travel racks + bag: Tortoise, Clear, Hot Pink, White (Oct 29) | $60 | in stock | not staged: travel racks (shorter, low ticket). **Her call** |
| Bam Bird Boutique | Fuchsia Travel Racks (Oct 9) | $50 | in stock | not staged: travel racks. **Her call** |
| Mahj Mood | Pusher add-ons (Mint scalloped, Pink Pearl, Purple Pearl, White scalloped) | $42 | in stock | not staged: pushers only |
| My Fair Mahjong | Wavy pusher add-ons (25 colours incl. Wavy-Tortoiseshell) | $45–55 | in stock | not staged: pushers only |
| Bespoke | "Less than perfect" / odd-lots racks | — | SOLD OUT | skip |

### Already in FYM but HIDDEN since Nov 1 (pending cut-out); now cut and staged to unhide
Mahjong Register Solid Wood scalloped, $89, all in stock, 20": Light Pink, Pink, Peach, Purple, Navy, Sky Blue, Mint, Green, Black, White. Also Mahjong Register **Crystal Palace** gold-hardware clear ($149, in stock; clear, so shown on white, c:false) and **My Fair Mahjong Poppy Red** ($125, in stock).
These 12 were added by adds112 and never got their photo step (README step 3b), so they sat hidden for a week.

### New in the last 60 days and already in FYM (no action)
Anders Ruff Pistachio + MAHJenta scalloped, Rosè Pink Pearl, Jade, Tortoise straight. Miss Mahjong Peach Sorbet + Iridescent Opal scalloped, Opal & Brass (**SOLD OUT**, not flagged). Mahjong Register Jet Set Black, Peacock Teal, Kelly Green gold-hardware, and Admiral Navy (**SOLD OUT**: `oos` staged). Tigre de Tartan Dove White / Rich Raisin / Marine Blue beechwood (straight + scalloped). Hip Hip Santa Baby. Mahj Mood Chocolate Brown wood (**SOLD OUT**), Luxe Amethyst (**SOLD OUT**: `oos` staged), Luxe Grey Marble. Virora wooden + hinged (Pink / Ivory / Purple wood **SOLD OUT**). Middle & Main Golden Grain beechwood. Bespoke Ultimate Holiday Red.
Still hidden in FYM, not touched here: Mac + Miller Heirloom Ivory (in stock), Mahj Mood Butter Yellow wood (in stock), TdT Clear Acrylic Logo (in stock).

Skipped on purpose: Miss Mahjong acrylic drop Tue 11/10 (has its own scheduled task); Mahjong Studios (no new racks checked: brand racks stay but are not a growth priority).

### Data fixes staged with the same script
- Mahj Mood Luxe Grey Marble showed as GREEN (#4f9a5a, rf green), but the photo is grey marble. Now neutral grey, renamed "Mahj Mood Luxe Grey Marble".
- Mahj Mood Luxe Amethyst renamed "Mahj Mood Luxe Amethyst" (both racks were called "Mahj Mood Luxe"), plus `oos`.
- Mahjong Register Admiral Navy gets `oos`.

## Decisions for Tiffany
1. Tortoise: OK to use **Mahjong Register Tortoise Club Scalloped** as the go-to scalloped tortoise? (Default if no answer: yes, for new albums. Swapping it into old albums stays a rainy-day job.)
2. Travel racks (Charleston Mahjong Club acrylic travel racks, Bam Bird Fuchsia travel racks): should travel racks come into FYM at all? (Default: no, they're shorter and low ticket.)
3. Fait à Main Pink Tortoise Scalloped ($175): bring it in with a lifestyle photo (c:false)? (Default: no, until there's a cleaner photo.)

## How to ship (FYM 1.19 builder)
`python3 builder/fym_fix_nov08/racks119.py <b119>` after the other 1.19 steps, then `python3 builder/fym_rack_images.py <b119>` (must print "all rack images reviewed ok") and the full `fym_gate.py`.
Assets: assets/racks/v119/. Config: config/fym-rack-adds-nov08.json.
