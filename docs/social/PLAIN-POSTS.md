# Plain posts: facts only, no cute copy (Tiffany Nov 10 11:45am, STANDING)

Her words: "really matter-of-fact posts... friendly, but basically facts, because all this cute stuff requires me to
have to monitor it, and I don't have time to monitor it... we've got to make it so that these posts can just post
without errors." The cutesy matchmaking voice (profiles, "she's a ...", one-liners, hotline scripts) is retired.

What every album / launch post says, and nothing more:
1. What it is: "New album: <Set> by <Brand>."
2. When: release day/time, or "in stock now".
3. Where the answers are: "We matched N mats to <Set>. See them all in the album, or match it yourself in Find Your Mat-ch."
4. The code: "Use code MAHJMATCH to save <pct from config/code-truth.json>% at <Brand>."
5. Hashtags.

Claude does NOT write these captions freehand. Run `scripts/social/plain_post.py` (fixed sentences + content_lint).
If a post needs words the script can't produce, it is not a plain post and goes to Tiffany.
Graphics: plain labels too (Colors, Tile faces, Racks that match, Top mat match, N mats matched). No personality copy.
Retired: hotline/character reels, tile-set "dating profiles", one-liners. Do not build new ones unless she asks.
