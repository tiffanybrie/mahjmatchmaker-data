# Site menu + Find Your Match as the star (draft, Oct 19)

These are drafts only. Nothing on the live site has changed. The mockups use the site's real logo, fonts (Shrikhand + Bitter), colors (pink #F56A8B, navy #1F3A6B, footer navy #013A5B) and images.

- Mockups: `mock/*.html` (built by `mock/gen.py`; screenshots made by `mock/shoot.py`)
- Screenshots: `shots/` (1280 desktop, 390 phone)
- Hero image for Squarespace: `assets/hero-fan-launch.png` (launch day) and `assets/hero-fan-prelaunch.png` (Coming 10.27). Transparent PNGs of the match-card fan.
- Replaces the menu part of the older "Menu, About and Community" Ready to Ship item (`site/livepatch/nav/nav_plan.md`). The About and Community page drafts there still stand.

## What it looks like

**Header (desktop):** logo · Mahjong Matches ▾ · Discount Codes · Blog · Shop · Community ▾ · **[♥ Find your match]** (pink header button, where "Private Lessons" used to be)

- **Mahjong Matches ▾:** All Tile Albums · Holiday Matches · Pink Tiles · Red Tiles · Purple Tiles · Blue Tiles · Green Tiles · Yellow & Orange Tiles · Brown Tiles · Ivory Tiles · Neutral Tiles · Masculine Sets · (Mat Gallery, later)
- **Community ▾:** About Tiffany (once /about is live) · Community · Facebook Group · Share Your Table · Request an Album
- **Footer:** Private Lessons | Rentals (as today) + new line: "As an Amazon Associate I earn from qualifying purchases."
- **Events:** Tiffany already took it out of the menu. It stays hidden (Not Linked). It does not go in the footer.

**Phone:** the menu (hamburger) lists the same five items. Mahjong Matches and Community open a second panel with a Back link. The pink Find your match button sits at the bottom of the menu. Optional extra: a small "Find your match" pill next to the hamburger (step 3b).

**Live check, Oct 19:** today "Mahjong Matches" is a single link to /mahjong-tile-matches, not a dropdown, and the header button is turned off. Step 1 creates the dropdown.

## Copy (brand voice, short)

| Spot | Pre-launch (now to 10/26) | Launch day (10/27 on) |
|---|---|---|
| Hero pill | COMING 10.27 | NEW · FIND YOUR MATCH |
| Hero headline | Find your match. | Find your match. |
| Hero line | Pick your tiles, then swipe through mats and racks that match them. Opens Tuesday, October 27. | Pick your tiles, then swipe through mats and racks that match them. Save your favorite as a match card. |
| Hero action | Email signup, button "Save my spot". Under it: "I'll email you the minute it opens. Until then, browse the albums." | Button "Find your match" → /find-your-match, plus text link "or browse the albums" → /mahjong-tile-matches |
| Under the action | (none) | First date's on us. Use code MAHJMATCH to save 10%. |
| Header button | Find your match → /find-your-match | same |

Second section on the homepage stays **New Tile Match Albums** (it's already second today). Everything below it stays as is.

## Squarespace steps

Do these in order. Each one can be checked on its own. Changing a page's Navigation Title or moving it into a dropdown **does not change its URL**, so no redirects are needed and Google sees nothing new.

### 1. Mahjong Matches dropdown
1. **Website → Pages.** Under **Main Navigation**, click **+** → **Dropdown** (older panels call it **Folder**). Name it `Mahjong Matches`.
2. Drag the existing **Mahjong Matches** page (/mahjong-tile-matches) into the new dropdown, at the top. Click its ⚙ → **General** → **Navigation Title**: `All Tile Albums`. Leave Page Title, SEO title and URL as they are.
3. Drag these pages from **Not Linked** into the dropdown, in this order, and set each one's Navigation Title:
   | Page URL | Navigation Title |
   |---|---|
   | /holiday-mahjong-matches | Holiday Matches |
   | /pink-mahjong-tile-matches | Pink Tiles |
   | /red-mahjong-tile-matches | Red Tiles |
   | /purple-mahjong-tile-matches | Purple Tiles |
   | /blue-mahjong-tile-matches | Blue Tiles |
   | /green-mahjong-tile-matches | Green Tiles |
   | /yellow-orange-mahjong-tile-matches | Yellow & Orange Tiles |
   | /brown-mahjong-tile-matches | Brown Tiles |
   | /ivory-mahjong-tile-matches | Ivory Tiles |
   | /neutral-mahjong-tile-matches | Neutral Tiles |
   | /masculine-mahjong-tile-matches | Masculine Sets |
4. Mat Gallery: add it as the last item when that page goes live (`site/livepatch/matgallery`).
5. Move the dropdown to the first spot in Main Navigation.

### 2. Community dropdown
1. **Main Navigation → + → Dropdown**, name `Community`.
2. Drag the existing **Community** page (/mahj-matchmaker-community) into it. Navigation Title `Community`.
3. **+** inside the dropdown → **Link**: title `Facebook Group`, URL `https://www.facebook.com/groups/mahjmatchmaker`, Open in new tab ON.
4. Drag **Share Your Table** (/share-your-table) and **Request an Album** (/request-an-album) in from Not Linked.
5. When the About page (/about) is published, drag it in as the first item with Navigation Title `About Tiffany`.
6. Final Main Navigation order: Mahjong Matches · Discount Codes · Blog · Shop · Community.

### 3. Find Your Match header button
1. Make the page first, so the button never 404s. Under **Not Linked → + → Blank page**, title `Find Your Match`, ⚙ → URL slug `find-your-match`.
   - **Before 10/27:** the page holds the same "Coming 10.27" hero as the homepage (headline, line, Newsletter block "Save my spot", the pre-launch fan image).
   - **On 10/27:** the page content is swapped for Find Your Match itself. The embed method comes from the launch plan (doc 54). The header button and the hero button already point here, so nothing else changes on launch day.
2. On any page, click **Edit**, hover the header, click **Edit Site Header** → **Elements** → turn **Button** on.
3. Click the button → **Button text** `Find your match`, **Link** `/find-your-match` (Private Lessons was set here before; it moves to the footer, which already has it).
4. The header has more items than before. If the nav wraps on a laptop screen, go to **Edit Site Header → Style → Logo** and bring the logo height down a little (the mockup uses about 72px on desktop).
5. On phones, Squarespace puts this button at the bottom of the open menu. That is what the phone mockup shows.

**3b (optional): pill next to the hamburger on phones.** Squarespace doesn't have a setting for this. It's one CSS rule in **Design → Custom CSS**. I'd test it in the preview first and only keep it if it looks clean:
```css
@media screen and (max-width: 767px) {
  .header-display-mobile .header-actions-action--cta { display: flex !important; }
  .header-display-mobile .header-actions-action--cta .btn { padding: .6em 1em; font-size: 13px; border-radius: 99px; white-space: nowrap; }
}
```
If Squarespace's header markup differs from these class names, the rule does nothing (no harm). The phone menu button and the big hero button still cover phones.

### 4. Homepage hero, pre-launch (on Tiffany's yes)
1. **Edit** the homepage. Section 1 (the pink floral hero) keeps its background photo. Section ⚙ → **Background** → **Overlay**: white, about 55% opacity, so the text reads.
2. Remove the old text box ("Find the Perfect Mahjong Match" / "Match mahjong tiles, mats, and racks across brands") and the old button.
3. Desktop layout, left half (Fluid Engine):
   - Text block (Paragraph 3, bold, all caps, navy pill look via Text Highlight or a small button): `COMING 10.27`
   - Text block, Heading 1: `Find your match.` (pink, Shrikhand, the site heading font)
   - Text block, Paragraph 1, navy: `Pick your tiles, then swipe through mats and racks that match them. Opens Tuesday, October 27.`
   - **Newsletter** block: one email field, button `Save my spot`, uses the existing mailing list. Post-submit message: `You're on the list! I'll email you on 10.27.`
   - Text block, small: `I'll email you the minute it opens. Until then, browse the albums.` (link "browse the albums" → /mahjong-tile-matches)
4. Right half: **Image** block with `assets/hero-fan-prelaunch.png`. Alt text: `Mahj Matchmaker match cards: Papaya Spritz tiles on the Regency Scalloped mat`.
5. **Phone layout** (toggle the phone icon in the editor): stack in this order: pill, headline, line, newsletter, small line, then the fan image. Center everything.
6. SEO: the page's H1 changes to "Find your match." The site title, SEO title and description stay as they are.

### 5. Homepage hero, launch day (Tue 10/27, morning)
1. Pill text → `NEW · FIND YOUR MATCH`.
2. Line → `Pick your tiles, then swipe through mats and racks that match them. Save your favorite as a match card.`
3. Replace the Newsletter block with a **Button** block: `Find your match` → `/find-your-match` (large, primary/pink). Next to it, a text link `or browse the albums` → /mahjong-tile-matches.
4. Under it, a small text block: `First date's on us. Use code MAHJMATCH to save 10%.`
5. Swap the image to `assets/hero-fan-launch.png`.
6. Phone layout: pill, headline, line, button (full width), text link, coupon line, image.

### 6. Shop My Finds page (new)
1. **Main Navigation → + → Blank page**, title `Shop My Finds`, ⚙ → Navigation Title `Shop`, URL slug `shop-my-finds`.
   - SEO title: `Shop My Finds: Mahjong Table Accessories | Mahj Matchmaker`
   - SEO description: `Tiffany's favorite mahjong table finds: holiday table looks, dice dishes, table lamps and affordable tile sets, all on her Amazon storefront.`
2. Drag it between Blog and Community.
3. Section 1 (background: the sand color from the site palette, or white):
   - Heading 1: `Shop My Finds`
   - Paragraph: `The little things that make a mahj table: holiday looks, dice dishes, lamps and sets that won't break the bank.`
   - Button `Shop my Amazon storefront` → `https://www.amazon.com/shop/heritagesig05`, open in new tab.
   - (Later) second button, outline style: `Shop on ShopMy` → `https://shopmy.us/shop/mahjmatchmaker`. Leave it off until ShopMy has her Amazon tag saved.
   - Small text: `As an Amazon Associate I earn from qualifying purchases.`
4. Section 2: **Add Section → Lists → Cards** (4 columns desktop, 2 on phone). One item per idea list. Images are in the repo at `assets/amazon-store/` (Sweet Jojo: `site/livepatch/nav-plan/mock/img/sweet-jojo.jpg`). Each item's button text `Shop the list`, link = that idea list's URL on the storefront (until the list exists, use the storefront URL), open in new tab.
   | Image | Title | Description |
   |---|---|---|
   | cover-holiday-mahjong-tables.jpg | Holiday Mahjong Tables | Three holiday table looks, budget friendly. |
   | cover-polo-club-holiday.jpg | Polo Club Holiday | Tartan, brass lamps and cognac leather. |
   | cover-retro-rattan-holiday.jpg | Retro Rattan Holiday | Red plaid, a ceramic tree and amber glass. |
   | cover-rackin-rudolph.jpg | Rackin' Rudolph | Santa red, gold bows and a reindeer dice box. |
   | cover-dice-dishes.jpg | Dice Dishes | Cute spots for your dice. |
   | cover-mahjong-table-lamps.jpg | Table Lamps | Cordless glow for game night. |
   | sweet-jojo.jpg | Affordable Sets | Sweet Jojo and other sets that won't break the bank. |
   | (navy card, no image) | See everything | Every idea list, all in one place. Button `Amazon storefront`. |
   The idea list names follow `assets/amazon-store/plan.md` (that storefront cleanup is its own approval).
5. Section 3 (blush background): Heading 2 `Shopping a partner brand?`, paragraph `First date's on us. Use code MAHJMATCH to save 10%.`, button `See all discount codes` → /mahjong-discount-codes.

### 7. Footer
1. Any page → **Edit** → hover the footer → **Edit Footer**.
2. Leave "Private Lessons | Rentals" as is. Do not add Events.
3. Add a full-width **Text** block under the three columns: `As an Amazon Associate I earn from qualifying purchases.` Paragraph 3, centered, white at about 80%.
4. The footer is shared, so this shows on every page, including every blog post with Amazon links.

### 8. Blog "How I'm Styling" posts (template for each post)
- First line under the title (small): `This post has affiliate links. As an Amazon Associate I earn from qualifying purchases.`
- Each item in the post: name + one short line + its own Amazon link (open in new tab).
- At the end: Button `Shop this table on my Amazon storefront` → the matching storefront post or idea list (or the storefront home).
- Partner-brand tiles/mats/racks keep their direct partner link + code MAHJMATCH, never Amazon.

## After each step
- Check the live page from outside (curl) after saving: one save in 35 didn't take on Oct 16 (doc 59).
- Click through the menu at desktop and phone width: every dropdown item opens the right page, Find your match opens /find-your-match.
- Nothing here uses jsDelivr images, so the doc 73 warm-up rule doesn't apply (all images are uploaded to Squarespace).

## Go-live order
- **On Tiffany's yes:** steps 1, 2, 3 (with the pre-launch Find Your Match page), 4, 6, 7.
- **Tue 10/27 morning:** step 5 + swap the /find-your-match page content to Find Your Match itself.
