# Instagram engagement (Tiffany, Nov 12 2026 7:17am)

STANDING YES: "like partner brands' new posts every day." Claude likes every NEW feed post / reel from partner brands
(handles in config/social/ig-handles.json for brands on the partner list) from @mahjmatchmaker in her Chrome. No other
account, no old posts, no unliking. Log every like in config/ig-engagement-log.json.

EVERYTHING ELSE NEEDS HER YES, from a DAILY LIST (FORMAT CHANGED Tiffany Nov 12 7:26am, see below): comments, reposts (web has a Repost button), follows of non-partners,
replies. Each run builds ONE Claude Doc "Instagram today <Mon M/D>" (title + lead + one table: brand | post link | what it
is | suggested action (comment / repost) | draft comment in her voice), pushes a notification to her phone with the doc
link, and waits. She answers in that run's chat ("yes all", "yes 1 and 3, change 2 to ..."); only then the run posts
exactly what she approved, and logs it. No answer = nothing posted (roll the good items into tomorrow's list).

Voice: warm, short, a person not a brand ("Obsessed with this colorway!" / "These would be so pretty on a cream mat"),
no ™, no links, no codes, no hashtags, never mention Find Your Mat-ch unless she adds it. 3-6 items a day max.
Never COMMENT on or REPOST Mahjong Row & Co., Yellow Mountain Imports (off social), Paige Spearin x TdT. LIKES are fine on any of them when their posts come up (Tiffany Nov 12 7:25am: "You can like Yellow Mountain... That doesn't bother me. You don't have to go looking for it. It pops up. You can heart it"). Where this file and the scheduled task's prompt differ, this file wins.

Safety: modest volume (likes: newest posts only, pause 3-8 s between actions; stop at the first "Try again later" /
action block and log it). Never type a password, never solve a captcha, never DM, never tap buy links. One driver in
Chrome; close every tab you open, even on errors.

Reposts + our code (Tiffany Nov 12 7:20am): a repost may carry a short note with our code ("code MAHJMATCH saves you X%"),
that's how a repost earns. EXCEPT Tigre de Tartan: they asked us not to repost with our code (it shows up tied to their
content). Rare brands like that: list them here. No-code-on-repost: Tigre de Tartan. Draft each repost's note in the
daily list so she approves the wording.

FORMAT (Tiffany Nov 12 7:26am, overrides the doc/table/link wording above AND the task prompt): NO Claude Doc, NO table,
NO links to posts. The whole list goes straight into ONE chat message (SendUserMessage, which pushes to her phone):
one long scrollable list, each item = brand, a one-line summary of the post in words, the action (comment / repost),
and the exact comment or repost note. She scrolls, reads, and replies with anything NOT to send (or edits). Post only
after she replies (her reply is the approval for everything she didn't flag); no reply = nothing posted, items roll to
tomorrow. "I don't need another Planoly type situation."
