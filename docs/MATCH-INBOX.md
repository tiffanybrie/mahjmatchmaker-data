# MATCH INBOX: things one chat spotted that another chat must fix (Tiffany, Oct 26 5:39pm)

Any chat (Main/social, Ops, Matches & Catalog) that notices a match/catalog problem writes it HERE, the same turn, so she never has to relay it.
Matches & Catalog checks this file at the start of every reply (with DESK) and moves items to DONE with the build number.
Especially: **a PARTNER brand holiday mat (not Amazon/Etsy) that isn't in a holiday album** → say whether it's a late release (store published date) or one we missed, then match it and tag it Holiday.

Format: `- [date time] [who spotted] ITEM · why · fix wanted`

## OPEN
- Oct 26 5:37pm · Main (Tiffany found it testing) · **FYM BUG, fix before launch: a searched mat sticks at the front of every deck.** After she searched Britt Mills SOIRÉE Leatherette, every later tile set (incl. My Fair Mahjong Style of Your Life, after "start over" + shop by brand) still shows Soirée first. Cause (live v95): the search button sets `S.mfront=id`; `matDeck()` puts `S.mfront` first whenever `!S.seen[S.mfront]`; `resetFrom(level<=1)` clears `S.seen` but NEVER clears `S.mfront`, so on every new set/start over the old search comes back to the top. Fix: in `resetFrom`, level<=1 add `S.mfront=null;` (also clear it in any start-over/tReset path), and only front it for the set it was searched on. Add a gate check: after resetFrom(1), S.mfront must be null. Gate + independent QA + publish to both places as usual.
- Oct 26 5:39pm · Main · **My Fair Mahjong Peppermint Wishes + Plaid Tidings: partner HOLIDAY mats not in any holiday album.** Late releases: both published on myfairmahjong.com Oct 19 (after the holiday albums), and our scraper missed them until the Oct 25 catalog audit added them to FYM (`hol:true`). Fix: match them into the holiday albums (pink/red Peppermint Wishes; green/red Plaid Tidings), check they're in the gallery Holiday section.
- Oct 26 5:39pm · Main · Same check for the other partner holiday mats added late (Oct 25 audit): Bespoke Mahjong "It's a Vibe Holiday", Bespoke x Gray Malin "A Very Merry Getaway" (published Oct 22), House of Hearts Studio Peace on Earth, Soirée All Day holiday line (added Oct 21). Are they in holiday albums? If not, match + tag.
- Standing ask: the weekly/launch watch should flag every NEW partner holiday mat into this inbox the day it's found, so holiday albums never miss a partner mat again.
- Oct 26 5:40pm · Main · Peace Love Mahjong tile focus (details in DESK): OG Desert Dreams bf y 0.5→0.79 (MUST, shows blanks now); Merry Nutcracker →0.21 and OG Totally Teal →0.41 (better faces); other 5 fine.

## DONE
