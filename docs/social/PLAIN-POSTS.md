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

## Correction, Tiffany Nov 10 11:49am: facts, but in HER voice with a little excitement
"You could still have a little bit of excitement in it and try to write it in my voice, not just like new album, colon."
Not robotic. The template sentences are her own words (Nov 9 10:47am codes-post line): "The latest <Brand> set, <Set>,
releases <when>!" / "As always, I have an album for you" / "You can also match <Set> and her new partner mat, <Mat>, in
Find Your Mat-ch!" / "Use code MAHJMATCH to save N% at <Brand> 💕". Excitement = her exclamation points + 1-2 set-colour
emojis. Still no invented one-liners or personality copy.

## Sell what we have (Tiffany Nov 10 11:50am)
Say the depth of the library when it is true: e.g. "(plus an album for every Oh My Mahjong set ever made)" (plain_post.py --every-set). Tell people what they get, not just that a post exists.

## Speak to our depth (Tiffany Nov 10 11:59am)
Every Find Your Mat-ch line says how big the library is: "along with over 1,500 mats on the mahj market" (number from the live FYM snapshot, rounded down to the hundred; plain_post.py does it).

## The social system now (Tiffany Nov 10 12:05pm, STANDING)
Social = getting the album work she already did out into the world. No new concepts, no special content. For every album:
1. The album's intro carousel (the slides she approved) -> IG carousel, auto-post, brand collab + tag.
2. Every slide -> its own IG story frame, auto-post.
3. The same slides -> a reel (slides in order, slow zoom, cross-fades, album cover as reel cover).
4. Caption from scripts/social/plain_post.py. Group post from the same script.
Claude HANDLES this end to end, the moment the album is ready. She does not build or monitor it.

## Do it the moment it happens (Tiffany Nov 10 12:06pm)
Never hold work to batch it. Holding only means Chrome drops or something gets blocked later. Same usage either way: do it now.
