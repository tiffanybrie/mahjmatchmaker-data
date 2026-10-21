# The Desk

See CLAUDE.md. Rewritten nightly by the end-of-day desk cleanup.

## In progress / don't drop
- (Oct 21 4pm) /find-your-mat-ch-feedback page is LIVE but unlinked and still shows the album-request form. Fix the form (fields: what were you doing / what happened or your idea / optional email; name "FYM Feedback"; notify mahjmatchmaker@gmail.com) or disable the page. The Gmail filter #11 import is pending too. Owner: the email/FYM visuals job, after v70.
- (Oct 21 4pm) The email + FYM page visuals wait on FYM v70 (banner name fix). Then re-capture, one QA pass, publish the hidden page, update launch step 0a and the trigger, update the Squarespace draft, reopen d-email-templates.
- (Oct 21) Waiting on Tiffany: mailing address for the email footer; yes for sender hello@mahjmatchmaker.com + DKIM + DMARC; standing yes for auto-posting feed pieces; keep or swap the no-commission bow lamp (ShopMy).
- [x] (Oct 21 ~5pm) ShopMy covers v3: all 20 uploaded after independent QA. Shelf order is set per Tiffany (Dice Dishes, Lamps, Etsy / Racks, Tablecloths, Amazon / Mahj & Vine, Tala, CMC / OMM x LSF, Mahjong House, Storage, then BJJ, Gifts, Merry, BAM, Halloween). The 5 CMC bags and totes are added to Mahjong Storage. Still open: the bow lamp (no commission), waiting on Tiffany.
- (Oct 21) Rule: only ONE agent drives Chrome at a time (stray keystrokes hit other tabs today).

## Oct 21 afternoon: Kerry cards into the live albums + thin-album shortlists
- [x] Checked the 11 Kerry cards (Coquette, Willow, Dandy, Pearlescent, La Fete, Sorbet, Moonlight, Luminaire, Birdie, Taylor, Talulah). Racks = current final_lists; tile photos = canonical album photos (no changes since render); no "Mahjong Social Club".
- [x] FAIL found: every card had the old "SHOP THE MATCH" footer (Oct 18 rule: every card carries MAHJMATCH). Re-rendered: 10 OMM cards say "10% OFF USE CODE : MAHJMATCH"; Coquette (LoveShackFancy x OMM, no code on tiles or mat) keeps SHOP THE MATCH, the documented Coquette exception.
- [x] Kerry ShopMy link verified: https://go.shopmy.us/p-96114928 -> Etsy listing 4493549326 (The Kerry). Gallery row (matgallery-v5.html + new53_rows.json) swapped from etsy.com to it.
- [x] FYM check: Kerry is NOT in any of the 11 sets' match lists (staged fym-oct21f) and its FYM url is still etsy.com. For the v70/v71 app fix, not published here.
- [x] LIVE: Kerry card #4 in all 11 albums + Coquette hero count 53/18 + /mahjong-mats Kerry row on ShopMy (curl + Playwright verified). README: site/livepatch/kerry-oct21/README.md.
- [ ] **FYM v71 (whoever builds it):** add Kerry (`www.etsy.com/listing/4493549326/the-kerry-mahjong-mat-watercolor-pink`) to the match list `m` of these 11 sets as Tiffany's real pick (album cards are live): pearlescent, moonlight, la-fete, willow, talulah, coquette, birdie, dandy, luminaire, taylor, sorbet. Racks per set = config/tile-racks-picks.json final_lists + mat racks (B&B Ballet Pink, Miss Mahjong Scalloped Iridescent Opal, Mahj Mood Scalloped Clear Acrylic). Set the mat's `u` to https://go.shopmy.us/p-96114928. Update locks.json + D.ao (album_order.py re-reads the live albums; Kerry is #4). Not Jasmine.
- [x] Job 2 built: thin-album swipe review https://claude.ai/artifact/UQy4YpGD2RR5Z1WqswJWYM (78 mats across Sorbet 8, Sunset 10, Limoncello 8, Gemma 9, Taylor 9, Jasmine 9, Nantucket 6, Pippa 11, Osler 8). Votes land in its db collection `votes` (doc id `<set>__<brand-name slug>`, fields v yes/no, set, key). Source: site/review/thin-albums-oct21/ (picks.py = the shortlist + rules, build_page.py).
- [ ] Waiting on independent QA. After it passes: add ONE Ready to Ship item under "This week", right after Brownstone, linking to the page; HQ points to it. Not before QA.
- (Oct 21) 10/27 launch checklist: Tiffany switches the FB group from Private to Public herself (Group settings → Privacy) right after the 'all-new Mahj Matchmaker' announcement. Put the exact taps in HQ Today that morning.
