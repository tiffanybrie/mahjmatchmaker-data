# Pinterest launch kit (Oct 18)

Kit page (artifact): https://claude.ai/artifact/2kAMiQEnb3fSWdjayGTi7H. Nothing has been posted.

- pins/: 33 pins at 1000x1500. 20 album #1 match pins, 13 holiday pins (holiday pins are scheduled Nov 1 or later).
- pins.csv: Pinterest bulk-upload columns. Media URLs are pinned to jsdelivr commit b2233187 (Oct 18: wood-stain strips removed from Birdie, Glow Wild, Heritage 2.0, Jade, Malachite pins; see scripts/pinterest/woodfix/). jsDelivr sometimes returns a one-off 403 on a fresh commit; retry before scheduling.
- pinterest-profile-photo.jpg: flame heart on cream, for the profile photo.
- Built by scripts/pinterest/build_pins.py (takes the scratchpad pins dir).
- Planoly: the Pinterest channel @mahjmatchmaker is connected, with auto-publish on.

Approvals she needs to give:
1. "Approve updating my Pinterest profile."
2. "Approve claiming mahjmatchmaker.com on Pinterest." This is a live Squarespace header code injection.
3. "Approve creating the 10 Pinterest boards."
4. "Approve scheduling the 33 pins in Planoly."

## Done Oct 18 (approved in chat)
- Website claim: mahjmatchmaker.com was already claimed on her Pinterest account (Settings → Link to Pinterest shows it with an Unclaim button). There was nothing to verify, so I made no Squarespace code-injection change.
- Boards: her account already had 8 boards from earlier: Mahjong Discount Codes, Learn to Play Mahjong, Mahjong Mats & Racks, Mahjong Gift Ideas, Mahjong Table Inspiration, Mahjong Tile Matches, Oh My Mahjong Amara Tile & Mat Matches and All Things Mahjong!, plus the protected "Products you tagged". The kit assumed the account was empty.
- I created 9 new public boards, with the kit descriptions and no collaborators: Pink / Blue / Green / Neutral Mahjong Tiles and Mat Matches, Oh My Mahjong Tile and Mat Matches, Christmas Mahjong Mats, Holiday Mahjong Table Ideas, Mahjong Racks and Rack Colors, and Amazon Mahjong Finds.
- I didn't create "Mahjong Gift Ideas" because she already has a board with that exact name. I left her existing boards untouched.
- On the OMM board, I left out the "by a certified Oh My Mahjong instructor" clause because I couldn't verify it.
- The profile name, bio and photo are unchanged, and no pins were posted.
- Oct 18: match pins reworked per Tiffany: headline '[N] mats that match [set] tiles', CTA 'See all [N] of [set]'s matches', #1 pick shown as an example. Counts from live albums (scripts/pinterest/album_counts_oct18.json). Media URLs pinned to db299d7.
