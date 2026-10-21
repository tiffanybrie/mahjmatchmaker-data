# Album vs Mat Gallery combo audit (Oct 20)

Read-only audit of matgallery-v5.html (682 mats) against the 37 live album pages. Data: album_combo_audit_oct20.json (same folder).

## Lagoon: Teal + Pink

- Live result: 31 mats; only 5 Lagoon album mats show (Aria, Delilah, Lorelei, Lucky Charms Watercolor, Radiance).
- After the recommended fix (A3): 54 mats. Blue = teal merge instead: 89 (floods).

| Mat | Why it is missing | Fixed by |
|---|---|---|
| Elysium | Photo: navy + lime with a teal frame and pink florals. Has pink (her accent call) but teal 11.7% (< 15% teal threshold) and teal is blanket-removed for Tiffany-called mats. Fixed by A3 (album-confirmed teal) or B (blue counts as teal). | A3 or B |
| Pink Winds | Photo: pale blue/aqua watercolor border with a lilac-pink centre. Measured purple 47 / blue 44.2 / green 8.9, pink 0, teal 0: aqua read as blue, lilac read as purple. Fixed for teal by B (merge); pink needs a per-mat tag. | A3 gives teal; pink needs per-mat tag |
| Gray Malin | Not in gallery: held-low-98 + hidden_oct20.csv ("image shows no mat: photo of..."). Needs a clean flat mat photo before it can enter. | New clean mat photo |
| Watercolor Blooms | Photo: aqua border, pink florals, pink centre: clearly teal + pink. Teal 36.4 (accent) but pink 11.5% is 0.5 under the 12% threshold (the cream tube in the photo inflates neutral to 49.5). Fixed by A3 or a 11% threshold. | A3 (pink 11.5, 0.5 under 12) |
| Esme | Photo: teal/aqua mat with pink florals. Pink measured 6.5% (< 12% accent threshold). Album-confirmed rule (A3) fixes it. | A3 |
| Jade | Photo: blue + blue-green leaves, no visible pink. Teal measured 24.3% but dropped: build_v5.py line 374 adds teal to REMOVED for every mat Tiffany gave a final call, and her accent_calls (neutral, purple) replace measured accents. Pink 0%. Shows under Teal only if the blanket teal removal is dropped; under Teal+Pink only with a per-mat pink tag (photo does not support it). | A3 gives teal; pink only by per-mat tag (none in photo) |
| Mirage | Photo: hot pink/red field with clearly teal palm motifs in the center panel. Measured pink 65.7 / red 26.6 / neutral 7.7, teal 0: the k-means cluster read swallowed the small teal motifs. Measurement wrong -> per-mat tag (teal) needed; also retired (hidden by default). | Per-mat tag teal + retired shown |
| Amethyst | Retired: hidden by default ("Hide retired" toggle is ON). Has teal (tag) but pink 4.9% < 12%. Needs retired shown + A3. | Retired shown + A3 |

Set colors: config/tile-tones.json (Tiffany-stated dominant where src=tiffany) + her Tile Edit caption words + measured tile palette. Lagoon = blue/teal/green + berry; combo = her own Teal + Pink.

## All 37 sets (main 2-color combo, regular album cards; holiday cards excluded)

"Color-present" = the mat really carries both colors (tagged, or measured at least 3%, blue and teal pooled). Those are the misses that count. The other misses are mats matched on harmony, not color, and a color filter should not show them.

| Set | Combo | Album mats | In gallery | Retired (hidden) | Not in gallery | Live misses (active) | Color-present misses | After A3 | Combo size live -> A3 |
|---|---|---|---|---|---|---|---|---|---|
| amara | red + pink | 33 | 17 | 13 | 3 | 17 | 2 | 0 | 31 -> 39 |
| birdie | blue + green | 18 | 13 | 4 | 1 | 7 | 3 | 0 | 81 -> 102 |
| coquette | pink + blue | 52 | 40 | 7 | 5 | 33 | 3 | 0 | 75 -> 96 |
| cypress-forest | earthy + green | 27 | 25 | 2 | 0 | 19 | 2 | 0 | 60 -> 66 |
| dandy | pink + purple | 20 | 14 | 6 | 0 | 14 | 3 | 0 | 34 -> 39 |
| drake | green + earthy | 36 | 24 | 5 | 7 | 17 | 0 | 0 | 60 -> 66 |
| emerald | green + pink | 16 | 8 | 8 | 0 | 6 | 2 | 0 | 81 -> 103 |
| gatsby | blue + dark | 47 | 40 | 6 | 1 | 36 | 3 | 0 | 23 -> 29 |
| gemma | purple + green | 12 | 9 | 2 | 1 | 7 | 1 | 0 | 19 -> 25 |
| glitterville | pink + purple | 16 | 8 | 8 | 0 | 8 | 0 | 0 | 34 -> 39 |
| glow-wild | pink + green | 36 | 23 | 9 | 4 | 18 | 3 | 0 | 81 -> 103 |
| heritage-2-0 | earthy + green | 60 | 41 | 12 | 7 | 33 | 1 | 0 | 60 -> 66 |
| heritage | earthy + neutral | 54 | 34 | 12 | 8 | 32 | 12 | 0 | 36 -> 51 |
| jade | green + teal | 38 | 27 | 9 | 2 | 24 | 11 | 0 | 41 -> 59 |
| jasmine | green + dark | 12 | 7 | 5 | 0 | 6 | 0 | 0 | 30 -> 32 |
| la-fete | pink + red | 18 | 12 | 5 | 1 | 12 | 2 | 0 | 31 -> 39 |
| lagoon | teal + pink | 36 | 24 | 7 | 5 | 19 | 11 | 0 | 31 -> 54 |
| limoncello | yellow + green | 12 | 5 | 6 | 1 | 4 | 1 | 0 | 24 -> 30 |
| lola | blue + green | 19 | 14 | 4 | 1 | 9 | 3 | 0 | 81 -> 102 |
| luminaire | purple + pink | 14 | 7 | 5 | 2 | 7 | 1 | 0 | 34 -> 39 |
| malachite | green + red | 33 | 21 | 8 | 4 | 18 | 1 | 0 | 34 -> 37 |
| moonlight | blue + green | 24 | 16 | 6 | 2 | 11 | 4 | 0 | 81 -> 102 |
| nantucket | red + blue | 12 | 8 | 3 | 1 | 6 | 2 | 0 | 20 -> 24 |
| osler | blue + red | 19 | 16 | 1 | 2 | 16 | 0 | 0 | 20 -> 24 |
| palm-royale | green + yellow | 19 | 10 | 8 | 1 | 8 | 0 | 0 | 24 -> 30 |
| pearlescent | neutral + pink | 24 | 11 | 10 | 3 | 10 | 4 | 0 | 20 -> 38 |
| pippa | yellow + pink | 19 | 11 | 5 | 3 | 11 | 4 | 0 | 15 -> 21 |
| seabreeze | teal + pink | 24 | 23 | 0 | 1 | 17 | 8 | 0 | 31 -> 54 |
| sierra | orange + earthy | 16 | 12 | 4 | 0 | 8 | 0 | 0 | 24 -> 25 |
| smith | earthy + blue | 25 | 20 | 4 | 1 | 17 | 3 | 0 | 40 -> 46 |
| solara | yellow + pink | 35 | 23 | 5 | 7 | 22 | 1 | 0 | 15 -> 21 |
| sorbet | yellow + orange | 11 | 6 | 4 | 1 | 6 | 1 | 0 | 12 -> 13 |
| sunset | orange + pink | 9 | 5 | 4 | 0 | 5 | 1 | 0 | 44 -> 52 |
| talulah | neutral + teal | 22 | 18 | 1 | 3 | 18 | 6 | 0 | 9 -> 23 |
| taylor | purple + neutral | 12 | 7 | 4 | 1 | 6 | 0 | 0 | 8 -> 10 |
| tortoise | earthy + neutral | 45 | 27 | 12 | 6 | 25 | 8 | 0 | 36 -> 51 |
| willow | green + blue | 43 | 32 | 3 | 8 | 21 | 5 | 0 | 81 -> 102 |

## Fix options (all 37 combos)

Active album memberships: 658; color-present: 217.

| Option | Color-present misses left | Total combo results | Single-section change |
|---|---|---|---|
| Live today | 112 | 1461 | none |
| (b) Blue + teal merged in combos | 94 | 1811 | none (combo only) |
| (c) Accent threshold 12 to 8% | 84 | 2069 | red 56->103, pink 213->272, green 212->288, orange 71->101 |
| (c) Accent threshold 5% | 66 | 2567 | red 56->132, green 212->314 |
| (a) Every album mat gets all set colors | 0 | 3517 | none if combo-only (665 tags, many not in photo) |
| (a3) Album mats get set colors the photo has (>=3%), combo-only | 0 | 1852 | none (combo-only field, like holiday hacc) |
| a3 + b | 0 | 2167 | none |
| a3 + drop blanket teal removal | 0 | 1854 | teal +5 mats |

**Recommendation: (a3) album-confirmed colors in a combo-only field.** It clears all 112 color-present misses with 176 new tags on 192 mats. Combo results grow 1461 -> 1852 (+27%), and single-color sections do not change at all. (b) fixes only 18 and almost triples Teal + Pink (31 -> 89). (c) at 8% fixes 28 but nearly doubles the Red section. (a) floods: 665 tags, and 3517 results. Then add per-mat tags (d) for the photo misreads below, and decide whether combos should show retired mats (the toggle hides 159 color-present album memberships).

## Systemic problems found

- **teal_blanket_removal**: build_v5.py:374 appends teal to REMOVED for all 22 mats with a Tiffany final call: measured teal >= 15% is dropped for amanda-toppe--limelight, mahj-moon--blue-tropical-palm, mahj-moon--tropical-hibiscus, oh-my-mahjong--isla, oh-my-mahjong--jade
- **teal_band**: families.fam_arr teal = hue 172-192 with sat > 0.3, and hue < 180 is re-read as green, so teal is only a 12-degree band (180-192); aqua/turquoise with hue > 192 reads blue (Pink Winds, Elysium frame).
- **accent_calls_replace**: Tiffany accent_calls replace ALL measured accents for that mat (Jade loses measured teal 24.3).
- **retired_hidden**: Hide retired defaults ON and also applies to combos: retired album mats never show unless she turns it off.

## Per-mat problems

Measurement disagrees with photo (eye-checked): OMM Mirage (teal palms read 0%), Amanda Toppe Pink Winds (aqua read as blue, lilac-pink read as purple), Mahj & Vine Watercolor Blooms (pink 11.5%, cream tube in photo inflates neutral), OMM Esme (pink 6.5%), OMM Jade and Elysium (teal dropped by blanket rule).

Album mats not in the gallery:

- Amazon Amazon (willow): not in gallery catalog (never scraped / non-partner / not a store product)
- Amazon Amazon 2 (willow): not in gallery catalog (never scraped / non-partner / not a store product)
- Bam Bird Boutique Classic Neoprene in Lavender (coquette): held low-confidence list (held-low-98.json: bam-bird-boutique--classic-neoprene-in-lavender)
- Bam Bird Boutique Classic Neoprene in Pink (coquette): not in gallery catalog (never scraped / non-partner / not a store product)
- Bam Bird Boutique Navy Vegan Leather (smith): not in gallery catalog (never scraped / non-partner / not a store product)
- Bam Bird Boutique Origami Berry (drake): not in gallery catalog (never scraped / non-partner / not a store product)
- Bespoke Mahjong Chartreuse Garden (lagoon, pippa): held low-confidence list (held-low-98.json: bespoke-mahjong--chartreuse-garden)
- Bespoke Mahjong Gray Malin (lagoon): hidden_oct20.csv: already out (held low-confidence list); would also be hidden: image shows no mat: photo of dogs on a ski lift 
- Bespoke Mahjong YOTD Purple (malachite): not in gallery catalog (never scraped / non-partner / not a store product)
- Bespoke Mahjong YOTD Raspberry (amara, glow-wild, lagoon, limoncello): held low-confidence list (held-low-98.json: bespoke-mahjong--yotd-raspberry)
- Bespoke Mahjong YOTD White (drake, heritage-2-0, heritage, malachite, tortoise): held low-confidence list (held-low-98.json: bespoke-mahjong--yotd-white)
- Bespoke Mahjong Year of the Dragon Raspberry (jade): not in gallery catalog (never scraped / non-partner / not a store product)
- Bird & Bamboo Neutre Blanc (talulah): held low-confidence list (held-low-98.json: bird-bamboo--the-neutre-blanc-mahjong-mat)
- Birdsong Mahjong Grace (drake, heritage-2-0, heritage, willow): not in gallery catalog (never scraped / non-partner / not a store product)
- Britt Mills Quinn (willow): held low-confidence list (held-low-98.json: britt-mills--quinn)
- Britt Mills Regal Bloom (glow-wild, solara): hidden_oct20.csv: already out (held low-confidence list); would also be hidden: wrong image: Oh My Mahjong "Regal Bloom (retired
- Four Winds Social Mozaic Mahj (solara): not in gallery catalog (never scraped / non-partner / not a store product)
- Four Winds Social Petals and Plum (glow-wild): not in gallery catalog (never scraped / non-partner / not a store product)
- Mac Miller Sweet Dreams (seabreeze): not in gallery catalog (never scraped / non-partner / not a store product)
- Mahj & Moon Vintage Floral Gingham (solara): held low-confidence list (held-low-98.json: mahj-moon--vintage-floral-gingham)
- Mahj & Vine Greenly (solara): held low-confidence list (held-low-98.json: mahj-vine--greenly)
- Mahj Mood Bow and Bloom (osler): not in gallery catalog (never scraped / non-partner / not a store product)
- Mahj Squad Bejeweled Dream (coquette): held low-confidence list (held-low-98.json: mahj-squad--bejeweled-dream)
- Mahj Tile Haus Imperial Lotus (talulah): not in gallery catalog (never scraped / non-partner / not a store product)
- Mahj and Moon Retro Daisy (pippa): not in gallery catalog (never scraped / non-partner / not a store product)
- Mahjong Studios Lunaflor (pippa): brand removed (Mahjong Studios, remove_mats.brands)
- Mary Benson Hydrangea (willow): not in gallery catalog (never scraped / non-partner / not a store product)
- Mary Benson Mary Benson (solara): held low-confidence list (held-low-98.json: mary-benson--blooming-tulips)
- Middle & Main Mahjong Painted Water Florentine (osler): not in gallery catalog (never scraped / non-partner / not a store product)
- Middle & Main Mahjong Peaches 'n Cream (talulah): held low-confidence list (held-low-98.json: middle-main-mahjong--peaches-n-cream)
- Middle & Main Mahjong Peaches and Cream (solara): not in gallery catalog (never scraped / non-partner / not a store product)
- Miss Mahjong Festival Jade (amara, jade, lagoon, willow): held low-confidence list (held-low-98.json: miss-mahjong--festival-jade)
- My Fair Mahjong Confetti Lemon Lime (amara, lagoon): hidden_oct20.csv: duplicate of my-fair-mahjong--confetti-green (audit: same mat, same photo (Confetti Lemon Lime = Confetti Gree
- Nawuno Nawuno (drake): not in gallery catalog (never scraped / non-partner / not a store product)
- Oh My Mahjong Regal Bloom (pearlescent): hidden_oct20.csv: already out (held low-confidence list); would also be hidden: wrong image: Oh My Mahjong "Regal Bloom (retired
- Splash of Color Preppy Animal Print (glow-wild): held low-confidence list (held-low-98.json: splash-of-color--preppy-animal-print)
- Tigre de Tartan Cannage Blonde (coquette, heritage-2-0, heritage, la-fete, luminaire, pearlescent, tortoise): held low-confidence list (held-low-98.json: tigre-de-tartan--cannage-blonde-w-rules)
- Tigre de Tartan Domino Oxblood (drake, heritage-2-0, heritage, malachite, tortoise): held low-confidence list (held-low-98.json: tigre-de-tartan--domino-oxblood)
- Tigre de Tartan El Último Refresco (gemma, heritage-2-0, heritage, moonlight, tortoise): held low-confidence list (held-low-98.json: miss-mahjong--el-ltimo-refresco)
- Tigre de Tartan French Mural (drake, heritage-2-0, heritage, palm-royale, tortoise, willow): held low-confidence list (held-low-98.json: tigre-de-tartan--french-mural)
- Tigre de Tartan Hearts & Horseshoes (gatsby, heritage, lola, moonlight, nantucket, tortoise): held low-confidence list (held-low-98.json: tigre-de-tartan--hearts-horseshoes)
- Tigre de Tartan Shell Yeah (birdie, coquette, luminaire, pearlescent, solara, sorbet, taylor): held low-confidence list (held-low-98.json: tigre-de-tartan--paige-spearin-shell-yeah)
- Wren Mats Dancing Poppies (drake, heritage-2-0, heritage, malachite, willow): held low-confidence list (held-low-98.json: wren-mats--dancing-poppies)

Notes: album "Birdie" (Lagoon) matched to the retired Birdie Green row (album name does not say which colorway). B&B Paradise Pink = gallery "The Paradise Passion Pink", and Isabel Harte = "Bamboo Dragon" (matched by hand).
