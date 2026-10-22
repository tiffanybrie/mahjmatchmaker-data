# HQ + Ready to Ship daily cleanup

Written Oct 21, 2026, after Tiffany said (1:00pm): "you should be cleaning this out… I come in here and then I don't know where to go anymore." A scheduled task runs this every day at 6:47am ET. Any session can run it by hand. The steps below assume no memory of earlier conversations.

**Goal:** HQ is her one front door. When she opens it she sees **Today** (5 items or fewer), then **This week**, then a "Social → review in Planoly" button. Every item truly needs her: an answer, a yes, or a login only she can do. Nothing stale, nothing she already answered, nothing that is our job.

## 1. The two pages

| Page | URL | Where items live | How an item is hidden |
|---|---|---|---|
| **Matchmaker HQ** | https://claude.ai/code/artifact/Cor6pKtesou4mFRQ41P6Ye | db collection `needs` (one doc per item). Also docs `hq/now`, `hq/priorities`, `hq/launchPlan`, `hq/launchChecks`, `hq/albums`, `hq/launches`, `hq/links`, `hq/top`, `hq/social`. Collections `log`, `money`, `seo`, `talk`, `ideas` | `status`: `open` shows; `done`, `parked`, `archived` hide. Parked needs show in the Parking lot tab. |
| **Ready to Ship (RTS)** | https://claude.ai/code/artifact/RTtaTzgkN2ssmiAP3FxvJF | Items are defined in the page HTML: `const DEC=[...]`, `LOOK=[...]`, `G=[...]` (first long script line) plus injected items (`l-highlights`, `l-retired-tiles2`, `l-fb-*`, `l-papaya-v2`, `l-navplan-fym`, `l-template-shop`). Her answers are in db collection `ship`, one doc per item id. | A `ship` doc with `v` (`ok`/`chg`/`no`) or `archived: true` moves the item to "Answered". The `HIDE` regex in the page removes items entirely. The **"Ready for you now"** list is the `NOW=[...]` array in the page script; only ids in `NOW` with no answer show there. |

### How to read them
- Page HTML: `Artifact` action `read` with the URL. The result names a saved file; read long lines in parts (`sed -n 'Np' | cut -c...` or `grep -o`).
- RTS items list: the first long `<script>` line holds `DEC`, `LOOK` and `G`. Eval it in node (`var DEC=...; LOOK; G`) to get `[id, title]` for every item.
- Data: `ArtifactData` `list` on `needs` / `hq` (HQ) or `ship` (RTS) with `out_dir` set to the scratchpad. Every write needs the doc's `version` as `if_version`. Prefer `batch` for many writes.

### HQ need fields the front door uses
`title` (one plain line), `line` (one plain line on what's needed), `link` + `linkLabel` (where she does it; omit when she answers in the HQ box), `when` (`today` | `week` | `box` for the permanent "Anything else" inbox), `order` (number, low first), `light` (`red` today / `yellow` this week / `green`), `due` (optional text like "By Sat Oct 24"), `status`, `showFrom` (ISO date, for parked items that come back), `archivedReason`, `archivedAt`. A need with no `when` falls back to its light: red → Today, yellow → This week.

## 2. Where the evidence lives (check before keeping OR archiving)
1. **Her answer is already in:** the need's `answer` field and the `answers` collection (HQ); the item's `ship` doc (`v`, `note`, `draft`) on RTS; the HQ `talk` collection; comments on either page (`ArtifactComments`).
2. **Work done since:** `git log --since=<3 days ago> -i --grep=<topic>` in `/home/claude/mahjmatchmaker-data`; `site/livepatch/<topic>/README.md` (each says STAGED or LIVE); `CLAUDE.md`; `docs/BRAND-GUIDE.md`.
3. **Social:** Planoly `list_post_groups` (Instagram workspace `019fc27c-0bef-7533-bc3f-030acc19a135` as of Oct 21; Pinterest stays in `019fc27b-964d-7279-8685-1f1bb7a7c3f5`). The plan is `docs/content-strategy-oct-dec.md`. Social items never live on HQ or RTS (see rule 4 below).
4. **Releases:** `config/release-calendar.json` (`items` + `upcomingAlbums`) and HQ `hq/launches`.
5. **Live site:** `curl -s https://www.mahjmatchmaker.com/<path>`, then grep. Never WebFetch it.
6. **Project docs** (claude.ai Project "Mahj Matchmaker"): 00 (top rules), 00a (brand guide), 99 / 99b (content timing + social plan). Repo copies are under `docs/` where they exist.
7. **Affiliate mail:** Gmail `mahjmatchmaker@gmail.com` (UpPromote/GoAffPro "referral order" emails).

## 3. The keep / archive test (apply to every open need and every RTS "now" item)
Keep it only if ALL of these are true:
1. It needs **Tiffany herself**: an answer, a yes, or a login only she can do. If the next step is ours (building, putting something live, watching a restock), it is not her need: archive it with "Claude's job" and do the work.
2. She has **not already answered** it anywhere in section 2 (including in chat: the main session must close items the same turn she answers).
3. It is **not superseded**: no later decision, rebuild or launch made it moot (e.g. Papaya launched, so every Papaya round is done).
4. It is **not social**. Posts, reels, stories, pins, episodes, schedules and captions live only in Planoly and are reviewed there. Archive social items with "Moved to Planoly". Exception: a decision only she can make that is NOT in Planoly becomes ONE short HQ need.
5. It is **not a new release we're holding.** "New release, not now" goes to `config/release-calendar.json` → `upcomingAlbums` (and the HQ Albums tab detail), never an HQ need.
6. It is **not a duplicate.** Two needs on the same topic: merge into one, archive the other with "Merged into …".

If it fails any test: set `status: "archived"` (HQ) or `archived: true` (RTS `ship` doc) with a one-line `archivedReason` and `archivedAt`. **Never hard-delete.** Never remove a page feature.

If it passes: rewrite it as one plain `title` + one plain `line` + a direct `link` to where she does it (RTS, a dashboard, a store page), or no link when she answers in the HQ box. Set `when`, `order`, `light`.

**Parked with a date:** an item that can't be done yet (e.g. "Etsy re-opens Oct 26") gets `status: "parked"` + `showFrom`. Each daily run reopens parked needs whose `showFrom` is today or earlier (`status: "open"`).

## 4. Ordering
1. Launch-critical first (anything that blocks the Tue Oct 27 Find Your Mat-ch™ launch).
2. Then today (things dated today, or blocking live money: affiliate links, codes).
3. Then this week, by due date.
- **Today:** 5 or fewer. Overflow moves to the top of This week.
- **Total open needs:** aim for 10 or fewer. If over, merge and park.
- RTS `NOW=[...]` must list only items still waiting on her, in the same order HQ points to them. If RTS has only a few, HQ needs point to them ("Open Ready to Ship") and RTS stays the place to tap yes on albums and cards.

## 5. Never add an HQ need without checking for an existing one
Before creating a need, list `needs` and search titles/ids for the same topic (brand, album, page, account). If one exists (open, parked or recently archived), **update that one** (reopen it if needed) instead of adding a second. One topic, one need.

## 6. The rest of HQ to refresh each run
- `hq/now`: what Claude is doing today and next (no stale dates).
- `hq/priorities`: 3-5 current priorities; nothing whose date has passed.
- `hq/launchPlan`: day-by-day from today to launch; past days get ✓ or are dropped. Old content moves into an `archived…` field inside the doc, never deleted.
- `hq/albums`: each album's real stage and owner (`tiffany` only when it truly waits on her).
  **Album status check (Tiffany, Oct 21 6:12pm: "it still says yours… there's 40 of them… Papaya Spritz is on the top").** Every morning, re-check every `hq/albums` item against reality before anything else. The page counts `owner==='tiffany' && stage!=='live'` as "Yours" (tab badge + chip), so that pair must be exact:
  1. **Live = done.** `curl -s -o /dev/null -w '%{http_code}' https://www.mahjmatchmaker.com/<set>-mahjong-tile-matches` (index: /mahjong-tile-matches; never WebFetch). 200 with the album title means set `stage:"live"`, `owner:"claude"`, link to the live page, detail "LIVE on the site". This catches albums that went live while HQ still said yours (Papaya Spritz and four From the Vault sets did on Oct 21).
  2. **"Yours" only with an open Ready to Ship item.** An album is `owner:"tiffany"` only if its id is in RTS `NOW=[...]` with no `ship` doc answer (or it has a swipe page she can open now, e.g. the thin-albums swipe). Everything else is `owner:"claude"`.
  3. **Honest non-her status** (the page's stage groups are fixed, so the status goes in the first words of `detail`): `VERY FAR ALONG` (stage `cards`/`swiped`), `STARTED, STALLED` (partial swipes; stage `swiped`), `NOT STARTED` (new-release swipe books; stage `swiped`), `UPCOMING` (config/release-calendar.json `upcomingAlbums`; stage `swiped`), banked items likewise. Each says Claude's next step.
  4. **Groups (Oct 21 night):** the Albums tab groups by each item's `group` field: `yes` (Needs your yes: owner tiffany, open RTS item or swipe page), `stalled` (Started, stalled), `building` (Claude building: VERY FAR ALONG), `notstarted` (Not started + UPCOMING), `banked` (e.g. Petalée), `live` (collapsed). Set `group` whenever you re-status an item; items without one fall back by stage/owner/detail prefix.
  5. Never delete an item; re-status it. After writing, the count of `owner==='tiffany' && stage!=='live'` must equal the number of open album items on RTS NOW plus open swipe pages. Log the before/after in the HQ `log` line.
- `hq/links`: no link that points social review anywhere but Planoly.

## 7. Upcoming albums list
`config/release-calendar.json` → `upcomingAlbums.items[]`: `{set, brand, added, why, state, swipeBook, when}`. Mirror the state in the HQ Albums tab (`hq/albums`, owner `claude`, detail starting "UPCOMING, not now"). As of Oct 21: **Green Light Gatsby (Anders Ruff)**, swipe book built (https://claude.ai/artifact/PNi1a7ckEZKQwxDs88sVJ7), after launch.

## 8. After the run
- Republish a page only when its HTML changed, to the SAME URL (`url` set), built from the freshly read saved HTML.
- Smoke-test the HQ front door at 390px (Playwright with a stubbed `claude.use` that feeds the real `needs` docs): no page errors, Today ≤ 5, no sideways scroll.
- Log one line in HQ `log` (area "HQ"): counts before → after.
- Commit any repo change (`git pull -q --rebase --autostash && git push -q`).

## Changelog
- **Oct 21, 2026 (6:12pm):** Albums tab fixed. "Yours" 40 -> 3 (Brownstone Bloom, Vivienne album order, thin-albums swipe; Petalée banked and taken out of Ready to Ship NOW); 6 albums found live and marked done (Papaya Spritz, Spring Love, Lilac Soiree, Preppy Soiree, Shangri-la, Sunday Tile Set); the rest re-owned to Claude with VERY FAR ALONG / STARTED, STALLED / NOT STARTED / UPCOMING. Daily album status check added in section 6.
- **Oct 21, 2026:** First cleanup. HQ open needs 19 → 9 (4 Today, 5 This week) plus the permanent inbox box; a parallel session adds "Review this week's posts in Planoly" as the 5th Today item; RTS "Ready for you now" 19 → 6. HQ got the Today / This week / Planoly front door and an `archived` status; RTS got an `archived` flag, a pointer to HQ, and a trimmed `NOW` list. Gatsby moved to `upcomingAlbums`.

## Rule (Tiffany, Oct 21 3:16pm)
When a draft changes or she rejects it, the matching HQ / Ready to Ship item is updated in the same turn: HIDE it (parked/archived, out of NOW; no "being rebuilt" notices: "Don't put it in front of me unless I can actually answer the question"), then reopen it in place when the new version is ready. Never leave an old draft up for review. The daily cleanup also checks for items whose draft has a newer commit and fixes them.

## FYM feedback (Tiffany, Oct 21 3:14pm)
Every day: read Gmail label **Site/FYM feedback** (mahjmatchmaker@gmail.com; filter in docs/GMAIL-FILTERS.md #11). Handle each one yourself: photo/colour/match/bug fixes go through the FYM gate + independent QA; reply to the sender only if they left an email and asked something. Log what you did. Surface to Tiffany only decisions only she can make (one HQ need, plain words). Never forward feedback to her inbox.

