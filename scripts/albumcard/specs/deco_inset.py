"""Deco card tile insets. Tiffany Nov 8 1:47pm (all three Deco albums, approved with this change): "do the 1, 2 columns and then
the tile backs" = faces-tray columns 1-2 (1-2 dots, the 1 bam crane + 2 bam, 1-2 craks, navy + gold iris flowers: more colour,
works for motif). (Was columns 3-4, Nov 8 10:11am.) Faces = Bam Bird's own faces-tray photo (listing image 16 Deco-15-2, no
variant: faces are identical on every colourway), backs = the right half of each colourway's approved FYM split
(assets/tiles/v92/bam-bird-boutique-deco-<c>-split.jpg, backs picked by variant_id Oct 25). No recolour: crop + scale only.
Output 800x1000 (card inset ratio 413x517), faces | 8px white line | backs, like the split.
Usage: python3 deco_inset.py  -> assets/tiles/album/inset/deco-<c>-flowers.jpg (file name kept so every build path stays)"""
from PIL import Image
R = '/home/claude/mahjmatchmaker-data/'
F = Image.open(R + 'assets/launches/bambird-deco-tile-set/16-faces-tray.jpg').convert('RGB').crop((118, 35, 464, 995))  # columns 1-2
H = 1000; fw = round(F.width * H / F.height); F = F.resize((fw, H), Image.LANCZOS)
for c in ('lagoon', 'mulberry', 'indigo'):
    S = Image.open(R + f'assets/tiles/v92/bam-bird-boutique-deco-{c}-split.jpg').convert('RGB')
    B = S.crop((812, 0, S.width, S.height)); B = B.resize((round(B.width * H / B.height), H), Image.LANCZOS)
    out = Image.new('RGB', (800, H), 'white'); out.paste(F, (0, 0)); out.paste(B.crop((0, 0, 800 - fw - 8, H)), (fw + 8, 0))
    out.save(R + f'assets/tiles/album/inset/deco-{c}-flowers.jpg', quality=92); print(c, fw)
