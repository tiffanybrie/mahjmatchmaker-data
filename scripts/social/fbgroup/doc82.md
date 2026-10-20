# 82 Facebook Group - announcements rules (Oct 19)

Project doc 82. Written to the repo because the Projects tool wasn't available in this session. Copy it into the project as `claude/82 Facebook Group - announcements rules (Oct 19).md`.

## Why
The Facebook group (facebook.com/groups/mahjmatchmaker, about 2,400 warm members, private as of Oct 19) went quiet: new albums and Oh My Mahjong launches stopped getting announced there. Oh My Mahjong pays Tiffany 20% through Nov 25, and every group announcement drives commission. The group is the warmest audience we have.

## Standing rules (Tiffany, Oct 19)
1. **Every new album or tile launch gets a group announcement.** The album lives on the website, not in the group. The post links to the album page (link in the first comment).
2. **Upcoming launches are group content too.** "Coming soon from Oh My Mahjong / Miss Mahjong / any partner brand, here's the date." Tiffany often gets Oh My Mahjong news early (Elizabeth tells her). Take dates only from the launch watch and email watch records in HQ (ArtifactData https://claude.ai/artifact/Cor6pKtesou4mFRQ41P6Ye, doc `hq/launches`) or from what Tiffany says. No date yet = "date TBA" or a clearly marked [DATE/TIME] placeholder. Never guess. Share Elizabeth's early info only after Tiffany says it can go public.
3. **Planoly can't post to Facebook groups.** Claude posts group posts from Tiffany's account, and only on her explicit yes: in chat, or a Yes in Ready to Ship for that exact post. A yes on one post doesn't cover any other post.
4. **The new Facebook Page** (https://www.facebook.com/profile.php?id=61595649176717, linked to Instagram) gets a follow-ask inside group posts. Don't invite her personal friends to it.

## Her group-post style
**Lessons from the Oct 19 NEW ERA post (Tiffany rewrote mine):**
- **The headline uses Facebook's Heading (H1) style**, always. How: the headline must be its own paragraph (press Enter after it, not just a line break), then type "# " at its start and Facebook turns that line into a heading. Check that only the headline became H1.
- Headline in normal title case, never ALL CAPS. Her emojis on both sides, e.g. "📣💕The New Era of Mahj Matchmaker is Here! 📣💕 MUST READ!!"
- Lead with the biggest news (the larger announcement), not the newest launch. A launch is a section, not the headline, unless the post is only about that launch.
- One topic per post when there's a lot: album requests, partner brands and Find Your Match each get their own later post.
- Her voice: "SUPER busy... dreaming and building", "friends!", "I told you I've been busy!!", "save some really exciting things for later this week".
- Photos: group cover first, then every new album cover (eye-catching "whoa" carousel). Never let Facebook's link preview be the image.

Use the `d-fbpublic` NEW ERA post as the model:
- A headline with matching emojis on both sides (💕 ... 💕, 🧡💜💚 ... 💚💜🧡), in caps when it's news.
- Opens with "Hey guys!" and a warm line. Says "y'all".
- Short sections, each with an emoji header line (🖼️ The albums have a new home!).
- Album lists: one per line, emoji + brand + set name.
- Ends with "Happy mat-ching! 🀄💕" and "Links are in the first comment 👇".
- Links go in the **first comment**, one per line, each with an emoji and a label.
- Code line: "my code MAHJMATCH will get you 10% or more off at our partner brands" (or the exact % for one brand, from the discount codes page).
- Posts that push a purchase end with: "#affiliate"
- Photo: the album or set's color card or profile card, a tile photo, or the albums collage (assets/brand/fb-page/mahj-matchmaker-albums-post-1640x856.jpg).
- Facts only: say "from the vault" or "retired" only for sets marked retired in config/tile-retired.json. Use match counts from the album data, never rounded up.

## Post types
- **New album / launch day:** see scripts/social/fbgroup/papaya-launch-post.txt (Papaya Spritz) for the pattern: what she looks like, her official pair, my first dates and racks, "her album is already live with N matches", the code, a comment question.
- **Coming soon (several brands):** the reusable template is in scripts/social/fbgroup/coming-soon-template.txt.
- **Weekly discount codes post:** `d-fbcodes` in Ready to Ship.

## Order of operations right now (Oct 19)
1. NEW ERA announcement (`d-fbpublic`, refreshed Oct 19 with every album since Heritage 2.0 plus a Papaya plug and the Page follow-ask). It goes up **before Papaya Spritz launches**, so Papaya gets plugged and the launch earns.
2. A day or two later, the group goes public. That needs its own yes.
3. Papaya Spritz launch post (`l-fb-papaya`) on her launch day. The date is still TBA: Oh My Mahjong shows "Coming Soon" (checked Oct 19), and HQ says "week of Oct 19, date TBA".
4. First public posts: the discount codes and the albums.

## Files
- scripts/social/fbgroup/new-era-post.txt + new-era-first-comment.txt
- scripts/social/fbgroup/papaya-launch-post.txt + papaya-launch-first-comment.txt
- scripts/social/fbgroup/coming-soon-template.txt
- scripts/social/fbgroup/rts_fbgroup_add.py (Ready to Ship builder for these items)

## Disclosure rule (Tiffany, Oct 19, standing)
- Never put "I may earn a commission" on a visual or card.
- Disclosure goes in the caption only, as the least in-your-face option: #affiliate (or #ad) with the hashtags.
- Visuals can show "Code MAHJMATCH" like everyone else does.
