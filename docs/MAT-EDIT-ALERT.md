# New mat alert + Mat Edit (social set): how to build one

Tiffany, Oct 30 9:05-9:06am: the Larkspur Mat Edit colour card should become the standing "New mat alert" + Mat Edit social piece, and Claude builds it with no help from her. She reviews it before anything posts.

**Builder:** `scripts/matcard/mat_alert.py`. It reuses the Larkspur card look from `scripts/matcard/matcard.py` (commits dbce3d9a, 7908fcc0): warm cream, a title in the mat's colour, flame-heart eyebrows, palette dots and album tile shots with their names. It also follows the newer brand-guide rules:
- Caprasimo headlines with no text shadow. The Larkspur card used Alfa Slab One with a white shadow, which is now against the rules.
- Story safe band y 269-1536. Feed band y 120-1230.
- Flat JPG output.
- Code MAHJMATCH on every frame, with no %.
- Find *Your* Mat-ch™ with "Your" in Playfair Display italic.

Fonts come from `scripts/social/tileprofile/fonts`, so nothing is needed from /tmp.

## The set (8 images, plus 2 contact sheets)
Every frame comes in two sizes: story 1080x1920 (`story-N-*.jpg`) and feed carousel 1080x1350 (`feed-N-*.jpg`). Output goes to `assets/social/mat-edit/<key>/`.
1. **alert**: NEW MAT ALERT, the mat name, "by <brand>", the brand's @handle (a visible mention on frame 1), the mat hero, a "Tiffany's N tile matches →" cue, and the site + code line.
2. **edit**: THE MAT EDIT colour card: the mat, its palette and the tagline.
3. **tiles**: TIFFANY'S TILE MATCHES, "<Mat> + N": every one of her real yeses as album tile photos, with names and a "retired" label where it applies.
4. **cta**: match-card style (the mat full size, one pick inset bottom-right), "See all N matches in Find *Your* Mat-ch™", www.mahjmatchmaker.com and a "Use code MAHJMATCH to save" pill. The link sticker goes on this frame.

## Command
```
# spec exists (config/matcard/<key>.json): pass her real yeses in her order
python3 scripts/matcard/mat_alert.py poppins --matches "Lola,Moonlight,Osler,Preppy Soirée,..."

# brand-new mat, no spec yet: crops the flat photo, measures + names the palette, writes the spec
python3 scripts/matcard/mat_alert.py <key> --mat-photo assets/launches/<handle>/<photo>.jpg \
   --name "Poppins" --brand "Oh My Mahjong" [--color "#d94784"] [--tag "Hot pink florals, ..."] --matches "..."

python3 scripts/social/center_check.py assets/social/mat-edit/<key>/{story,feed}-*.jpg
```
Options:
- `--cta-pick "<set>"`: by default the script picks the first cross-brand match that isn't retired (never the obvious same-brand pair, Oct 23 14:34).
- `--handle`: by default the handle comes from `config/social/ig-handles.json`.
- `--frames alert,edit,tiles,cta`: renders only those frames. A partial run rewrites the contact sheets with only those frames, so always finish with a full run.

The script exits 1 in four cases:
- a match has no album tile photo
- the brand has no verified handle
- any element sits outside the safe band
- any text is clipped

`meta.json` lists the brands shown and their handles, for Tag people.

## Rules (all settled; don't re-ask)
- **Matches = Tiffany's real yeses only** (a swipe book or album). Never Claude picks (CLAUDE.md rule 4). If she hasn't swiped the mat yet, build no Mat Edit: check `config/swipe-books.json` and HQ for an existing book first, because she never swipes twice (Oct 30 2:45am).
- **Racks are left off** unless she has picked them. The old Poppins spec carried launch-watch Bird & Bamboo guesses, and those were never her picks.
- **Palette names** made by `--mat-photo` are a best guess from a colour table. The hexes are measured. Fix any name that contradicts the brand's own colour words.
- **Find Your Mat-ch CTA:** only post once the mat is live in Find Your Mat-ch with her picks (Tiffany's matches = N). Check `config/fym-mats-snapshot.json` or the live app. If it isn't there yet, the post waits for the next FYM build. Hand the build to Matches & Catalog via `docs/MATCH-INBOX.md`.
- **Brands:** tag every brand shown (`meta.json` handles). The main brand goes in the caption; the rest go in Tag people. Every frame that shows a brand gets that brand's mention.
- **No code** on LoveShackFancy collab sets: say so in the caption. Never put a Tigre de Tartán set or mat in the same caption as MAHJMATCH (content_lint `tdt-policy`). Never use a Paige Spearin x TdT collab.
- **Caption:** follows the brand guide feed format and passes `python3 scripts/social/content_lint.py <file>`. The IG version uses @handles; the FB Page version uses brand names. Save it to `docs/social/mat-alert-<key>-{ig,fb}-caption.txt`.
- **LOOK at both contact sheets** before anything goes to HQ. `center_check` flags the small "retired" labels under single tiles on frame 3 and a ~10px wordmark offset; both are by design. Anything else that is off gets fixed.
- **Nothing is posted or scheduled** until she says yes. After her yes, it goes into Planoly per the CLAUDE.md social rules:
  - feed carousel + FB Page target
  - story frames as a reminder post, because frame 1 has a brand mention and frame 4 needs the link sticker

## Launch watch step (trig_01S2VsjwznnHev1uUbYmEwJq)
When a partner mat launches AND Tiffany's swipe book for it is complete, run the command above with her yeses, then:
1. lint the caption
2. look at the contact sheets
3. write one HQ need (light yellow, quick) with the story contact sheet inline (`img`, jsDelivr URL pinned to the commit) and both captions in `why`.
If her swipe isn't done, the launch watch builds the swipe book (or reuses the existing one), and the Mat Edit waits.

First one: Poppins (Oh My Mahjong), Oct 30. Files are in `assets/social/mat-edit/poppins/` and the post package is `docs/social/mat-alert-poppins-2026-10-30.md`.
