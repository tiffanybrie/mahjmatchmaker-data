# What's Live ledger
Artifact: https://claude.ai/artifact/9mwKRfRbQRAoBLknJCcpL9 (page source: whats-live.html)
Rows live in that artifact's db collection "status". Fields: area, name, stage (you|us|today|approved|live), who (Tiffany|Claude|Done), next, order, updated (ms), and optionally album {cards, order, page, fym}.
To update: ArtifactData update on status/<id> (change stage/who/next, set updated). rows.json is the Oct 18 seed snapshot.
HQ links to it with needs/whats-live-ledger.
