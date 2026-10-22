# Email: lists, templates, schedule

**Rule (Tiffany, Oct 21, 2:13pm): Tiffany approves the templates once. Claude runs every send.** Never ask her to send, schedule or turn on an email. Don't ask her again about a template she has approved. A new kind of email (a template that doesn't exist yet) goes to her once, as a picture, on Ready to Ship.

Her words: "I don't want to have to deal with any of it. Don't come at me to send an email. That should be all in your court. I should just have to look at the templates you're using, sign off once, and never look at it again."

Tool: Squarespace Email Campaigns (on her plan since Oct 16; 500 sends a month, resets on the 15th). Admin: https://hexaflexagon-denim-nhf4.squarespace.com/config/marketing/campaigns. Brevo was dropped.

## 1. Lists (checked in Squarespace, Oct 21)

| Where people sign up | Where they land | Notes |
|---|---|---|
| Homepage "3. Get New Matches First" Newsletter block ("Homepage Email Sign…", button "Sign Me Up") | Storage **Squarespace**. Mailing list **None**. Confirmation email off. reCAPTCHA on. | The person becomes an email subscriber in Contacts. They are not added to any mailing list. |
| Find Your Mat-ch notify-me form (`site/livepatch/fym-teaser-oct21/`, the "Save the date" slot) | **Not live yet.** Live /find-your-match is the old "Coming 10.27" page and has no form. The staged teaser has a placeholder slot for a native Newsletter block. "Find Your Mat-ch Preview" (/find-your-mat-ch-preview) has no form either. | When the block is added, set Storage to **Squarespace**. Leave the mailing list at None, or use "Mahj Matchmaker Newsletter". Either way the subscriber lands in All subscribers. |
| "Save my spot" pre-launch hero (`site/livepatch/nav-plan` step 4) | **Not built.** The live homepage hero is still "Find the Perfect Mahjong Match". | Uses the same Squarespace storage, if it's ever built. |
| Forms with a "subscribe" checkbox (Request an Album, Share Your Table, Contact) | Smart segment "Form Submitters" (4–5 people) | Only the people who ticked the box count as subscribers. |

Lists and segments on Oct 21: All Subscribers (9), Email Subscribers (9), New Email Subscribers (9), Potential Customers (9), Form Submitters (5), Customers (0), SMS (0). The only real mailing list is **Mahj Matchmaker Newsletter**, and it has **0** contacts. Nothing feeds it.

**Decision: send ONE launch email to "All subscribers".** Squarespace sends each opted-in person one copy, so one email reaches everyone (homepage signups, notify-me signups, form subscribers) and nobody gets it twice. That is why the separate launch newsletter (RTS d-newsletter2) was merged into the launch email.

## 2. Templates

Source of truth: `site/email/build.py`. It holds the copy and builds `site/email/templates/<id>.html`, `site/email/shots/<id>.png` (600px) and `<id>-390.png` (phone), and `site/email/emails.json` (subject, preview, plain text). Run `python3 site/email/build.py shots`. The build fails (lint) on TEACHMAHJ, %, Amazon links, ®, "Find Your Match" or "Happy Mat-ching", or ™ used more than once in a body.

| id | Email | Kind | When | Subject |
|---|---|---|---|---|
| `launch` | "It's here!" launch tutorial | Campaign, one send | Tue Oct 27, 9:30am CT | It's here! Find Your Mat-ch is live 💕 |
| `welcome` | Welcome + 3 places to start + 3 blog reads (her Oct 18 note: add the blog) + IRL photo ask | Automation "Welcome new subscribers" | On subscribe, from launch | Welcome to Mahj Matchmaker! 💕 |
| `album-request` | Album request thank-you | Automation "Reply to form submission", trigger = Request an Album form only | On submit, from launch | Got it! Your album request is in 💕 |
| `album-exists` | "It's already in our library" | Sent by Claude (one-off campaign or a Gmail reply from mahjmatchmaker@) | When a request is for a set that already has an album | Good news, it's already in our library! |
| `album-live` | "Your album is live" | Sent by Claude to everyone who asked for that set | When a requested album goes live | Your [tile set] matches are here! 🎉 |

Every email:
- names Find *Your* Mat-ch™ (™ once)
- carries "Use code MAHJMATCH to save 💕", with no %
- has no Amazon links and no other code
- is signed "Happy mat-ching! xo, Tiffany"

Look: blush email background `#fbe3ea`, warm white content `#fffdfa`, cream header `#faf3ea` with the site logo (wordmark with the tagline ribbon), deep navy body text `#062a55`, pink headings/links `#d6336c`, heart-pink rounded button `#f56c8c`, Book Serif font pack.

Launch email = a Find *Your* Mat-ch™ TUTORIAL (Tiffany, Oct 21 3:13/3:14pm: "You can't preview the Find Your Match tool with match cards"). No match-card fan and no hero image (QA: weight). Re-captured from live v72 (Oct 21 night): 6 annotated steps, each ONE image (`step-sq1..6.jpg`, 560 wide: Caprasimo step title baked in above a real v72 screen with callout pills + pink arrows; step 1 also carries "Here's how it works") + one live caption from `scripts/fym_promo/tutorial.json`: 1 Pick your door, 2 Here's what these buttons do (♥ love it, ✕ not the one, ← Back, Tiffany's picks on/off, Holiday + colors), 3 Your shortlist (Next: add racks), 4 Pick 2 racks (tap × to swap, Make it official), 5 Make it official (view + Story/Post/Pin size, Save / Share), 6 Use code MAHJMATCH to save (every piece linked). Then the Start swiping button, "Hope you love it!", "Something look off or have an idea? Tell me here →" (/find-your-mat-ch-feedback) and the "Use code MAHJMATCH to save 💕" box. Images: `site/email/assets/fym/` from `scripts/fym_promo/capture2.py` + `render2.py` (same source as the page tutorial `assets/site/fym-tutorial/tut1..6.webp`). `python3 site/email/build.py shots cdn` writes pinned jsDelivr srcs for Squarespace; in cdn mode every src is absolute (wordmark pinned @dbce3d9) and lint fails on any relative src. Squarespace draft 6ad90449db1bc22351dc7e9d = one image section + caption per step (6).

Headlines are IMAGES (Caprasimo, brand colours, 2x, light PNGs, alt text) in all five emails: H1s, "Hi, I'm Tiffany!", section heads, step titles. Body stays live text. Squarespace font packs are web-safe stacks only: use **Book Serif** (= the Palatino, Baskerville, Garamond stack; checked in the editor Oct 21, Narrow Serif is the Times stack), the closest to Lora. Build lint: one "!" max and no ALL CAPS in subjects, every image has alt text, ≤600 KB images, live words ≥ 10 per image.

## 3. Approval

Ready to Ship item **`d-email-templates`**, "Email templates: approve once": screenshots of all five emails. It replaced d-newsletter2 and d-emails2, which are archived with "Merged into d-email-templates". HQ need: `needs/email-templates-approve` (This week, by Mon Oct 26).

Yes text: "On your yes, the launch email is scheduled for Tue Oct 27 at 9:30am CT to All subscribers (everyone who signed up on the site), and the automations are turned on at launch. You won't be asked again."

The only thing she has to give, once: the **mailing address for the email footer**. Squarespace requires it on marketing email (a P.O. box works). She types it in the note box.

Sender: Mahj Matchmaker <mahjmatchmaker@gmail.com>, unless she says otherwise. Squarespace emails that inbox a one-time verify link, and Claude clicks it.

## 4. Schedule

| When (CT) | What | Who |
|---|---|---|
| Tue Oct 27, 8:15am | Scheduled task "Launch day: send Find Your Mat-ch email + turn on automations" (`trig_01ErZyguaegwpM88rte63TfY`, runs on her MacBook for Chrome) checks `ship/d-email-templates`. If yes, it sets sender + address, schedules the campaign for 9:30am, and builds and turns on the 2 automations. If no, it does nothing, logs it in HQ and makes the HQ need red. | Claude |
| Tue Oct 27, 9:00am | Homepage hero switch (separate task `trig_011jdGGQRMhNGJVvBQw8tTZn`) | Claude |
| Tue Oct 27, 9:30am | Launch email goes out | Squarespace |
| After launch | Welcome + album-request automations run by themselves. album-exists / album-live are sent by Claude when the album pipeline hits those moments. | Squarespace / Claude |

Never send any email to her list without her one-time template yes. Never send twice: before scheduling, check Sent and Scheduled.

## 5. Status (update when it changes)

- Oct 21: Launch campaign built as a **draft** (composer `6ad90449db1bc22351dc7e9d`):
  - subject and preview set
  - recipients set to All subscribers
  - header logo on cream, the fan image linked to /find-your-match, text, the "Start swiping" button to /find-your-match, and the albums/code/sign-off section
  - not scheduled and not sent
  - Sender Details and Legal Address are empty (waiting on her address)
- Automations: not built yet. The Oct 15 "Reply to form submission" draft is the untouched Squarespace sample ("Thank you for getting in touch", trigger Any form). The launch-day task turns it into the album-request thank-you (trigger: Request an Album form only). It also builds "Welcome new subscribers" from `welcome.html`. The Oct 8 "Tag Contacts who fill out a form" draft is not ours.
- Notify-me form: not live (see §1). Until it is, the announcement bar's "Get notified" link (to /find-your-match) lands on a page with no signup.

## 6. How to build in the Squarespace email editor (Claude in Chrome)

- Use your own tab and close it when done.
- Composer text sections are ProseMirror. Click into the section, then dispatch `new ClipboardEvent('paste', {clipboardData: dt})`, where `dt` is a DataTransfer with `text/html`. Keyboard typing into the button label appends to the old text: press End, Backspace ×N, then type.
- Images: `fetch(<jsDelivr url>)` → `new File([...])` → set it on the second hidden `input[type=file]` (multiple) with a DataTransfer → dispatch `change`.
- Colour pickers: triple-click the hex field, type the hex, then press Return. Section colours apply to the selected section only. When nothing is selected, the side panel shows the GLOBAL email styles.
- Never click "Send to recipients" except in the launch-day task after approval.

## 7. Feedback (Tiffany, Oct 21 3:14pm: feedback must NOT hit her)
- Every FYM promo (launch email, FYM page, app page footer) links "Something look off or have an idea? Tell me here →" to the hidden page /find-your-mat-ch-feedback (Not Linked). Its form ("FYM Feedback": what were you doing / what happened or your idea / optional email) notifies mahjmatchmaker@gmail.com.
- Gmail filter (docs/GMAIL-FILTERS.md #11) labels it **Site/FYM feedback**, skips the inbox, marks it read.
- **Claude reads that label every day** (HQ cleanup task), fixes what it can (photo, match, bug: with the FYM gate + QA), and surfaces to Tiffany ONLY decisions only she can make, as one HQ need.

## Draft status (Oct 21, ~5:30pm)
- Squarespace draft 6ad90449db1bc22351dc7e9d rebuilt to match `templates/launch.html`: subject "It's here! Find Your Mat-ch is live 💕"; sections = logo, "It's here!" image, intro text, 5 × (step image with the title baked in + caption text), Start swiping button, tail text (Hope you love it! / Tell me here → /find-your-mat-ch-feedback / code / sign-off), footer. Every image has alt text. Font pack Book Serif. Not scheduled, not sent; Sender Details and Legal Address still empty (waiting on Tiffany).
- Image upload method that works in the email editor: select the image section with a real click, hover it, click REPLACE, click UPLOAD FILE, then set the section's own input[type=file] with a DataTransfer and dispatch change. (The UPLOAD FILE click may also open the OS file picker on her Mac; cancel it.) Text sections: focus the ProseMirror editor, execCommand selectAll + delete, then dispatch a paste ClipboardEvent with text/html.

- Oct 21 ~11:40pm ET: draft 6ad90449db1bc22351dc7e9d now has 6 step images (step-sq1..6, jsDelivr @fcf9fd1) with alt text and captions from `scripts/fym_promo/tutorial.json`. Upload method that worked: select the section, click REPLACE > UPLOAD FILE (the OS picker did not open), then set that section's own `input[type=file]` (DOM order, 0 = "It's here!", n = step n) via DataTransfer + `change`. Alt text = side panel > image row > textarea (native value setter + input event). Step 6 = duplicate caption, duplicate image, move the image down one.

## Changelog
- 2026-10-21 15:40: Launch email rebuilt as a FYM tutorial with real app screens (no match-card fan, no hero), Caprasimo headline images in all five, subject with one "!" and no ™, feedback link + routing. RTS d-email-templates hidden until the new version passes QA.
- 2026-10-21: First version. Lists checked, 5 templates built, launch draft made in Squarespace, RTS approve-once item, HQ need and launch-day scheduled task.
