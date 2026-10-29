# Sunday Sets swipe book rebuild (Oct 29)
Artifact WJT7jTYfXX45917UkEqKyq (db `sundaysets`, votes keyed `<group>__<itemid>` — ids unchanged).
1. map.py: old items -> FYM b101 mat keys (handle, then name+brand, then fuzzy; manual fixes inline). Output plan.json {map,out,drop}.
2. Full mat photos pulled from the FYM artifact chunks mc/<n//12>.webp (last 4 bytes = uint32 LE header len; JSON header maps key -> [off,len]), saved as mx/<i>.jpg.
3. Contact sheets reviewed by eye; prop/banner/corner/watermark shots dropped unless Tiffany voted yes (keys.json = sheet order).
4. Group tile images = assets/tiles/album/<set>.png (canon_tiles.py: 0 fixes).
5. Dropped ids + vote status: dropped.json. Result 401 -> 207 items; published v19-21 (old m/*.jpg removed, mx/*.jpg added).
