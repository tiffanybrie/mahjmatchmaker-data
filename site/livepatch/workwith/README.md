# Work With page: styled code block (Oct 18)

Tiffany approved the v2 copy ("This page is approved"), then asked for styling: "It needs styled headings, etc., some images… We're cuter than this Claude ;)".

**Files**
- `workwith.html`: the code block to paste. Copy is her approved v2 word for word. The only added visible text is the "Partner brands" label on the logo strip, plus two button labels that reuse her own headings ("Say hello!" and "Ways we work together").
- `preview.html`: the preview, published to artifact Q8RhYaJwAxYHwXGLGavrEC.
- `build.py <commit>`: rebuilds both files. Images are pinned to jsDelivr at that commit, and `urls.txt` lists them. All 22 were warmed on Oct 18, with 0 failing.

**Design:** Caprasimo headings, pink #e05f86 and navy #1f2f5c, plus:
- a blush hero with a fan of 5 real match cards (Pippa + Vivienne, three Papaya Spritz cards, Solara + Vivienne)
- icon section cards and three "ways" cards
- a navy logo strip with 15 partner logos
- details/summary FAQ and a pink "Say hello!" band

Tested at 390 and 1280 with no sideways scroll. Everything is scoped under `.mmww`.

**Page**
- **Slug:** none of /work-with, /work-with-us, /for-brands or /partner exist yet. Suggested slug: **/work-with-us**. Keep it hidden from the nav, since the partner email links to it.
- **Building it:**
  1. Duplicate a simple page.
  2. Paste the block into a code block.
  3. Put the contact form block under it, so the "Say hello!" band's "form below" stays true.
- **SEO title:** Work With Mahj Matchmaker | Partner Program for Mahjong Brands
- **SEO description:** Partner with Mahj Matchmaker: get your own partner brand page, a spot on our Discount Codes page, and your tiles, mats and racks in Find Your Match. Players save with code MAHJMATCH.
- **Status:** not live. The live site was not edited.
- `preview_embedded.html`: the artifact copy, with images embedded as data URIs because the artifact viewer blocks outside images.

## Oct 18 afternoon updates (her feedback)
- Code de-emphasized: removed "Your code (MAHJMATCH) is front and center…" and the code chip in the Affiliate card. New line: "We focus on making your products highly visible with links and recommendations." The page no longer mentions the code.
- New releases card softened: "Let us know what's coming! We love hearing about new products, and we work them into matches and blog articles as they make sense." Also "your products are set up for…" → "can be set up for…".
- Find Your Match section: "Coming 10.27" tag + 4 phone-frame previews (assets/workwith/fym-step1..4), captured from the pending FYM build (new card design).
- Partner strip: ALL 36 partner brands as a slow marquee (pause on hover; static wrap with prefers-reduced-motion). 30 logos + 6 wordmarks.
- **To add a brand:** add its name to PARTNERS in build.py. If a logo exists in builder/logos/map.json (or add to EXTRA_LOGOS with the file in builder/logos/), it shows the logo, else a wordmark. Commit the logo, run `python3 build.py <commit>`, warm with `cd site/livepatch && python3 ../../scripts/jsdelivr/warm.py workwith`, rebuild preview_embedded.html.
