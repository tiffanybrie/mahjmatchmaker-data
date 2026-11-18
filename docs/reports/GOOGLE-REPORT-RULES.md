# Google & Revenue report: rule changes live HERE, not in the scheduled task

Why (Nov 8 2026): the report's scheduled task (trig_01LZjGfVneN3vKwweVXwbzub) runs on Tiffany's Mac. Her approval to use the Mac covers the task's exact instructions. Editing those instructions from a chat silently voids the approval, and every run after that falls back to cloud-only (no Google searches, no Search Console, no dashboards). That happened Nov 8 (two prompt edits at 1:17pm + 1:23pm), and she only found out because the report kept not showing up.

How it works now:
- The task already reads CLAUDE.md at setup, and CLAUDE.md points here. So any NEW rule for the report is added to this file (dated, with her words), never to the task's instructions.
- Changing the task's schedule or turning it on/off is fine from a chat (that doesn't void the approval).
- If the instructions themselves ever truly must change: do it once, and in the SAME reply tell her "the Google report needs a 30-second re-approve on your Mac: Claude desktop app > Scheduled tasks > Mahj Matchmaker morning Google & Revenue report > approve / Require this computer", plus one HQ Today card. Never edit and say nothing.

Two different ways the report stops (explain them separately):
1. TURNED OFF: her Mac is asleep/closed at 12:13pm ET, so the system switches the task off (reason: computer away). The cloud catch-up task (trig_013ZpyRxFivSKPoYTgSvVBU6, 10:43am / 1:43pm / 5:43pm) turns it back on and retries.
2. RUNS CLOUD-ONLY: the Mac approval is missing (instructions changed). Only she can fix this, on the Mac.

## Rules added after Nov 8 (newest last)
- Nov 9 2026 ~12:15am, Tiffany: "How can you honestly skip them? ... it has a column for every one of those. How do you just, like, not recognize that you didn't run it?" (the Nov 8 re-run checked AI Overview for 38 brands but never ran AI Mode, which docs/REVENUE-WATCH.md has required since Nov 6; the run also started searching before reading the setup docs).
  1. READ FIRST, THEN SEARCH. Read every setup doc the task lists (CLAUDE.md, ANSWERS last 3 days, REVENUE-WATCH fully, NORTH STAR, ai-overview-drop-oct29, RULES-ENFORCEMENT-AUDIT, this file) BEFORE the first browser step. The dailyLog gets a line "Read: <docs>".
  2. EVERY BRAND, EVERY COLUMN: each aiBrands row has overview, namesUs, otherCode, position AND aiMode (same query + &udm=50; AI boxes load late, wait ~5s before reading). A brand not checked gets notChecked: "<reason>" instead, never a silent gap.
  3. GATE: run `python3 scripts/checks/report_complete.py <seo.json>` before writing the seo doc. FAIL = finish the missing columns this run (or mark notChecked with the reason) and re-run. Never write a report that fails it without saying FAIL in the aiSummary.
- Nov 9 2026 ~12:15am, Tiffany: "Do you know where that traffic comes from ... You need to be in Squarespace Analytics." A traffic rise or drop is never explained by a guess. Read Squarespace Analytics > Traffic Sources (daily table: Direct / Search / Social / Email / Referral) for both weeks, plus Search Console Pages + Queries for both weeks, and say which source and which pages moved. Store it in sc.sources.


## AI OVERVIEW SOURCES, EVERY RUN (Tiffany Nov 12 2026 11:27am)
For every brand whose AI Overview does NOT name MAHJMATCH, write down the sources it cites (URL + type: IG reel,
IG /popular/ page, FB group post, Reddit, YouTube Short, codes page, coupon site) and which code each one feeds.
Compare against the brand's history in ALL earlier reports (not just yesterday) and against its sales. The money is
in the AI Overview; AI Mode is the easy one. Example (OMM, Nov 12): docs/google/aio-sources/2026-11-12-oh-my-mahjong.md.
Skip Wren Mats' wrong-code issue (Tiffany: not worth the time).

## AI OVERVIEW AND AI MODE ARE NEVER ONE NUMBER (Tiffany Nov 12 2026 7:58pm + 10:52pm)
The summary line and every table report "AI Overview names MAHJMATCH for X of N" and, separately, "AI Mode: X of N".
Never "AI answers", "Google AI" or any merged count (from Oct 31 the summaries said "AI answers" and the numbers became
untrustworthy). AI Overview first: it is the one that makes money.
