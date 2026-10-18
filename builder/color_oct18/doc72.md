# 72 Color Sweep: every set under a color, plus lead-image fixes (Oct 18)

Tiffany said (07:38) that the yellow/orange chip didn't show the Sunday sets, Dear Santa wasn't under any color, Hummingbird was missing, and "some sets just haven't made it in."

## What changed in Find Your Match
- **Untagged sets:** 221 of 268 before (220 catalog sets plus December 1994). After: 12.
- **Still untagged (12):**
  - 8 black-back sets, because we have no Black chip: The Empress, Oakley, Neon Shadow, Art Deco, Hocus Pocus Halloween, Mahj-O-Ween, Celebration, Jet Set.
  - 3 entries that aren't tile sets: Mahjong Tile Takers, Giant Mahjong Tile (decor), Mischief Mahj (an event flyer).
  - December 1994, held back per doc 50.
- **Her calls:**
  - Sunday → Yellow & Orange (mustard backs).
  - Dear Santa → Ivory (her word, even though the old FYM photo showed dark green).
- **Album sets that had no color (proposed from the album photo):**
  - Hummingbird → Ivory
  - Brownstone Bloom → Ivory
  - Plum Panda → Purple
  - Nature Walk → Red (burgundy)
  - Papaya Spritz → Yellow & Orange
  - Petalée → Pink
  - Sunday Blues → Blue
- **Holiday sets now also have a color:**
  - Red: Rackin' Rudolph, Holly Jolly Rudolph Red, Tinselle Ruby Red.
  - Green: Grinch Green, Tinselle Emerald.
  - Pink: Sugarplum Pink, Nutcracker.
  - Blue: Nivalee Glacier Blue, Après Ski Club (teal backs).
- **New catalog sets added to Holiday (proposed):** Christmas Kiss, Nivalee Emerald Green, Glitter Glow, Nativity. Holiday sets stay out of non-holiday mat matches.
- **Every other catalog set** got a proposed back-color tag. The full list with a confidence for each is in config/tile-back-colors-proposed.json:
  - 144 clear
  - 37 likely
  - 28 where the back isn't in the photo, so the tag was guessed from the product color. These need her OK first.
- **Bug fixed:** a color list could only show one set per name, so Yellow Mountain's Seabreeze never appeared. Both Seabreezes now show under Blue.
- **Chip order** now matches the website: Holiday, Pink, Red, Blue, Green, Purple, Yellow & Orange, Brown, Ivory, Natural Patterns.
- Color = tile back only (doc 50 rule 2). Layer colors were not used for tags.

## Lead images replaced with her approved album photos (12)
- Sunday (her tile pile)
- Hummingbird (it was showing a cat photo)
- Plum Panda
- Brownstone Bloom (color-fixed pile)
- Papaya Spritz
- Petalée (pile)
- Holly Jolly Rudolph Red
- Nivalee Glacier Blue
- Tinselle Ruby Red
- Tinselle Emerald Green
- Après Ski Club
- Rackin' Rudolph

The other 44 album sets already matched.

## Website (not edited; needs her approval)
- **Color pages:** all 9 match FYM for the 37 live albums.
- **Chip rows:** the home page and /mahjong-tile-matches have identical chips (the Matches page also has Masculine and Request).
- **Problem: the "All Albums by Color" grid on /mahjong-tile-matches isn't actually grouped.**
  - It has no color headings.
  - Coquette is missing.
  - Pearlescent sits between the pinks and yellows.
  - Glow Wild (pink) sits among the browns.
  - Sorbet and Pippa (yellow) sit among the greens.
- **Problem: the home page has no by-color album grid at all.**
- **Fix:** replace that grid with the grouped block in builder/color_oct18/albums_by_color_block.html, which has color headings in chip order, and add the same block to the home page under Shop by Color.
- **Approval line:** "Approve updating the color sections on the home page and the Mahjong Matches page."
- When Sunday, Papaya Spritz, Petalée, Brownstone Bloom and the other almost-live albums go live, add each one to its color page and to this block.

## Needs Tiffany
1. A Black chip for the 8 black-back sets? Yes or no.
2. Remove the 3 entries that aren't tile sets from the catalog?
3. OK the proposed tags, especially the 28 where the back isn't shown (the My Fair Mahjong regional series, Middle & Main, the Oh My Mahjong Debutantes, Royal Mahjong Society Heirloom).
4. Papaya Spritz's shop link points to OMM's "jubilee-mahjong-tiles" page. Is that correct?
5. The vault albums (Lilac Soiree, Preppy Soiree, Shangri-La, Spring Love) aren't in FYM at all.

## Files
- config/tile-back-colors.json: the source of truth, kept identical to BACKG in FYM
- config/tile-back-colors-proposed.json
- builder/color_oct18/: props.py (each set's tag), buildimg.py, colorpatch.py, the before/after untagged lists
