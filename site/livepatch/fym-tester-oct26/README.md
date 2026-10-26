# Find Your Mat-ch tester page + user feedback form (DRAFT, Oct 26). Not live.
Tiffany's plan (docs/ANSWERS.md 2026-10-26 14:14): FB group + friends test Version 1.0 tonight; they get their OWN feedback form (not the partner form, not Dropbox). Partners stay on /find-your-mat-ch-feedback ("FYM Feedback") + Dropbox and stay high priority. Feedback is tagged by PUBLIC version (1.0, 1.1 ...; docs/FYM-VERSIONS.md). Never internal build numbers.

Files:
- `fb-group-post.md`: the group post (2 variants) + first comment. Posted only on her yes.
- `top-block.html`: code block ABOVE the form (pill "Version 1.0 · Tester week", headline, 2 lines, form-button CSS, version-tag script).
- `bottom-block.html`: code block BELOW the form ("Open Find Your Mat-ch" button → /find-your-mat-ch-preview, What's in Version 1.0, work-in-progress note, sign-off).
No discount-codes page link anywhere (ANSWERS 14:17). Copy uses "start with tiles or start with a mat" (ANSWERS 13:52).

## Same tool as the partner form
The partner/app form is a **native Squarespace Form block** named "FYM Feedback" on the hidden page /find-your-mat-ch-feedback, emailing mahjmatchmaker@gmail.com, where Gmail filter #11 archives it to `Site/FYM feedback` (docs/GMAIL-FILTERS.md, docs/PARTNER-FEEDBACK.md). The tester form uses the **same tool (a Squarespace Form block) but is a separate form with its own name, so its emails carry their own subject and their own label.**

## The page
Pages > Not Linked > + > Blank page. Title `Thanks for testing Find Your Mat-ch`, URL slug `/find-your-mat-ch-tester`. SEO: hide from search (Page Settings > SEO > Hide page from search results), same as the hidden preview page. Content, top to bottom, in one section:
1. Code block: paste `top-block.html` (whole file).
2. Form block (config below).
3. Code block: paste `bottom-block.html` (whole file).
Paste method (attended chat, own tab, one Chrome driver): CodeMirror 6 `v.dispatch({changes:{from:0,to:v.state.doc.length,insert:html}})` with `html` fetched from the pinned jsDelivr URL of the file (warm it first, doc 73). Never retype.

## Form block config ("FYM Tester Feedback")
- **Form name: `FYM Tester Feedback`** (exact: drives the email subject "Form Submission - FYM Tester Feedback" and the Gmail filter).
- Storage: Email → `mahjmatchmaker@gmail.com`. (Optionally also connect a Google Sheet in Storage for a running list.)
- Submit button label: `Send it to Tiffany 💕`
- Post-submit message: `Thank you!! 💕 Your note came straight to me. Send another anytime this week.`
- Fields, in order:
  1. **Which device were you on?** Radio, required: `iPhone` / `Android phone` / `iPad or tablet` / `Computer`
  2. **How did you start?** Radio, required: `I started with tiles` / `I started with a mat` / `I tried both`
  3. **What did you love?** Textarea, optional.
  4. **Anything confusing or broken?** Textarea, optional. Description: `Tell me what you were doing and what happened.`
  5. **A photo that looks off, or a partner brand product you couldn't find?** Textarea, optional. Description: `Brand + set or mat name helps a lot.`
  6. **Your name** Name field, REQUIRED (Tiffany 15:13: so she can match feedback to group members/friends by name).
  7. **Your email** Email field, REQUIRED.
  8. **Version** Hidden field, field name `VERSION`. Filled from the URL `?SQF_VERSION=1.0`.
- Version tag: `top-block.html` adds `?SQF_VERSION=1.0` to the page URL on load (skips inside the editor), so every submission carries `Version: 1.0`. When a new public version goes live, change `FYMT_VERSION` in top-block.html and the pill text, re-paste. **Untested:** confirm with ONE test submission that the email shows `Version: 1.0`. Fallback if Squarespace ignores it: the email's received time maps to the public version via docs/FYM-VERSIONS.md (Claude tags it when logging).

## Gmail (mahjmatchmaker@), installed by an attended chat
`config/gmail-filters.xml` has a new entry `mahjmatchmaker:fymtester`: `from:form-submission@squarespace.info subject:"FYM Tester Feedback"` → skip inbox, mark read, label **Site/FYM tester feedback**, never spam. The Contact form filter's exclusion list now also excludes "FYM Tester Feedback" (otherwise tester notes would land STARRED in her inbox). Import only those two entries (Settings > Filters > Import). Claude reads the label with the morning cleanup, logs each note with its version, and fixes what it can; partner notes in `Site/FYM feedback` are handled first.

## Still open
- The app's own "Something look off?" link still goes to the partner form (/find-your-mat-ch-feedback). Pointing it at the tester page would be an app change for 1.1 (gate + QA); not done here.
- After the 9am CT launch tomorrow, the button can stay on /find-your-mat-ch-preview (stays live) or switch to /find-your-match.
