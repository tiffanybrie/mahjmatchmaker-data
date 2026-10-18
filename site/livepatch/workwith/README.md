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
