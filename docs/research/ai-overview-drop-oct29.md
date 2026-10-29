# AI Overview drop: 6 brands lost MAHJMATCH (checked Oct 29, 2026, ~3:30pm ET)

Main's delegated agent ran the check in Tiffany's Chrome on desktop, signed in, with `hl=en&gl=us`. Screenshots are in `assets/qa/google-oct29/`. Nothing on the live site was edited and nothing was posted.

## Per brand

| Brand (page) | Overview names MAHJMATCH? | Codes the Overview cites | Overview sources | Our organic pos | Google's last crawl | SC 28d (clicks / impr / pos) | SC 7d vs prev 7d | Re-index requested | Feedback sent |
|---|---|---|---|---|---|---|---|---|---|
| My Fair Mahjong (/my-fair-mahjong-discount-code) | **No** | TM10, MidlandMahj10, BRITTANYCRNA, MAHJMANIA, MYMAHJMOOD, MYMAHJONGLIFE | myfairmahjong.com, Instagram (901bam, paulaparkerclaxton), TikTok (brittanycrna), Stylin Brunette, WeThrift | #4 (after SimplyCodes, Goodsearch, FB group) | **Oct 9** | 6 / 500 / 6.0 | impr 133→110, pos 6.0→6.5 | Oct 29 | Yes |
| Peace Love Mahjong | **No** | LEMAHJ10, SETTHEMAHJ, Mahjonggmommas-PLM-10, BOOKANDACHAI, LUCKYM, MJTI, TroopMahjong10, bamsandbabes | peacelovemahjong.com, Instagram, WeThrift, Facebook, Missy Mahjong | #3 | **Oct 10** | 0 / 150 / 4.4 | impr 69→58, pos 4.5→4.3 | Oct 29 | Yes |
| Bespoke Mahjong | **No** | missy, Stylin10, MidlandMahj10, MAJMOM, MySweet10, HWOM, MJTI (group) | bespokemahjong.com, Instagram (Midland Mahj, mahjonggm…), Missy Mahjong, Stylin Brunette, Facebook | #3 | **Oct 2** | 2 / 160 / 6.4 | impr 67→93, pos 7.6→5.6 | Oct 29 | Yes |
| Mini Mahjer | **No** | TWOSPARROWS, simplymahj, MJTI, coastal, DEVINEMAHJONG, MODERNDAYMAHJ, GREENMAHJ, MJTARA, 901BAM | minimahjer.com, Simply Mahj, Facebook (DCMahj), Missy Mahjong, WeThrift, Instagram | **#1** | **Oct 4** | 1 / 97 / 4.6 | impr 28→38, pos 3.8→4.4 | Oct 29 | Yes |
| The Mahjong Co. (/mahjong-co-discount-code) | **Yes (recovered)**, listed with a link to us | MAGIC, MAHJANDTELL, GATHERING10, TAYLOR10, JAMI10, Birdbam10, MAHJCITYCLUB, **MAHJMATCH**, MARNIMAHJ | Facebook, Instagram, **mahjmatchmaker.com** | **#1** | **Oct 27** | 12 / 526 / 6.7 | impr 169→214, pos 6.2→6.3 | Oct 29 | Not needed |
| Hip Hip Mahjong | **No** | MAJMOM, MidlandMahj10, TroopMahjong10, LUCKYM, MAHJONGANDMICS | hiphipmahjong.com, Stylin Brunette, Facebook, Instagram, Missy Mahjong | **#1** | **Oct 3** | 2 / 53 / 2.3 | impr 18→35, pos 2.2→2.4 | Oct 29 | Yes |
| Oh My Mahjong (reference) | not re-checked today (Main checked it at 2:55pm: No) | | | #6 desktop (Main, 2:55pm) | Oct 27 | 0 / 126 / 11.3 | impr 25→76, pos 11.8→10.6 | Oct 29 (quota left) | n/a |

**AI Mode** (one check, My Fair Mahjong, `udm=50`): it **does** name MAHJMATCH, second under "Top Recommended Codes" after BRITTANYCRNA, and lists mahjmatchmaker.com as a source card. AI Mode and the Overview pull from different source sets.

**Search Console notes**
- 28 days vs previous 28: the previous period is all zeros because these pages are newer than 56 days, so that comparison can't show a drop. 7 days vs previous 7 (data runs through about Oct 27) shows **no ranking drop**. Positions are flat within ±0.6, and Bespoke improved by 2.0. Clicks per page are 0 to 5 a week, so the swings are noise. Impressions are up for 5 of 7 pages.
- URL Inspection shows "No referring sitemaps detected" on all 6 pages, and OMM shows "Temporary processing error" for its sitemap. Google isn't linking these pages to our sitemap.xml.
- Indexing requests today: YOLO and Let's Be Besties (earlier run), plus these 7, for about 9 of roughly 10 a day. All are recorded in HQ `hq/indexing` (v44).

## Likely cause, in plain words

1. **Google is still answering from an old copy of 5 of our 6 pages.** It last read My Fair, Peace Love, Bespoke, Mini Mahjer and Hip Hip between **Oct 2 and Oct 10**, before the Oct 27 "verified" refresh. The one page Google re-read after the refresh (**Mahjong Co., crawled Oct 27**) has MAHJMATCH back in its Overview today. So the fix that worked is a re-crawl, and the 5 others were requested today.
2. **The Overview prefers "many voices" over one page.** For codes, Google's AI now builds a list from Instagram reels, TikToks, Facebook group threads and code-roundup blogs (Stylin Brunette, Missy Mahjong). Influencer codes like MidlandMahj10, MJTI and MAJMOM show up on many brand-related posts. MAHJMATCH appears almost only on mahjmatchmaker.com, so even ranking #1 organically (Mini Mahjer, Hip Hip) doesn't put us in the Overview. We have no social or third-party mentions for it to quote.
3. **Rankings didn't fall.** Organic positions are #1 to #4 and Search Console positions are flat. This is an AI-citation loss, not a ranking loss.

## Next actions (in order)

1. **Instagram "partner codes" carousel + caption, with every brand name and MAHJMATCH typed out in text** (e.g. "My Fair Mahjong: MAHJMATCH (10%)"), plus a story version. The Overview quotes Instagram captions heavily. Main drafts it to the brand guide and puts it on HQ for her yes (new public content needs her approval), then it goes to Planoly with the Facebook Page as a target.
2. **Run the weekly FB group codes post (doc 94) now, not on its usual day.** Use the same typed-out format with brand names and MAHJMATCH, which is the format the Overview pulls from "Mah Jongg, That's It!"-style threads. Also post a version to the Mahj Matchmaker Facebook **Page**, which is public and crawlable, unlike a private group.
3. **Re-check the 5 stale pages on Nov 1 in URL Inspection.** If the last crawl is after Oct 27, re-run the Google search for each. If the Overview still omits us after a fresh crawl, cause 2 is the main one and actions 1 and 2 carry the fix. Add a rule to the code report: whenever a page's "verified" line changes, request re-indexing that day for every edited brand page, since the daily ~10 quota allows it. Most of the Oct 27 refresh was never re-requested.
4. **Fix the sitemap link-up.** Every brand page says "No referring sitemaps detected" (OMM: "Temporary processing error"). Resubmit `sitemap.xml` in Search Console → Sitemaps and check that the brand pages are listed there. Squarespace generates it automatically, so this is only a check plus a resubmit, with no site edit.
5. **On-page (next Ops paste, not today):** add `dateModified` (2026-10-27) to each brand page's schema, and put one plain answer sentence first, e.g. "The My Fair Mahjong discount code is MAHJMATCH for 10% off (verified Oct 27, 2026)." That gives the AI a clean line to quote. Also check that the /mahjong-discount-codes hub and the homepage link the 6 pages with brand-name anchor text, so Google re-reads them sooner. (Today's curl showed no `dateModified` on any of the 7 pages.)

Not done here: no live-site edits, no posts. Screenshots: `my-fair-mahjong-overview.jpg`, `peace-love-mahjong-overview.jpg`, `bespoke-mahjong-overview.jpg`, `mini-mahjer-overview.jpg`, `mahjong-co-overview.jpg`, `hip-hip-mahjong-overview.jpg`, `my-fair-mahjong-ai-mode.jpg`.
