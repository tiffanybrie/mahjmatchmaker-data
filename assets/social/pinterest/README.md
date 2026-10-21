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
- Oct 18 14:15: Pinterest profile updated (approved in chat): name 'Mahj Matchmaker', bio from the kit, flame-heart photo. Website was already verified. Username unchanged.
- Oct 18 14:30: holiday table + Amazon pins reworked search-first (Tiffany: no How I'm Styling / Retro Rattan titles; keyword first). Board pins crop off the baked-in board titles and use a new header. Images at 081804d.

## Scheduled in Planoly (Oct 19, 2026, 3:50am ET), approved by Tiffany in chat: "Approve scheduling the 33 pins in Planoly."
- 33 pins scheduled to @mahjmatchmaker, auto-publish. Match pins: daily Oct 21 to Nov 9, 11am ET. Holiday pins: daily Nov 1 to Nov 13, 7pm ET (8pm on Nov 1).
- Images were uploaded directly (Planoly refuses jsDelivr and raw GitHub URLs), using the exact bytes from each pin's pinned commit.
- Fixed in the copy: Tinselle pin "the The Polo Club" → "The Polo Club".

## Oct 21 audit + always-on pipeline (Tiffany: "I don't want to have to monitor Pinterest")
- State found: only 3 live pins (Amara, Dec 30 2025). The Oct 19 batch of 33 had never fired because its first slot was Oct 21 11am ET; 0 failed. No holiday mood board or Amazon pin had gone live, so there is nothing to delete.
- The 6 holiday mood board pins were unscheduled, rebuilt from assets/blog/holiday-boards-oct21/ (commit 07e3806): Amazon-board versions use generic names only ("A Classic Plaid / Retro / Reindeer Holiday Table") and link to shopmy.us/mahjmatchmaker; blog versions keep the brand mats and link to our pages. Same Planoly drafts, rescheduled Nov 1-3 and Nov 11-13, 7pm ET.
- New: scripts/pinterest/autopin.py + config/pinterest/queue.json. Every album cover, own mood board/graphic and colour hub gets a 1000x1500 pin (assets/social/pinterest/pins/auto/). 14 new pins scheduled Oct 21-28 (2/day, 13:00Z + 20:00Z); 26 more pending in the queue.
- Daily scheduled task "Pinterest autopin (daily)" checks what published/failed, adds new pages from the sitemap, and keeps ~7 days of pins scheduled. Logs to HQ (area "Pinterest").
