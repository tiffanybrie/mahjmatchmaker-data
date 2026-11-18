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

REPOSTS ARE HERS (Tiffany Nov 12 7:30am): Claude NEVER reposts and never drafts repost notes. She reposts from her phone
and adds her own "Add a thought" bubble with our code (the bubble shows on the original post in followers' feeds; other
brands do the same, so it's normal). No code in the bubble for brands that asked: Tigre de Tartan. The daily list
points out "worth a repost" posts (brand + what it is) WITH a suggested bubble note she can copy (Tiffany 7:31am: "you
can put those notes in there"). She expects to turn the list off soon: her Favorites feed now shows the partners, so
she reposts straight from it. When she says so, stop the list (likes keep going).

FORMAT (Tiffany Nov 12 7:26am, overrides the doc/table/link wording above AND the task prompt): NO Claude Doc, NO table,
NO links to posts. The whole list goes straight into ONE chat message (SendUserMessage, which pushes to her phone):
one long scrollable list, each item = brand, a one-line summary of the post in words, the action (comment, or "worth a repost" for her to do),
and the exact comment, or the suggested repost bubble note for her to copy. She scrolls, reads, and replies with anything NOT to send (or edits). Post only
after she replies (her reply is the approval for everything she didn't flag); no reply = nothing posted, items roll to
tomorrow. "I don't need another Planoly type situation."

CHROME CLOSED (Tiffany Nov 12 7:28am): the task runs at 2:23pm, 5:23pm and 8:23pm ET. Each run FIRST checks
config/ig-engagement-log.json: if today's list was already sent (or today's likes done), stop quietly. Then check
Chrome (list_connected_browsers / tabs_context_mcp). If Chrome is closed: send her ONE short message the first time it
happens that day: "Chrome's closed, so today's Instagram likes and list didn't happen. I'll try again at <next time>, or
reply 'it's open, do it now'." (record "chrome_closed_notified": <date> in the log so later runs don't repeat it). If she
replies in that chat, run the whole job right then. The 8:23pm run, if Chrome is still closed, sends a last one-liner:
"Instagram skipped today (Chrome closed all day)."
