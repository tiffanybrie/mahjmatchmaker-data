# PAYOUT RECONCILE: every tracked dollar is paid, pending, or chased (Tiffany Nov 4 2026, STANDING; Main owns money)

Her words (Nov 4 2:24pm): "every dollar that we've tracked in the money tab is either just not been paid out yet, or this is
how much of it has been paid out, this is where it went... nobody just doesn't pay... when should we expect to get paid?"

## Rules she set
- Payouts are CASH, almost always PayPal (a handful may be Venmo). The ONLY store-credit brand is Maison Mahj.
  Any other payout as store credit / gift card = flag (Nov 3: Peace Love Mahjong $402.88 as GoAffPro Store Gift Card;
  she is fixing the GoAffPro setting herself).
- Payment emails (PayPal "You've got money", network "commissions sent/paid" emails) land in mahjmatchmaker@ or
  tiffanybrie@: both inboxes are scraped.
- Moving tiffanybrie@ UpPromote accounts to mahjmatchmaker@: one brand at a time (Mahj Squad asked, no reply; Bird & Bamboo
  next maybe). Screenshot the dashboard + earnings history BEFORE any switch request. End state: two dashboards
  (UpPromote Marketplace + GoAffPro).

## The ledger (HQ Money tab, "Payouts" section; ArtifactData collection `payouts`)
Per brand: network · account email · payout method (PayPal/Venmo/store credit) · payout schedule + minimum (from the
program terms) · earned by month (from money docs) · paid (date, amount, method, where it landed: PayPal txn) ·
approved-unpaid · pending (in hold/refund window) · next expected payout date · status: OK / DUE / OVERDUE / WRONG METHOD.
Month view: "October earned $X · paid $Y · approved, not yet due $Z · overdue $W".

## Sources
- GoAffPro https://goaffpro.com/affiliate/payouts (+ per-store pending)
- UpPromote Marketplace https://marketplace.uppromote.com (payments tab) — mahjmatchmaker@ brands
- tiffanybrie@ UpPromote brand dashboards (each brand's own af.uppromote.com page; Payments tab), one at a time (sign-out
  problem: docs memory "UpPromote sign-in")
- PayPal activity (read only, never send/transfer): match each incoming affiliate payment to a brand + period
- Gmail both inboxes: "commissions ... have been sent", "You've got new earnings", PayPal receipts
- Program terms per brand (payout cadence, minimum, hold days) → config/payout-terms.json

## Cadence
Weekly (Mondays, with the sales close-out) + the 1st and 16th of each month. OVERDUE (past the program's stated date
+ 7 days, or no payout ever with approved > minimum) → HQ red needs card "Brand owes $X since <date>: ask them?"
(reaching out is HER call; Claude drafts the note).

## Payout Tracker (Tiffany Nov 6 4:20pm: "build the sheet")
Live page: https://claude.ai/artifact/Q3r6wMhYLqoyJSYnfKmtH2 (Dashboard type). Data = two attached CSVs (source of truth copies in docs/payouts/brands.csv + payments.csv).
WEEKLY (Main, standing): read PayPal + GoAffPro + UpPromote payment emails/dashboards, update both CSVs, upload_asset the new file, update datasets/<id> url+name+updated+edit. Every new payout lands in payments.csv the day its email arrives.

## Close October (Nov 7)
Payout Tracker top section 'Close October': payments.csv has account + for_month + sep/oct/nov split + how_sure; moves.csv logs PayPal->Byline transfers she tells us about (Claude never moves money). Safe to move = PayPal October money - moved. Update both files and re-upload when a payout lands or she moves money.
