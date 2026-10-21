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
9. **Contact form**: `from:form-submission@squarespace.info -subject:("Album Requests" OR "Album Request" OR "Share Your Table")` → star, mark important, label Site/Contact form, never spam. Stays in inbox. It catches ANY other Squarespace form, so a new form lands here (prominent) rather than being hidden.
10. **Signups**: `from:squarespace subject:("Email Subscriber Report" OR "new subscriber" OR "new subscribers")` → skip inbox, label Site/Signups.

## Brands/Partners (hand-labelled, mahjmatchmaker@)
Mahj Mood affiliate follow-up, Amore Mahjong customer-message reply, Let's Be Besties (Laurie), Four Winds Social ambassador thread, Golden Pond outreach, Mahjong Register thread. Add new brand-person threads by hand, or ask Claude to.

## Not filtered on purpose
- Real people (for example casey.magyarics@gmail.com) and partner replies: no filter touches them.
- UpPromote "Confirm Your Payment Info Update" OTPs stay in the inbox (time-sensitive). They get the Programs label.
- Pinterest, Facebook and other non-mahjong promos: untouched (Gmail's Promotions tab already holds them).
