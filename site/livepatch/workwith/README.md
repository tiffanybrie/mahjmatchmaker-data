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
- **Slug:** none of /work-with, /work-with-us, /for-brands or /partner exist yet. Suggested slug: **/work-with-us**. Keep it hidden from the nav. It is linked from the footer "Brands" form reply, the partner thank-you email and her affiliate applications.
- **Building it:**
  1. Duplicate a simple page.
  2. Paste the block into a code block.
  3. No form on this page (see the Brands form below).
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

## Oct 19: purpose and flow (Tiffany, 12:31am and 12:33am)
**What the page is:** a "why work with Mahj Matchmaker" page. She partners by applying to brands' affiliate programs, so the page must never ask a brand to introduce itself. It's used three ways:
1. **Reply to the Brands form:** brands that find us after Find Your Match launches fill in a simple form and get this page back by email.
2. **Affiliate applications:** she links it when applying to a brand's program.
3. **Partner thank-you email:** it's linked from the email to existing partners (`emails.md` #2).

**Copy changes (v6):**
- Removed "Say hello! Use the form below and tell me a little about your brand" and the hero's "Thank you so much for your interest in Mahj Matchmaker."
- Hero buttons are now "Ways we work together" and "See the matches."
- New closing band: **"Ready to partner?** Affiliate programs are set up on your end. Send your affiliate invite or sign-up link to mahjmatchmaker@gmail.com and I'll take it from there." The button is "Send your invite" (mailto).

## Brands form (staged, not live)
- **Where:** a new hidden page, /brands, with a Form block. Title "For mahjong brands", one line: "Tell me how to reach you and I'll send over how I work with brands."
- **Fields (keep it short):**
  - Brand name (required)
  - Your name (required)
  - Email (REQUIRED, which the automation needs)
  - Website (required)
  - What would you like to work on? (text area, optional)
- **Storage:** email to mahjmatchmaker@gmail.com, and submissions are kept in Squarespace (Profiles / form submissions). Don't add a mailing-list opt-in; this isn't a newsletter signup.
- **Post-submit message:** "Thank you! Check your inbox. I just sent you how I work with brands."
- **Footer link:** add a small link in the footer text block next to the email: `<a href="/brands">Brands</a>`. The label can be "Brands" or "Work with us".
- **Auto-reply:** Squarespace Email Campaigns → Automations → **Form response** trigger, connected to the Brands form, using the email in `emails.md` #1. Squarespace says form-response automations can "connect to any form block on your site" and fire when "a visitor submits a form response that included their email address", but "will only send if the email field is required" (support.squarespace.com/hc/en-us/articles/360002077567-Sending-automated-campaigns). She has the Email Campaigns plan (doc 59).
- **Fallback** if the automation won't connect: a saved Gmail reply (template) she sends herself.
