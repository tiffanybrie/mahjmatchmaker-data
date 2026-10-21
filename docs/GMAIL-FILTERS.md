# Gmail filters + labels (set up Oct 21, 2026)

Tiffany's ask (Oct 21, 2:04pm): affiliate APPROVAL emails go straight out of the inbox. She only sees one when something is NOT approved. Referral ORDER emails are grouped instead of cluttering the inbox. Brand newsletters are organized. Site form mail is organized. People writing in (the /contact form, real people) stay prominent.

Re-importable file: `config/gmail-filters.xml` (Gmail > Settings > Filters and Blocked Addresses > Import filters; tick "Apply new filters to existing email").
Generator: the queries below are the source of truth. Edit them here and in the XML together.

Rules: no filter deletes or forwards anything. "Skip Inbox" (archive) is the strongest action. Declines, the contact form and real people are never archived.

## Accounts
| Account | Filters | Notes |
|---|---|---|
| mahjmatchmaker@gmail.com (brand inbox; Gmail connector account) | 10 filters, imported Oct 21 and applied to existing mail | Labels created with colours via the connector. |
| tiffanybrie@gmail.com (personal; Squarespace form notifications + many UpPromote/OMM/PayPal affiliate emails) | 10 filters, imported Oct 21 and applied to existing mail | She has older personal filters there too; they were left alone. |

## Label tree
- Affiliate/Orders (new referral orders; archived, still unread so she can glance)
- Affiliate/Approved (referral order approved; archived + marked read)
- Affiliate/Payouts (commissions paid out; archived)
- Affiliate/Needs a look (declined / rejected / reversed / failed; STAYS in inbox, marked important)
- Affiliate/Programs (applications, account approved, verify email, coupon assigned, payment-info OTPs; STAYS in inbox, label only. A newly approved affiliate is her setup task.)
- Brands/Newsletters (mahjong brand marketing email; archived)
- Brands/Partners (real brand people writing to her; hand-applied, no filter, because brands send newsletters, affiliate notices and personal mail from the same addresses)
- Site/Album requests (Squarespace "Form Submission - Album Requests"; stays in inbox)
- Site/Contact form (any other Squarespace form submission, which means the new /contact form; stays in inbox, starred + important)
- Site/Share your table ("Form Submission - Share Your Table"; stays in inbox)
- Site/Signups (Squarespace "Email Subscriber Report"; archived)
- Site/FYM feedback (Squarespace "Form Submission - FYM Feedback" from /find-your-mat-ch-feedback; archived + marked read. CLAUDE reads this label daily and handles it; Tiffany never sees it unless a decision only she can make comes out of it. Tiffany, Oct 21 3:14pm.)

## Subject wording found in the survey (60 to 90 days)
| Platform / sender | Order | Approved | Paid | Account |
|---|---|---|---|---|
| UpPromote (no-reply@secomapp.com, or the brand's own address such as joanna@andersruff.com, Partnerships@macandmillermahjong.com, affiliates@tigredetartan.com, emilyk@birdandbamboo.com) | "Great news! A new referral order has been tracked." / "A new BMD referral order has been tracked" | "Your referral order has been approved, check your Affiliate account." / "Your BMD referral order…" | "You've got new earnings, check your account now!" | "Your affiliate account has been approved / is being reviewed", "[Brand] Verify your email address", "Confirm Your Payment Info Update" (OTP), "You have been assigned a coupon code" |
| GoAffPro (no-reply@goaffpro.com, info@peacelovemahjong.com) | "New referral order" (the body shows the order amount and commission) | (none sent) | (none seen) | "Verify your account to get started", "Congrats! Your … Affiliate Account has been Approved!" |
| Peachs | "You referred a new affiliate order" | | | |
| ShopMy | "Week of Oct 12 · You earned $…" / "You received your first commission!" | | | |
| PayPal | | | "UpPromote: Schedule payment", "Affiliate Payment", "August OMM Affiliate Payment", "You've got money" (body names the affiliate program) | |
| Bespoke Mahjong | | | "Affiliate Payouts / Please Check Your PayPal Email" | |
| Rakuten (Etsy program) | | | | "Your application has been declined", the only decline in mahjmatchmaker@ |
| Bam Bird Boutique (tiffanybrie@) | | | | "We're so sorry your affiliate account has been denied." |
| Squarespace | | | | "Form Submission - Album Requests" (tiffanybrie@), "Form Submission - Share Your Table" (mahjmatchmaker@), "Email Subscriber Report" (weekly) |

No "referral declined / rejected / reversed" email from UpPromote or GoAffPro turned up in either inbox. The Needs-a-look filter covers whatever wording comes later.

## Filters (Gmail query, then action)
NEG = `-subject:(declined OR rejected OR reversed OR refunded OR refund OR cancelled OR canceled OR voided OR denied OR failed OR "not approved" OR "on hold")`. It is on every archiving affiliate filter, so a decline can never be archived.

1. **Needs a look**: `subject:(declined OR rejected OR reversed OR refunded OR cancelled OR canceled OR voided OR denied OR "not approved" OR failed OR "on hold") (subject:(referral OR commission OR commissions OR affiliate OR affiliates OR payout OR payouts) OR from:(secomapp.com OR goaffpro.com OR uppromote.com OR refersion.com OR shopmy.us OR rakutenadvertising.com OR awin.com OR impact.com OR shareasale.com))` → label Affiliate/Needs a look, mark important, never spam. Stays in inbox.
   - v1 looked for the affiliate words anywhere in the body. In tiffanybrie@ that tagged about 70 Amazon, Zappos, Etsy and news emails (label + important only, nothing archived). v2 (above) requires the affiliate word in the subject or an affiliate-platform sender. See "Status" for the cleanup.
2. **Approved**: `subject:("referral order has been approved") NEG` → skip inbox, mark read, label Affiliate/Approved.
3. **Orders**: `(subject:("referral order has been tracked" OR "new referral order" OR "referred a new affiliate order") OR (from:shopmy.us subject:("you earned" OR "first commission"))) NEG` → skip inbox, label Affiliate/Orders.
4. **Payouts**: `(subject:("new earnings" OR "affiliate payout" OR "affiliate payouts" OR "commissions have been paid" OR "commission has been paid" OR "payout sent") OR (from:paypal.com (uppromote OR goaffpro OR affiliate OR commission))) NEG` → skip inbox, label Affiliate/Payouts.
5. **Programs**: `subject:("affiliate account" OR "affiliate program" OR "affiliate partner" OR "assigned a coupon code" OR "assigned you a coupon" OR "UpPromote Marketplace" OR "Payment Info Update" OR "invited you to join") -subject:("referral order") NEG` → label Affiliate/Programs, never spam. Stays in inbox.
   - The `-subject:"referral order"` part was added after the first run, because the approval subject contains "check your Affiliate account". The stray label was removed from 30 approval threads in mahjmatchmaker@.
6. **Brand newsletters**: `(mahjong OR mahj OR mahjongg) unsubscribe -"affiliate program" -from:(pinterest.com OR facebookmail.com OR squarespace.info OR squarespace.com OR secomapp.com OR goaffpro.com OR uppromote.com OR shopmy.us OR paypal.com OR rakutenadvertising.com OR refersion.com OR awin.com OR evite.com OR signupgenius.com OR paperlesspost.com OR planoly.com) -subject:(referral OR commission OR commissions OR affiliate OR affiliates OR payout OR earnings OR approved OR declined OR rejected OR invoice OR receipt OR order OR shipped OR shipping OR delivered OR "your account" OR verify OR verification OR password)` → skip inbox, label Brands/Newsletters.
   - Needs both a mahjong word AND "unsubscribe", so a person writing in (no unsubscribe footer) is never caught. Order, shipping and receipt emails from brands stay in the inbox. Mahj Mood sends its updates from a plain Gmail address with no unsubscribe link, so those stay in the inbox.
7. **Album requests**: `from:form-submission@squarespace.info subject:("Album Requests" OR "Album Request")` → label Site/Album requests, never spam. Stays in inbox.
8. **Share your table**: `from:form-submission@squarespace.info subject:("Share Your Table")` → label Site/Share your table, never spam. Stays in inbox.
9. **Contact form**: `from:form-submission@squarespace.info -subject:("Album Requests" OR "Album Request" OR "Share Your Table" OR "FYM Feedback" OR "Find Your Mat-ch Feedback")` → star, mark important, label Site/Contact form, never spam. Stays in inbox. It catches ANY other Squarespace form, so a new form lands here (prominent) rather than being hidden.
11. **FYM feedback** (added Oct 21, 3:40pm; NOT YET IMPORTED, see below): `from:form-submission@squarespace.info subject:("FYM Feedback" OR "Find Your Mat-ch Feedback")` → skip inbox, mark read, label Site/FYM feedback, never spam. Account: mahjmatchmaker@gmail.com (the form's notification address). Requires the Squarespace form on /find-your-mat-ch-feedback to be named **FYM Feedback** (its notification subject is "Form Submission - FYM Feedback") and to email mahjmatchmaker@gmail.com. To install: Gmail (mahjmatchmaker@) > Settings > Filters > Import filters > config/gmail-filters.xml, tick only the FYM feedback entry (and re-import Contact form, whose query now excludes FYM Feedback).
10. **Signups**: `from:squarespace subject:("Email Subscriber Report" OR "new subscriber" OR "new subscribers")` → skip inbox, label Site/Signups.

## Brands/Partners (hand-labelled, mahjmatchmaker@)
Mahj Mood affiliate follow-up, Amore Mahjong customer-message reply, Let's Be Besties (Laurie), Four Winds Social ambassador thread, Golden Pond outreach, Mahjong Register thread. Add new brand-person threads by hand, or ask Claude to.

## Not filtered on purpose
- Real people (for example casey.magyarics@gmail.com) and partner replies: no filter touches them.
- UpPromote "Confirm Your Payment Info Update" OTPs stay in the inbox (time-sensitive). They get the Programs label.
- Pinterest, Facebook and other non-mahjong promos: untouched (Gmail's Promotions tab already holds them).

## Status (Oct 21, evening): DONE
- Both accounts run the current queries for all 10 filters. Needs a look is v2. Programs now matches `from:awin.com` instead of "invited you to join", which was catching Facebook, Slack and Redfin invites. Newsletters also excludes amazon.com, venmo.com, shop.app, redditmail.com, judge.me, etsy.com and lettuce.com. config/gmail-filters.xml matches.
- tiffanybrie@ cleanup:
  - Removed "Needs a look" from 71 wrong threads. Only the Bam Bird Boutique denial keeps it. The "important" marks were left alone because they can't be told apart.
  - Removed "Programs" from 19 personal invite threads.
  - Removed "Newsletters" from about 195 Amazon/Venmo/Reddit/Shop/judge.me threads, and moved the 25 from the last 30 days back to the inbox.
- Side effect fixed: during the cleanup, keystrokes landed as Gmail shortcuts and muted those 19 invite threads. They were unmuted, and the 5 that had been in the inbox were moved back. A stray star and an empty forward draft were removed.
- tiffanybrie@ already had her own filter "category:promotions → Skip Inbox", so brand promos there were mostly archived before this.
- mahjmatchmaker@ counts: inbox 1,040 → 765. Orders 48, Approved 30, Payouts 3, Needs a look 1, Programs 51, Newsletters 220, Partners 6, Share your table 1.

## Inbox cleanup Oct 21 (Tiffany's yes, 4:05pm ET)
Rule: archive only. Nothing deleted, trashed or marked spam. Filters skip the inbox and label `Promos/Unread` (Pinterest gets its own label `Pinterest`). Each filter was also applied to existing mail.

**Orders / Approved check (both accounts):** the Affiliate/Orders, Affiliate/Approved and Affiliate/Payouts filters are "Skip Inbox" in mahjmatchmaker@ and tiffanybrie@ (read from Settings > Filters). A search for `in:inbox` with those labels returns 0 threads in both accounts. They live only under their own labels.

### mahjmatchmaker@gmail.com (inbox 766 → 147 threads)
- New filter, Pinterest (`from:pinterest.com` minus security/billing/ads/login subjects) → skip inbox, label Pinterest. 599 threads archived (discover/explore/inspire/ideas recommendations, pinbot, activity). The Pinterest account security alert and "Website claimed" stay in the inbox.
- New filter, label Promos/Unread (31 threads archived): loveshackfancy.com, balticessentials.com, wrappedinacloud.com.
- Unsubscribed via Gmail's own header button: Baltic Essentials.
- Not unsubscribed (no one-click Unsubscribe in Gmail): LoveShackFancy (the link opened its website; closed, no data entered), Wrapped in a Cloud, all Pinterest.

### tiffanybrie@gmail.com (about 2,063 inbox threads in 90 days; 685 archived, about 1,378 left)
- New filter, Pinterest (same query as above) → skip inbox, label Pinterest. Ads payment, ads statement/receipt and account notices stay in the inbox on purpose.
- New filter, label Promos/Unread, one filter for 31 senders (685 threads archived, 673 never opened): news.bizjournals.com (Louisville Business First), fullfocus.co, joinreframeapp.com, wholesomeyum.com, iphonephotographyschool.com, onepeakcreative.com, foundr.com, thirdlove.com, roysreport.com, r.sofi.com, email.sharperimage.com, email.theblaze.com, noreply@helium10.com, thehustle.co, stofferhome.com, listings@redfin.com, babyfoode.com, shortform.com, hellofunnels.co, redditmail.com, e.avis.com, bonniechristine.com, newsletter.printful.com, engage.ticketmaster.com (UofL Athletics "gocards"), hautestock.co, email3.homeagain.com, dailypassport.com, emilyley@substack.com, every-tuesday.com, muneezaahmed.com, o.westelm.com.
- Unsubscribed via Gmail's header button (23): fullfocus, foundr, news.bizjournals, joinreframeapp, wholesomeyum, onepeakcreative, thirdlove, roysreport, r.sofi, email.sharperimage, email.theblaze, thehustle, stofferhome, babyfoode, shortform, hellofunnels, redditmail, e.avis, bonniechristine, newsletter.printful, engage.ticketmaster, hautestock, email3.homeagain, dailypassport, every-tuesday, muneezaahmed (26 counting all confirmed "You unsubscribed" screens).
- Filtered but NOT unsubscribed (Gmail had no one-click button, or it needs a third-party web page): iphonephotographyschool.com, helium10.com, redfin.com, emilyley@substack.com, o.westelm.com.
- Existing personal filters (category:promotions → Skip Inbox, etc.) were left alone.

### Left alone on purpose (unsure, flag for Tiffany)
- Stacie Bloomfield (classes@staciebloomfield.com, "[LEV] Module..." course emails, 32 unread): looks like a course she is in.
- o.westelm.com and hautestock.co "[MEMBERS]": both sent a real appointment confirmation / member mail; they are archived, not deleted. Remove them from the tiffanybrie@ Promos/Unread filter if she wants those in the inbox.
- Adobe, Experian, Amazon, PayPal, Venmo, SignUpGenius, school/Seesaw/SportsEngine, Oldham County, dance studio, bank alerts, Squarespace, Etsy: transactional or personal, untouched.

### KEEP list (never filtered)
Tucker Carlson Network, Mary Benson Art (studio@marybensonart.com), orders/receipts/shipping/delivery/purchase notices, real people (Casey etc.), partner brand people (Oh My Mahjong, Anders Ruff, Royal Mahjong Society, Mahj Mood, Four Winds Social, Let's Be Besties, Amore Mahjong, Peace Love Mahjong), Squarespace form submissions, Affiliate "Needs a look" + "Programs", security/account/password/bank/bill mail, school/family/calendar/evite mail.
