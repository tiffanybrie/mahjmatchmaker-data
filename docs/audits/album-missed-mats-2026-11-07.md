# Album missed-mats audit (Nov 7, 2026)

**Summary.** 43 live albums had **374 strong mats they never saw** (299 year-round + 75 holiday). Every live album has at least 4. The biggest year-round gaps: Heritage 10; Papaya Spritz 9; Heritage 2.0 9; Amara 8; Birdie 8; Coquette 8. Almost all of it is catalog that arrived after the album was built: Let's Be Besties (Nov 1, 347 mats), the Oct 31 Bougie / Betty June & Jeannette / Luna EK / YOLO drops, Mahj & Moon Etsy pairings, plus new partner pieces (Bam Bird Deco Dragons + Pink on Pink plaid, Britt Mills leatherettes, PLM vegan leathers, Sunday vegan leathers, Anders Ruff). 17 of the Nov 7 never-in-catalog ShopMy/Amazon mats made a list (Mahjong House Ruby Table, Rebecca Illustrated Canaries + White Sailboats, Case-Mate Ballet Pink, Amazon holiday tartans/snowflakes/Hanukkah). Papaya Spritz: 10 (Tiffany was right that it missed some, but its 50 cards already cover the obvious oranges; the misses are mostly newer patterned mats).

**How.** Per album, never-considered = mats staged Nov 7 (config/fym-shopmy-nov07.json, config/fym-amazon-holiday-oct26.json) + FYM v117 mats whose `add` tag is dated after the album was built (cutoff per album below; untagged original catalog counted as seen), minus anything already on the live album page or in its FYM match list, and minus hidden/retired/sold-out, Mahjong Studios, Paige Spearin, non-album Splash, travel/minis. Each was colour-scored against the set (measured back/signature/layer shades from config/tile-tones.json + colour-card faces, CIEDE2000, tone gate, clash penalty); top 12 year-round + top 4 holiday per album went on a contact sheet (mat full, album tiles inset), and only the ones that LOOK like a real match were kept. Motif only lifts a mat whose colours already fit (Nov 7 8:07pm). Holiday mats are listed for the holiday section only. Scripts: scripts/audits/album_missed_*_nov07.py. Sheets: assets/qa/album-missed-nov07/<album>.jpg.

**Caveats.** Album build dates are estimates (most albums pre-date the Oct 16+ catalog growth, so for them every add-tagged mat is "never seen"). Malachite: config/tile-tones.json lists its back as blush (#d0b1b9); the album photo shows dark green malachite backs, so this audit used #445344 (fix the profile in tile-tones on her OK). Mats marked non-partner are allowed in FYM (nonpartner_allow) or are her ShopMy picks: shop link only, no code. 30 other Amazon pins in her ShopMy (not the 28 holiday picks) were not in scope. Nothing was added to any album: these are candidates for her yes/no.

## Papaya Spritz: 10 strong (1 holiday)
Built ~2026-10-17 · 50 cards live · 738 mats it never saw, 89 colour-qualified · sheet `assets/qa/album-missed-nov07/papaya-spritz.jpg`

- **Fall Pop Garden** · Let's Be Besties · colour · partner (code): papaya-orange field with magenta/pink florals (the pink faces) _(#1, FYM nov01-v113)_
- **Aviary Garden** · Bougie Mahjong · colour · no partner code in FYM (allowed mat): Bougie Aviary Garden: orange inner frame + sage/lime greens (lime layer) _(#3, FYM oct31-v108)_
- **Tropicana** · Let's Be Besties · colour · partner (code): Tropicana: lime ground + orange + teal + pink, echoes back, lime layer AND faces _(#6, FYM nov01-v112)_
- **Texas Mon Amour Peach** · Fait à Main · colour · no partner code in FYM (allowed mat): Fait a Main Texas Mon Amour Peach: peach-orange with lavender paisley (lavender layer) _(#7, FYM oct26-partners)_
- **Pink Voltage** · Let's Be Besties · colour · partner (code): Pink Voltage: orange + hot pink + red stripes _(#9, FYM nov01-v113)_
- **Charlotte** · Betty June & Jeannette · colour + motif · no partner code in FYM (allowed mat): BJ&J Charlotte: blush chinoiserie with orange tigers + blue hydrangea _(#12, FYM oct20r3)_
- **Hummingbird Spring** · Let's Be Besties · colour · partner (code): butter-yellow ground (yellow back colour) with lavender florals + pink _(#4, FYM nov01-v113)_
- **Modern Abstract Watercolor** · YOLO Mahjong · colour · partner (code): YOLO coral/sage watercolor _(#5, FYM oct30-v106)_
- **Blue Rattan Premium** · Sunday Mahjong · colour · no partner code in FYM (allowed mat): Sunday Blue Rattan: orange cane with slate-blue frame (contrast) _(#10, FYM nov01-v112)_
- **Poinsettia Party** · Soirée All Day · holiday · partner (code) **[holiday]**: Soiree All Day Poinsettia Party, lime-olive centre + plum _(#14, FYM oct21-soiree)_

## Amara: 9 strong (1 holiday)
Built ~2026-10-15 · 46 cards live · 807 mats it never saw, 184 colour-qualified · sheet `assets/qa/album-missed-nov07/amara.jpg`

- **Plaid Neoprene – Pink on Pink** · Bam Bird Boutique · colour · partner (code): Bam Bird Pink on Pink plaid: the hot pink back _(#1, FYM oct30-v104)_
- **Pink Leopard** · Mahj & Moon · colour · no partner code in FYM (allowed mat): Mahj & Moon pink leopard, magenta frame _(#2, FYM oct31-v108)_
- **Pink Blooms** · Let's Be Besties · colour · partner (code): pink centre in pink/red florals _(#5, FYM oct16lbb)_
- **Pink Pizzazz** · Let's Be Besties · colour · partner (code): pink + kelly green swirl: Amara's own pink + green _(#6, FYM nov05-v115)_
- **Dusty Rose Peonies** · Let's Be Besties · colour · partner (code): pink roses, pink centre _(#7, FYM nov01-v113)_
- **Camellia Kaleidoscope** · Let's Be Besties · colour · partner (code): pink kaleidoscope with mint stripes (green faces) _(#9, FYM nov01-v113)_
- **Palm Blush** · Bougie Mahjong · colour + motif · no partner code in FYM (allowed mat): Bougie Palm Blush: pink solid, dark green border _(#4, FYM oct31-v108)_
- **Peach Petals** · Let's Be Besties · colour · partner (code): hot pink + kelly green petals, navy stripe _(#11, FYM nov01-v113)_
- **Orange and Pink Christmas** · Let's Be Besties · holiday · partner (code) **[holiday]**: pink/orange watercolor tree _(#14, FYM nov01-v113)_

## Birdie: 10 strong (2 holiday)
Built ~2026-10-15 · 33 cards live · 807 mats it never saw, 535 colour-qualified · sheet `assets/qa/album-missed-nov07/birdie.jpg`

- **Paisley Petals** · Let's Be Besties · colour · partner (code): mint + sage paisley, coral centre (pink faces) _(#1, FYM nov01-v113)_
- **Sea Glass** · Let's Be Besties · colour · partner (code): seafoam/periwinkle sea glass _(#3, FYM nov01-v113)_
- **Navy Green Sky Gator Skin Leatherette** · Let's Be Besties · colour · partner (code): mint gator with navy border (navy layer) _(#5, FYM nov01-v113)_
- **Navy Sky Mint Gator Skin** · Let's Be Besties · colour · partner (code): mint gator, navy border _(#6, FYM nov01-v113)_
- **Palm Harbor Club Tropical** · Bougie Mahjong · colour + motif · no partner code in FYM (allowed mat): pale aqua palms + dark green frame _(#4, FYM oct31-v108)_
- **Coral Lake** · Let's Be Besties · colour · partner (code): seafoam + coral reef _(#9, FYM oct16lbb)_
- **Palm Grove Links** · Bougie Mahjong · colour · no partner code in FYM (allowed mat): sage golf links, blue + pink _(#10, FYM oct31-v108)_
- **Sea of Hydrangeas** · Let's Be Besties · colour · partner (code): periwinkle hydrangeas on sage _(#11, FYM nov01-v113)_
- **Holly Jolly Gingham** · Let's Be Besties · holiday · partner (code) **[holiday]**: sky-blue gingham + green holly _(#13, FYM nov01-v113)_
- **Beachy Wreath Christmas** · Let's Be Besties · holiday · partner (code) **[holiday]**: aqua sea + pink bow wreath _(#16, FYM nov01-v113)_

## Brownstone Bloom: 9 strong (2 holiday)
Built ~2026-10-29 · 40 cards live · 630 mats it never saw, 461 colour-qualified · sheet `assets/qa/album-missed-nov07/brownstone-bloom.jpg`

- **Harriet Got Lost in the Corn Maze** · Noli June · colour + motif · partner (code): Noli June needlepoint pumpkins: cream + rust + teal, fall _(#2, FYM oct30-v106)_
- **Autumn Lace Wreath** · Piper Chase Studios · colour · no partner code in FYM (allowed mat): Piper Chase Autumn Lace Wreath: cream + brown + blush _(#4, FYM oct31-v109)_
- **Lena Took Seven Months to Needlepoint a Pillow** · Noli June · colour · partner (code): Noli June needlepoint roses on cream _(#5, FYM oct30-v106)_
- **Leopard Toile** · Piper Chase Studios · colour · no partner code in FYM (allowed mat): Piper Chase Leopard Toile: tan centre, navy + rust _(#9, FYM oct31-v109)_
- **Vino Amici** · Bougie Mahjong · colour · no partner code in FYM (allowed mat): sepia vineyard on cream _(#1, FYM oct31-v108)_
- **Cloud Crane Floral Frame** · Luna EK Studio · colour + motif · no partner code in FYM (allowed mat): cream chinoiserie tapestry with rust peonies _(#12, FYM nov03-etsy)_
- **Blossom Pavilion Waterscape** · Luna EK Studio · colour · no partner code in FYM (allowed mat): cream/blush pavilion waterscape _(#11, FYM nov03-etsy)_
- **Buffalo Plaid Snow Day** · Bougie Mahjong · holiday · no partner code in FYM (allowed mat) **[holiday]**: cream snowmen + buffalo check _(#14, FYM oct31-v108)_
- **Christmas Tree Gingham** · Amazon · holiday · non-partner, her ShopMy pick **[holiday]**: cream/red tree gingham _(#15, staged Amazon holiday pick (never in catalog))_

## Coquette: 9 strong (1 holiday)
Built ~2026-10-15 · 62 cards live · 807 mats it never saw, 258 colour-qualified · sheet `assets/qa/album-missed-nov07/coquette.jpg`

- **Lavender Scroll** · YOLO Mahjong · colour · partner (code): YOLO Lavender Scroll: mauve-lavender + blush centre _(#5, FYM oct30-v106)_
- **Peacock Flair** · Let's Be Besties · colour · partner (code): plum + lavender peacock _(#1, FYM nov01-v113)_
- **Rose Bunches** · Let's Be Besties · colour · partner (code): violet roses _(#2, FYM nov01-v113)_
- **Livy** · Betty June & Jeannette · colour · no partner code in FYM (allowed mat): BJ&J Livy: lavender + pink folk florals _(#9, FYM oct20r3)_
- **Camellia Kaleidoscope** · Let's Be Besties · colour · partner (code): pink kaleidoscope, mint _(#3, FYM nov01-v113)_
- **Watercolor Pink Blooms** · Let's Be Besties · colour · partner (code): pink watercolor blossoms _(#4, FYM nov01-v113)_
- **Mandala Peonies Burst** · Let's Be Besties · colour · partner (code): pink peonies + teal medallion _(#7, FYM nov01-v113)_
- **Summer Bloom** · Mahj & Moon · colour · no partner code in FYM (allowed mat): Mahj & Moon lavender floral _(#11, FYM oct31-v108)_
- **Pink Christmas Tree Gingham** · Amazon · holiday · non-partner, her ShopMy pick **[holiday]**: pink tree gingham _(#14, staged Amazon holiday pick (never in catalog))_

## Dandy: 9 strong (1 holiday)
Built ~2026-10-15 · 30 cards live · 807 mats it never saw, 149 colour-qualified · sheet `assets/qa/album-missed-nov07/dandy.jpg`

- **Day Dreamer (Pink and Green)** · Betty June & Jeannette · colour · no partner code in FYM (allowed mat): BJ&J Day Dreamer: hot pink + lime green, Dandy's exact pair _(#2, FYM oct31-v109)_
- **Neon Daze Queen** · Let's Be Besties · colour · partner (code): magenta mandala _(#1, FYM nov01-v113)_
- **Plaid Neoprene – Pink on Pink** · Bam Bird Boutique · colour · partner (code): Bam Bird Pink on Pink plaid _(#3, FYM oct30-v104)_
- **Hot Pink Crocodile** · YOLO Mahjong · colour · partner (code): hot pink croc _(#4, FYM oct30-v106)_
- **Pink Paris Watercolor** · Let's Be Besties · colour · partner (code): magenta frame Paris watercolor _(#7, FYM nov01-v113)_
- **Peach Petals** · Let's Be Besties · colour · partner (code): hot pink + green petals, navy stripe _(#8, FYM nov01-v113)_
- **Pink Blooms** · Let's Be Besties · colour · partner (code): pink florals _(#5, FYM oct16lbb)_
- **Flower Paper** · Let's Be Besties · colour · partner (code): magenta + olive folk tulips (olive layer) _(#9, FYM nov01-v113)_
- **Chinoiserie Christmas Tree** · Etsy · holiday · no partner code in FYM (allowed mat) **[holiday]**: pink/lime chinoiserie tree _(#14, FYM oct26-etsy)_

## Drake: 11 strong (3 holiday)
Built ~2026-10-15 · 41 cards live · 807 mats it never saw, 157 colour-qualified · sheet `assets/qa/album-missed-nov07/drake.jpg`

- **Highland Clover** · Let's Be Besties · colour · partner (code): brown + olive/green plaid frame _(#2, FYM nov01-v113)_
- **Savannah Leatherette** · Britt Mills · colour · partner (code): Britt Mills Savannah: deep green with pink _(#4, FYM oct16)_
- **Emerald Mirage Leatherette** · Britt Mills · colour · partner (code): Britt Mills Emerald Mirage _(#3, FYM oct25-audit)_
- **Olive Plaid** · Let's Be Besties · colour · partner (code): olive plaid with red fret _(#5, FYM nov01-v113)_
- **Heritage Tartan** · Anders Ruff · colour · partner (code): Anders Ruff Heritage Tartan: olive-taupe plaid _(#8, FYM oct25-audit)_
- **The Country House** · Let's Be Besties · colour · partner (code): taupe/brown plaid _(#9, FYM oct16lbb)_
- **Stella** · House of Hearts Studio · colour · no partner code in FYM (allowed mat): House of Hearts Stella: olive leaves + swans, red centre _(#1, FYM oct25-hoh)_
- **Forest Bird Bloom** · Luna EK Studio · colour · no partner code in FYM (allowed mat): Luna EK dark green botanical, tan centre _(#11, FYM nov03-etsy)_
- **Christmas Village** · Let's Be Besties · holiday · partner (code) **[holiday]**: olive Christmas village _(#13, FYM nov01-v113)_
- **Green Christmas Watercolor** · Etsy · holiday · no partner code in FYM (allowed mat) **[holiday]**: dark green holly _(#14, FYM oct26-etsy)_
- **Scandi Folk Christmas (Green)** · Etsy · holiday · no partner code in FYM (allowed mat) **[holiday]**: dark green Scandi folk _(#16, FYM oct26-etsy)_

## Emerald: 10 strong (2 holiday)
Built ~2026-10-15 · 25 cards live · 807 mats it never saw, 171 colour-qualified · sheet `assets/qa/album-missed-nov07/emerald.jpg`

- **Green Dragon Scales** · YOLO Mahjong · colour + motif · partner (code): emerald dragon scales (dragon motif) _(#1, FYM oct30-v106)_
- **Green Malachite** · Mahj Squad · colour · partner (code): Mahj Squad Green Malachite: emerald stone _(#2, FYM oct16)_
- **Botanical Jewel** · Let's Be Besties · colour · partner (code): emerald botanical _(#4, FYM nov01-v113)_
- **Bamboo Lotus** · Let's Be Besties · colour · partner (code): kelly bamboo + blue lotus _(#8, FYM nov01-v113)_
- **Tennis Club** · Let's Be Besties · colour · partner (code): kelly gingham + pink border + navy stripe (pink faces) _(#6, FYM nov01-v113)_
- **Pink and Green Open Heart** · Let's Be Besties · colour · partner (code): kelly + magenta heart _(#10, FYM nov01-v113)_
- **Emerald Lace** · Let's Be Besties · colour · partner (code): emerald + blue lace _(#12, FYM oct16lbb)_
- **Emerald Mirage Leatherette** · Britt Mills · colour · partner (code): Britt Mills Emerald Mirage _(#11, FYM oct25-audit)_
- **Festive Frost** · Let's Be Besties · holiday · partner (code) **[holiday]**: emerald frost snowflake _(#13, FYM nov01-v113)_
- **Evergreen Christmas Plaid** · YOLO Mahjong · holiday · partner (code) **[holiday]**: emerald centre in red plaid _(#14, FYM oct30-v106)_

## Gatsby: 10 strong (2 holiday)
Built ~2026-10-15 · 60 cards live · 807 mats it never saw, 173 colour-qualified · sheet `assets/qa/album-missed-nov07/gatsby.jpg`

- **Deco Dragon (Indigo)** · Bam Bird Boutique · colour + motif · partner (code): Bam Bird Deco Dragon (Indigo): art deco + dragons, made for the era _(#9, FYM oct25-audit)_
- **Azure Dolphin Cove** · Bougie Mahjong · colour + motif · no partner code in FYM (allowed mat): teal deco-fret dolphin cove _(#2, FYM oct31-v108)_
- **Blue Palms** · Let's Be Besties · colour + motif · partner (code): steel blue palms, navy centre _(#5, FYM nov01-v113)_
- **Sapphire Leaves** · Let's Be Besties · colour · partner (code): navy/steel leaves + green stripe (green layer) _(#6, FYM oct31-v108)_
- **The Mariner** · Let's Be Besties · colour · partner (code): teal/green marbled, deep green centre _(#12, FYM oct16lbb)_
- **Cobalt Garden** · Bougie Mahjong · colour · no partner code in FYM (allowed mat): cobalt garden, navy centre _(#4, FYM oct31-v108)_
- **Peacock Garden Leatherette** · Britt Mills · colour · partner (code): Britt Mills Peacock Garden: navy + olive _(#7, FYM oct27-v101)_
- **Royal Peacock** · Let's Be Besties · colour · partner (code): teal peacock _(#1, FYM nov01-v113)_
- **Alpine Snowflakes** · Let's Be Besties · holiday · partner (code) **[holiday]**: navy snowflakes + green dots _(#14, FYM nov01-v113)_
- **Emerald Night Christmas** · Let's Be Besties · holiday · partner (code) **[holiday]**: emerald night trees _(#13, FYM nov01-v113)_

## Gemma: 8 strong (1 holiday)
Built ~2026-10-22 · 19 cards live · 696 mats it never saw, 73 colour-qualified · sheet `assets/qa/album-missed-nov07/gemma.jpg`

- **Amethyst Luxe** · Bougie Mahjong · colour · no partner code in FYM (allowed mat): Bougie Amethyst Luxe: deep purple solid, gold edge _(#4, FYM oct31-v108)_
- **Peacock Flair** · Let's Be Besties · colour · partner (code): plum peacock (teal layer) _(#1, FYM nov01-v113)_
- **Rose Bunches** · Let's Be Besties · colour · partner (code): violet roses on black _(#5, FYM nov01-v113)_
- **Deco Dragon (Mulberry)** · Bam Bird Boutique · colour + motif · partner (code): Bam Bird Deco Dragon (Mulberry) _(#7, FYM oct25-audit)_
- **Hummingbird Blossoms** · Let's Be Besties · colour · partner (code): deep purple hummingbird, magenta _(#9, FYM nov01-v113)_
- **Peacock and the Lotus** · Let's Be Besties · colour · partner (code): purple frame peacock lotus _(#10, FYM nov01-v113)_
- **Lavender Flowers** · Let's Be Besties · colour · partner (code): lavender roses _(#11, FYM nov01-v113)_
- **Winter Wonderland Leatherette** · Let's Be Besties · holiday · partner (code) **[holiday]**: navy jewel snowflake _(#13, FYM nov01-v113)_

## Glitterville: 8 strong (1 holiday)
Built ~2026-10-15 · 25 cards live · 807 mats it never saw, 158 colour-qualified · sheet `assets/qa/album-missed-nov07/glitterville.jpg`

- **Pink Pizzazz** · Let's Be Besties · colour · partner (code): raspberry + green swirl (green faces) _(#1, FYM nov05-v115)_
- **Multi Hearts** · Let's Be Besties · colour · partner (code): raspberry hearts _(#2, FYM nov01-v113)_
- **Crimson & Black Paisley** · Let's Be Besties · colour · partner (code): crimson + raspberry paisley _(#3, FYM nov01-v113)_
- **Plaid Neoprene – Pink on Pink** · Bam Bird Boutique · colour · partner (code): Bam Bird Pink on Pink _(#4, FYM oct30-v104)_
- **Save the TaTas** · Let's Be Besties · colour · partner (code): magenta mandala _(#12, FYM nov01-v113)_
- **Dusty Rose Peonies** · Let's Be Besties · colour · partner (code): pink peonies _(#10, FYM nov01-v113)_
- **Flower Paper** · Let's Be Besties · colour · partner (code): raspberry folk tulips _(#5, FYM nov01-v113)_
- **Ditsy Christmas Maraschino** · Tigre de Tartan · holiday · partner (code) **[holiday]**: TdT Ditsy Christmas Maraschino _(#16, FYM oct18)_

## Glow Wild: 8 strong (2 holiday)
Built ~2026-10-15 · 41 cards live · 807 mats it never saw, 193 colour-qualified · sheet `assets/qa/album-missed-nov07/glow-wild.jpg`

- **Vegan Leather (Ruby)** · Sunday Mahjong · colour · no partner code in FYM (allowed mat): Sunday Ruby vegan leather: the oxblood back _(#2, FYM nov01-v113)_
- **The Speakeasy** · Let's Be Besties · colour + motif · partner (code): navy + red art-deco Speakeasy _(#3, FYM oct16lbb)_
- **Leopard Love** · Let's Be Besties · colour · partner (code): leopard on brown (tortoise layer) _(#7, FYM nov01-v113)_
- **Texas Mon Amour Chocolate Blue** · Fait à Main · colour · no partner code in FYM (allowed mat): Fait a Main chocolate + light blue bandana _(#10, FYM nov01-v112)_
- **Harvest Leaves** · Let's Be Besties · colour · partner (code): autumn leaves on deep green (green faces) _(#12, FYM nov01-v113)_
- **Classic Red Tartan** · YOLO Mahjong · colour · partner (code): classic red tartan _(#5, FYM oct30-v106)_
- **Christmas Red Tartan Scalloped** · Amazon · holiday · non-partner, her ShopMy pick **[holiday]**: red tartan scalloped _(#13, staged Amazon holiday pick (never in catalog))_
- **Christmas Plaid Pinecone Border** · Amazon · holiday · non-partner, her ShopMy pick **[holiday]**: oxblood plaid pinecone border _(#15, staged Amazon holiday pick (never in catalog))_

## Heritage: 11 strong (1 holiday)
Built ~2026-10-15 · 56 cards live · 807 mats it never saw, 134 colour-qualified · sheet `assets/qa/album-missed-nov07/heritage.jpg`

- **Vegan Leather (Chestnut)** · Sunday Mahjong · colour · no partner code in FYM (allowed mat): Sunday Chestnut vegan leather _(#1, FYM oct16)_
- **Tiger Print** · YOLO Mahjong · colour · partner (code): orange tiger print _(#3, FYM oct30-v106)_
- **Vegan Leather – Metallic** · Peace Love Mahjong · colour · partner (code): PLM Metallic vegan leather (tan) _(#4, FYM oct27-v101)_
- **Bird & Pear Blossom** · Mahj & Moon · colour · no partner code in FYM (allowed mat): Mahj & Moon bird & pear, terracotta _(#5, FYM oct31-v108)_
- **Giraffe Pattern** · Let's Be Besties · colour · partner (code): rust giraffe _(#7, FYM oct16lbb)_
- **Leopard Toile** · Piper Chase Studios · colour · no partner code in FYM (allowed mat): Piper Chase Leopard Toile _(#8, FYM oct31-v109)_
- **L'Été Indien Studio Print No. 1** · Fait à Main · colour · no partner code in FYM (allowed mat): Fait a Main brown check _(#9, FYM oct26-partners)_
- **Leopard Print** · YOLO Mahjong · colour · partner (code): leopard print _(#10, FYM oct30-v106)_
- **Terracotta Floral Tapestry** · Luna EK Studio · colour · no partner code in FYM (allowed mat): terracotta tapestry _(#11, FYM nov03-etsy)_
- **Cloud Crane Floral Frame** · Luna EK Studio · colour + motif · no partner code in FYM (allowed mat): tan chinoiserie tapestry _(#2, FYM nov03-etsy)_
- **Country Club Christmas** · Bougie Mahjong · holiday · no partner code in FYM (allowed mat) **[holiday]**: Country Club Christmas _(#15, FYM oct31-v108)_

## Heritage 2.0: 11 strong (2 holiday)
Built ~2026-10-15 · 77 cards live · 807 mats it never saw, 426 colour-qualified · sheet `assets/qa/album-missed-nov07/heritage-2-0.jpg`

- **Leopard Toile** · Piper Chase Studios · colour · no partner code in FYM (allowed mat): Piper Chase Leopard Toile: tan centre + rust + navy _(#2, FYM oct31-v109)_
- **Bird & Pear Blossom** · Mahj & Moon · colour · no partner code in FYM (allowed mat): Mahj & Moon bird & pear on terracotta _(#4, FYM oct31-v108)_
- **Cloud Crane Floral Frame** · Luna EK Studio · colour + motif · no partner code in FYM (allowed mat): cream chinoiserie tapestry with rust peonies _(#5, FYM nov03-etsy)_
- **Giraffe Pattern** · Let's Be Besties · colour · partner (code): rust giraffe _(#6, FYM oct16lbb)_
- **Vegan Leather – Metallic** · Peace Love Mahjong · colour · partner (code): PLM Metallic vegan leather: warm tan solid (partner) _(#7, FYM oct27-v101)_
- **Lena Took Seven Months to Needlepoint a Pillow** · Noli June · colour · partner (code): Noli June needlepoint roses _(#8, FYM oct30-v106)_
- **Fern Berry Wreath** · Luna EK Studio · colour · no partner code in FYM (allowed mat): sepia/cream fern wreath _(#10, FYM nov03-etsy)_
- **Harriet Got Lost in the Corn Maze** · Noli June · colour · partner (code): Noli June needlepoint pumpkins _(#12, FYM oct30-v106)_
- **Italian Villa** · Mahj & Moon · colour · no partner code in FYM (allowed mat): Mahj & Moon Italian Villa: terracotta + green _(#1, FYM oct31-v108)_
- **Christmas Tree Gingham** · Amazon · holiday · non-partner, her ShopMy pick **[holiday]**: cream/red tree gingham _(#14, staged Amazon holiday pick (never in catalog))_
- **Gingerbread Gingham** · Amazon · holiday · non-partner, her ShopMy pick **[holiday]**: gingerbread gingham _(#16, staged Amazon holiday pick (never in catalog))_

## Jade: 10 strong (2 holiday)
Built ~2026-10-15 · 58 cards live · 807 mats it never saw, 190 colour-qualified · sheet `assets/qa/album-missed-nov07/jade.jpg`

- **Green Dragon Scales** · YOLO Mahjong · colour + motif · partner (code): jade dragon scales (dragon motif) _(#1, FYM oct30-v106)_
- **Palm Garden Tropical** · Bougie Mahjong · colour + motif · no partner code in FYM (allowed mat): Bougie Palm Garden Tropical: jade/forest leaves on cream _(#2, FYM oct31-v108)_
- **Botanical Jewel** · Let's Be Besties · colour · partner (code): jade botanical _(#3, FYM nov01-v113)_
- **Green Bamboo Blossoms** · Let's Be Besties · colour · partner (code): sage + forest fretwork, pink blossoms (pink faces) _(#4, FYM nov01-v113)_
- **Green Malachite** · Mahj Squad · colour · partner (code): Mahj Squad Green Malachite _(#12, FYM oct16)_
- **Palm Court Tennis Club** · Bougie Mahjong · colour · no partner code in FYM (allowed mat): jade tennis club _(#8, FYM oct31-v108)_
- **Hibiscus Palm Club** · Bougie Mahjong · colour · no partner code in FYM (allowed mat): tropical leaves + coral hibiscus _(#7, FYM oct31-v108)_
- **Emerald Lace** · Let's Be Besties · colour · partner (code): green + blue lace _(#5, FYM oct16lbb)_
- **Festive Frost** · Let's Be Besties · holiday · partner (code) **[holiday]**: green frost snowflake _(#13, FYM nov01-v113)_
- **Merrywood Leatherette** · Britt Mills · holiday · partner (code) **[holiday]**: Britt Mills Merrywood _(#14, FYM oct27-v101)_

## Jasmine: 9 strong (2 holiday)
Built ~2026-10-22 · 24 cards live · 696 mats it never saw, 138 colour-qualified · sheet `assets/qa/album-missed-nov07/jasmine.jpg`

- **Botanical Jewel** · Let's Be Besties · colour · partner (code): jade botanical _(#1, FYM nov01-v113)_
- **Green Dragon Scales** · YOLO Mahjong · colour + motif · partner (code): jade dragon scales _(#2, FYM oct30-v106)_
- **Hibiscus Palm Club** · Bougie Mahjong · colour + motif · no partner code in FYM (allowed mat): tropical palms + pink hibiscus (palm faces) _(#4, FYM oct31-v108)_
- **Bamboo Lotus** · Let's Be Besties · colour · partner (code): kelly bamboo + blue lotus (blue layer) _(#5, FYM nov01-v113)_
- **Palm Garden Tropical** · Bougie Mahjong · colour + motif · no partner code in FYM (allowed mat): Bougie Palm Garden Tropical _(#9, FYM oct31-v108)_
- **Plaid Neoprene – Green with Pink** · Bam Bird Boutique · colour · partner (code): Bam Bird green plaid with pink _(#10, FYM oct30-v104)_
- **Nantucket Floral** · Let's Be Besties · colour · partner (code): mint stripe + pink florals _(#11, FYM nov01-v113)_
- **Festive Frost** · Let's Be Besties · holiday · partner (code) **[holiday]**: green frost _(#13, FYM nov01-v113)_
- **Plaid Tidings** · My Fair Mahjong · holiday · partner (code) **[holiday]**: Plaid Tidings, jade centre _(#14, FYM oct25-audit)_

## La Fete: 10 strong (2 holiday)
Built ~2026-10-15 · 31 cards live · 807 mats it never saw, 373 colour-qualified · sheet `assets/qa/album-missed-nov07/la-fete.jpg`

- **Mandala Peonies Burst** · Let's Be Besties · colour · partner (code): pink peonies + teal medallion (teal layer) _(#1, FYM nov01-v113)_
- **Mia Leatherette** · Britt Mills · colour · partner (code): Britt Mills Mia: blush + navy cheetah _(#2, FYM oct27-v101)_
- **Paris Conservatory** · Bougie Mahjong · colour · no partner code in FYM (allowed mat): Bougie Paris Conservatory: pink + navy _(#3, FYM oct31-v108)_
- **Palm Blush** · Bougie Mahjong · colour + motif · no partner code in FYM (allowed mat): Bougie Palm Blush: pink + teal border _(#5, FYM oct31-v108)_
- **Elizabeth** · Betty June & Jeannette · colour · no partner code in FYM (allowed mat): BJ&J Elizabeth pink _(#6, FYM oct20r3)_
- **Dusty Rose Peonies** · Let's Be Besties · colour · partner (code): pink roses _(#9, FYM nov01-v113)_
- **Watercolor Pink Blooms** · Let's Be Besties · colour · partner (code): pink watercolor blossoms _(#12, FYM nov01-v113)_
- **Canaries** · Rebecca Illustrated · colour · non-partner, her ShopMy pick: Rebecca Illustrated Canaries: pink + mint + yellow _(#10, staged ShopMy (never in catalog))_
- **Pink Christmas Tree Gingham** · Amazon · holiday · non-partner, her ShopMy pick **[holiday]**: pink tree gingham _(#16, staged Amazon holiday pick (never in catalog))_
- **Poinsettia Ornament** · Piper Chase Studios · holiday · no partner code in FYM (allowed mat) **[holiday]**: Piper Chase Poinsettia Ornament _(#15, FYM oct31-v109)_

## Lagoon: 6 strong (1 holiday)
Built ~2026-10-15 · 42 cards live · 807 mats it never saw, 290 colour-qualified · sheet `assets/qa/album-missed-nov07/lagoon.jpg`

- **Deco Dragon (Lagoon)** · Bam Bird Boutique · colour + motif · partner (code): teal Deco Dragon made for Lagoon (Bam Bird partner): same teal, dragon motif _(#2, FYM oct25-audit)_
- **Teal Dots and Stripes with Instructions** · Let's Be Besties · colour · partner (code): teal field, rainbow stripe border echoes the striped layers _(#1, FYM nov01-v113)_
- **Ocean Jewel** · Let's Be Besties · colour · partner (code): teal-blue kaleidoscope with green + berry red accents _(#4, FYM nov01-v113)_
- **Folk Garden** · Let's Be Besties · colour · partner (code): teal ground, pink/orange folk florals echo the berry faces _(#5, FYM nov01-v113)_
- **Vibrant Symphony** · House of Hearts Studio · colour · no partner code in FYM (allowed mat): teal ground, red florals (brand photo has a small 'VIBI' banner) _(#8, FYM oct25-hoh)_
- **Winter Jewel** · Let's Be Besties · holiday · partner (code) **[holiday]**: teal snowflake medallion _(#13, FYM oct16lbb)_

## Lilac Soiree (retired): 8 strong (1 holiday)
Built ~2026-10-21 · 9 cards live · 696 mats it never saw, 128 colour-qualified · sheet `assets/qa/album-missed-nov07/lilac-soiree.jpg`

- **Deep Blue Floral with Instructions** · Let's Be Besties · colour · partner (code): cobalt-violet blue on white, same blue as the backs _(#1, FYM nov01-v113)_
- **Watercolor Lilies** · Let's Be Besties · colour · partner (code): lavender lotus on blue water _(#2, FYM nov01-v113)_
- **Plum Lotus** · Let's Be Besties · colour · partner (code): slate-violet with pink lotus _(#3, FYM nov01-v113)_
- **Blooming Lotus** · Let's Be Besties · colour + motif · partner (code): periwinkle field, lotus motif _(#5, FYM nov01-v113)_
- **Acrylic Flowers** · Let's Be Besties · colour · partner (code): periwinkle frame, pink/violet florals echo the faces _(#9, FYM nov01-v113)_
- **Hummingbird Blossoms** · Let's Be Besties · colour · partner (code): purple + pink hummingbirds _(#8, FYM nov01-v113)_
- **Silk Dragon** · Bougie Mahjong · colour + motif · no partner code in FYM (allowed mat): navy/periwinkle with pink dragons (motif: chinoiserie) _(#4, FYM oct31-v108)_
- **Hanukkah Menorah & Peacocks** · Amazon · holiday · non-partner, her ShopMy pick **[holiday]**: Hanukkah: blue + lavender peacock menorah _(#13, staged Amazon holiday pick (never in catalog))_

## Limoncello: 8 strong (2 holiday)
Built ~2026-10-22 · 21 cards live · 696 mats it never saw, 152 colour-qualified · sheet `assets/qa/album-missed-nov07/limoncello.jpg`

- **Martini Shaken** · Let's Be Besties · colour + motif · partner (code): olive-lime field, olive motif _(#1, FYM nov01-v113)_
- **Palm Court** · Let's Be Besties · colour + motif · partner (code): lime fret + palms on pink (pink faces) _(#2, FYM nov01-v113)_
- **Retro Palm Burst** · Let's Be Besties · colour · partner (code): lime/green/mint geometric _(#3, FYM nov01-v113)_
- **Limoncello** · Bougie Mahjong · colour + motif · no partner code in FYM (allowed mat): the Limoncello mat: lemons with olive + yellow stripe (name + motif) _(#7, FYM oct31-v108)_
- **Monogram Floral Fret** · Piper Chase Studios · colour · no partner code in FYM (allowed mat): olive-lime floral with pink roses _(#11, FYM oct31-v109)_
- **Palm Court Tennis Club** · Bougie Mahjong · colour · no partner code in FYM (allowed mat): green tennis-club scene, lime accents _(#4, FYM oct31-v108)_
- **Garland Christmas** · Let's Be Besties · holiday · partner (code) **[holiday]**: lime-green garland _(#13, FYM nov01-v113)_
- **Holly Coastal Christmas** · Let's Be Besties · holiday · partner (code) **[holiday]**: pale lime holly _(#14, FYM nov01-v113)_

## Lola: 10 strong (2 holiday)
Built ~2026-10-15 · 30 cards live · 807 mats it never saw, 336 colour-qualified · sheet `assets/qa/album-missed-nov07/lola.jpg`

- **Vegan Leather – Slate Blue** · Peace Love Mahjong · colour · partner (code): PLM Slate Blue vegan leather (partner): soft blue solid _(#1, FYM oct27-v101)_
- **Blue Willow Chinoiserie** · Let's Be Besties · colour + motif · partner (code): blue-and-white chinoiserie, same blues _(#2, FYM nov01-v113)_
- **Hydrangea** · Royal Mahjong Society · colour · partner (code): RMS Hydrangea: periwinkle lattice + blue stripes _(#3, FYM oct16)_
- **Porcelain Crane Garden** · Bougie Mahjong · colour · no partner code in FYM (allowed mat): cobalt porcelain toile _(#4, FYM oct31-v108)_
- **Blue Hamsa** · Let's Be Besties · colour · partner (code): light + cobalt blue hamsa _(#5, FYM nov01-v113)_
- **Blue Bamboo** · Let's Be Besties · colour · partner (code): light blue bamboo with pink blossoms _(#7, FYM nov01-v113)_
- **Blue Chinoiserie Village** · YOLO Mahjong · colour + motif · partner (code): blue-and-white chinoiserie village _(#9, FYM oct30-v106)_
- **Deep Blue Floral with Instructions** · Let's Be Besties · colour · partner (code): cobalt watercolor damask _(#11, FYM nov01-v113)_
- **Blue & White Snowflake** · Amazon · holiday · non-partner, her ShopMy pick **[holiday]**: blue + white snowflakes _(#14, staged Amazon holiday pick (never in catalog))_
- **Flaming Dreidels** · Let's Be Besties · holiday · partner (code) **[holiday]**: Hanukkah: blue dreidels _(#13, FYM nov01-v113)_

## Luminaire: 10 strong (3 holiday)
Built ~2026-10-15 · 21 cards live · 807 mats it never saw, 467 colour-qualified · sheet `assets/qa/album-missed-nov07/luminaire.jpg`

- **Gigi (Canvas Art)** · Betty June & Jeannette · colour · no partner code in FYM (allowed mat): pastel pink/lavender/blue canvas art (BJ&J Gigi), the tile's exact stripes _(#2, FYM oct26-etsy)_
- **Bam Bird Toile Pink** · Let's Be Besties · colour · partner (code): soft pink toile _(#7, FYM nov01-v113)_
- **Pink Hummingbird** · AussieHannaGift · colour · no partner code in FYM (allowed mat): soft pink hummingbird _(#5, FYM nov03-etsy)_
- **Scalloped Bow Garden** · Mahj & Moon · colour · no partner code in FYM (allowed mat): pink bows + aqua scallop _(#12, FYM oct31-v108)_
- **Canaries** · Rebecca Illustrated · colour · non-partner, her ShopMy pick: Rebecca Illustrated Canaries: pink + lavender + mint _(#10, staged ShopMy (never in catalog))_
- **Watercolor Pink Blooms** · Let's Be Besties · colour · partner (code): watercolor pink blooms _(#4, FYM nov01-v113)_
- **Flutter for a Cause** · Let's Be Besties · colour · partner (code): pink butterfly floral _(#1, FYM nov01-v113)_
- **Nutcracker Leatherette** · Britt Mills · holiday · partner (code) **[holiday]**: Britt Mills Nutcracker, pink + periwinkle centre _(#14, FYM oct16)_
- **Pink Christmas Tree Gingham** · Amazon · holiday · non-partner, her ShopMy pick **[holiday]**: pink Christmas-tree gingham _(#13, staged Amazon holiday pick (never in catalog))_
- **Ornament Plaid** · Piper Chase Studios · holiday · no partner code in FYM (allowed mat) **[holiday]**: pastel ornament plaid _(#16, FYM oct31-v109)_

## Malachite: 10 strong (3 holiday)
Built ~2026-10-20 · 51 cards live · 702 mats it never saw, 194 colour-qualified · sheet `assets/qa/album-missed-nov07/malachite.jpg`

- **Crimson Harvest Leatherette** · Britt Mills · colour · partner (code): Britt Mills Crimson Harvest: deep green + pink/red (the faces) _(#1, FYM oct27-v101)_
- **Plaid Neoprene – Green with Pink** · Bam Bird Boutique · colour · partner (code): Bam Bird green plaid with pink _(#3, FYM oct30-v104)_
- **Green Dragon Scales** · YOLO Mahjong · colour + motif · partner (code): green dragon scales (dragon motif) _(#4, FYM oct30-v106)_
- **Botanical Jewel** · Let's Be Besties · colour · partner (code): deep green botanical, plum flowers _(#6, FYM nov01-v113)_
- **Emerald Mirage Leatherette** · Britt Mills · colour · partner (code): Britt Mills Emerald Mirage: deep green jungle _(#12, FYM oct25-audit)_
- **Olive Plaid** · Let's Be Besties · colour · partner (code): dark olive plaid + red fret border (red layer) _(#8, FYM nov01-v113)_
- **Emerald Society** · Bougie Mahjong · colour · no partner code in FYM (allowed mat): deep emerald solid _(#5, FYM oct31-v108)_
- **Plaid Tidings** · My Fair Mahjong · holiday · partner (code) **[holiday]**: My Fair Mahjong Plaid Tidings _(#13, FYM oct25-audit)_
- **Merrywood Leatherette** · Britt Mills · holiday · partner (code) **[holiday]**: Britt Mills Merrywood (sage centre, red corners) _(#14, FYM oct27-v101)_
- **Green Christmas Watercolor** · Etsy · holiday · no partner code in FYM (allowed mat) **[holiday]**: dark green holly _(#16, FYM oct26-etsy)_

## Moonlight: 10 strong (2 holiday)
Built ~2026-10-15 · 42 cards live · 807 mats it never saw, 182 colour-qualified · sheet `assets/qa/album-missed-nov07/moonlight.jpg`

- **Blue Willow Chinoiserie** · Let's Be Besties · colour + motif · partner (code): blue-and-white chinoiserie _(#2, FYM nov01-v113)_
- **Blooming Lotus** · Let's Be Besties · colour · partner (code): cornflower field, lotus _(#5, FYM nov01-v113)_
- **Blue Hamsa** · Let's Be Besties · colour · partner (code): light + cobalt blue hamsa _(#8, FYM nov01-v113)_
- **Deep Blue Floral with Instructions** · Let's Be Besties · colour · partner (code): cobalt watercolor damask _(#9, FYM nov01-v113)_
- **Porcelain Crane Garden** · Bougie Mahjong · colour · no partner code in FYM (allowed mat): cobalt porcelain toile _(#10, FYM oct31-v108)_
- **Blue Bamboo** · Let's Be Besties · colour · partner (code): light blue bamboo, pink blossoms _(#11, FYM nov01-v113)_
- **Sea Glass** · Let's Be Besties · colour · partner (code): periwinkle/teal sea glass _(#1, FYM nov01-v113)_
- **Watercolor Lilies** · Let's Be Besties · colour · partner (code): blue water lilies _(#12, FYM nov01-v113)_
- **Blue & White Snowflake** · Amazon · holiday · non-partner, her ShopMy pick **[holiday]**: blue + white snowflakes _(#13, staged Amazon holiday pick (never in catalog))_
- **Flaming Dreidels** · Let's Be Besties · holiday · partner (code) **[holiday]**: Hanukkah: blue dreidels _(#15, FYM nov01-v113)_

## Nantucket: 9 strong (5 holiday)
Built ~2026-10-22 · 40 cards live · 696 mats it never saw, 65 colour-qualified · sheet `assets/qa/album-missed-nov07/nantucket.jpg`

- **Classic Red Tartan** · YOLO Mahjong · colour · partner (code): classic red tartan with green stripe, echoes the green-white layers _(#3, FYM oct30-v106)_
- **Ruby Table Double-Sided** · The Mahjong House · colour · non-partner, her ShopMy pick: Mahjong House Ruby Table: solid red _(#6, staged ShopMy (never in catalog))_
- **Vegan Leather (Ruby)** · Sunday Mahjong · colour · no partner code in FYM (allowed mat): Sunday Ruby vegan leather: deep red solid _(#11, FYM nov01-v113)_
- **Checkerboard with Instructions** · Let's Be Besties · colour · partner (code): deep red with instructions _(#4, FYM nov01-v113)_
- **Cheaper Than Christmas Tiles** · Let's Be Besties · holiday · partner (code) **[holiday]**: red + green stripe border, painted mahjong tiles _(#2, FYM nov01-v113)_
- **Red Tartan Scalloped (Lewtemi)** · Amazon · holiday · non-partner, her ShopMy pick **[holiday]**: red tartan scalloped _(#15, staged Amazon holiday pick (never in catalog))_
- **Holly Starburst** · Let's Be Besties · holiday · partner (code) **[holiday]**: red + green starburst _(#13, FYM nov01-v113)_
- **Ho Ho Ho! Christmas** · Let's Be Besties · holiday · partner (code) **[holiday]**: red/green plaid Ho Ho Ho _(#14, FYM nov01-v113)_
- **Red Snowflake** · Amazon · holiday · non-partner, her ShopMy pick **[holiday]**: red snowflake _(#16, staged Amazon holiday pick (never in catalog))_

## Osler: 9 strong (2 holiday)
Built ~2026-10-22 · 38 cards live · 696 mats it never saw, 236 colour-qualified · sheet `assets/qa/album-missed-nov07/osler.jpg`

- **Vegan Leather – Slate Blue** · Peace Love Mahjong · colour · partner (code): PLM Slate Blue vegan leather: the pale blue back _(#1, FYM oct27-v101)_
- **Floral Scrolls** · Let's Be Besties · colour · partner (code): light blue scrolls with red accents (echoes red layers) _(#7, FYM nov01-v113)_
- **White Sailboats** · Rebecca Illustrated · colour + motif · non-partner, her ShopMy pick: Rebecca Illustrated White Sailboats: pale blue, nautical _(#12, staged ShopMy (never in catalog))_
- **Azure Harbor Regatta** · Bougie Mahjong · colour + motif · no partner code in FYM (allowed mat): nautical regatta, light blue _(#8, FYM oct31-v108)_
- **Blue Bamboo** · Let's Be Besties · colour · partner (code): light blue bamboo _(#3, FYM nov01-v113)_
- **Porcelain Crane Garden** · Bougie Mahjong · colour · no partner code in FYM (allowed mat): cobalt porcelain toile _(#2, FYM oct31-v108)_
- **Blue Willow Chinoiserie** · Let's Be Besties · colour + motif · partner (code): blue-and-white chinoiserie _(#5, FYM nov01-v113)_
- **Blue & White Snowflake** · Amazon · holiday · non-partner, her ShopMy pick **[holiday]**: blue + white snowflakes _(#15, staged Amazon holiday pick (never in catalog))_
- **Whoosh** · Let's Be Besties · holiday · partner (code) **[holiday]**: navy ski map _(#14, FYM nov01-v113)_

## Palm Royale: 9 strong (2 holiday)
Built ~2026-10-15 · 25 cards live · 807 mats it never saw, 465 colour-qualified · sheet `assets/qa/album-missed-nov07/palm-royale.jpg`

- **Palm Court Tennis Club** · Bougie Mahjong · colour + motif · no partner code in FYM (allowed mat): green palm tennis club (palm motif) _(#3, FYM oct31-v108)_
- **Palm Garden Tropical** · Bougie Mahjong · colour + motif · no partner code in FYM (allowed mat): palm-leaf tropical frame _(#5, FYM oct31-v108)_
- **Southern Stained Glass** · Let's Be Besties · colour · partner (code): sage stained glass, pink magnolia echoes faces _(#4, FYM oct16lbb)_
- **Green Pickleball** · YOLO Mahjong · colour · partner (code): sage + pink pickleball _(#10, FYM oct30-v106)_
- **Canine Garden Party** · Bougie Mahjong · colour · no partner code in FYM (allowed mat): sage/tan garden scene _(#2, FYM oct31-v108)_
- **Lotus Garden Frame** · Luna EK Studio · colour + motif · no partner code in FYM (allowed mat): sage chinoiserie lotus garden _(#1, FYM nov03-etsy)_
- **Martini Shaken** · Let's Be Besties · colour · partner (code): olive martini _(#8, FYM nov01-v113)_
- **Winter Christmas Trees Stripe** · Amazon · holiday · non-partner, her ShopMy pick **[holiday]**: sage stripe Christmas trees _(#13, staged Amazon holiday pick (never in catalog))_
- **Cardinal Evergreen Wreath** · Amazon · holiday · non-partner, her ShopMy pick **[holiday]**: cardinal evergreen wreath on cream _(#16, staged Amazon holiday pick (never in catalog))_

## Pearlescent: 5 strong (1 holiday)
Built ~2026-10-15 · 37 cards live · 807 mats it never saw, 602 colour-qualified · sheet `assets/qa/album-missed-nov07/pearlescent.jpg`

- **Novella Leatherette** · Britt Mills · colour · partner (code): Britt Mills Novella: blush + green _(#4, FYM oct16)_
- **Jean Always Chose Cranberry From a Can** · Noli June · colour · partner (code): Noli June ivory with rose florals _(#6, FYM oct30-v106)_
- **The Veranda - Bamboo Neutral with Rattan Fringe** · Tala Mahj · colour · no partner code in FYM (allowed mat): Tala Veranda bamboo neutral (check Tala allow list) _(#7, FYM oct20r3)_
- **Crimson Crane** · Let's Be Besties · colour · partner (code): pale aqua/blush crane _(#9, FYM nov01-v113)_
- **Scandi Folk Christmas (Cream)** · Etsy · holiday · no partner code in FYM (allowed mat) **[holiday]**: cream Scandi folk _(#15, FYM oct26-etsy)_

## Pippa: 4 strong (0 holiday)
Built ~2026-10-22 · 27 cards live · 696 mats it never saw, 54 colour-qualified · sheet `assets/qa/album-missed-nov07/pippa.jpg`

- **Limoncello** · Bougie Mahjong · colour + motif · no partner code in FYM (allowed mat): Limoncello: yellow stripes + lemons _(#1, FYM oct31-v108)_
- **Walking on Sunshine** · Let's Be Besties · colour · partner (code): saturated yellow with rainbow folk florals _(#2, FYM nov01-v113)_
- **Yellow and Bird Bam** · Wren Mats · colour · partner (code): Wren Yellow and Bird Bam: yellow + cobalt _(#11, FYM oct25-audit)_
- **Golden Hour Ripple** · YOLO Mahjong · colour · partner (code): butter/gold ripple _(#8, FYM oct30-v106)_

## Preppy Soiree (retired): 8 strong (2 holiday)
Built ~2026-10-21 · 14 cards live · 696 mats it never saw, 185 colour-qualified · sheet `assets/qa/album-missed-nov07/preppy-soiree.jpg`

- **Plum Lotus** · Let's Be Besties · colour · partner (code): slate-violet with lavender lotus (faces) _(#1, FYM nov01-v113)_
- **Blue Palms** · Let's Be Besties · colour + motif · partner (code): dusty blue palms _(#2, FYM nov01-v113)_
- **Sapphire Leaves** · Let's Be Besties · colour · partner (code): dusty blue leaves _(#3, FYM oct31-v108)_
- **Sage Mosaic** · Let's Be Besties · colour · partner (code): navy + lavender mosaic _(#4, FYM nov01-v113)_
- **The Blues** · Wren Mats · colour · partner (code): Wren The Blues: slate blue-grey solid _(#12, FYM oct25-audit)_
- **Cobalt Garden** · Bougie Mahjong · colour · no partner code in FYM (allowed mat): cobalt garden _(#8, FYM oct31-v108)_
- **Blue & White Snowflake** · Amazon · holiday · non-partner, her ShopMy pick **[holiday]**: blue + white snowflakes _(#14, staged Amazon holiday pick (never in catalog))_
- **Flaming Dreidels** · Let's Be Besties · holiday · partner (code) **[holiday]**: Hanukkah: blue dreidels _(#13, FYM nov01-v113)_

## Seabreeze: 9 strong (2 holiday)
Built ~2026-10-15 · 30 cards live · 807 mats it never saw, 305 colour-qualified · sheet `assets/qa/album-missed-nov07/seabreeze.jpg`

- **Hibiscus Lagoon** · Bougie Mahjong · colour + motif · no partner code in FYM (allowed mat): turquoise palms + pink centre _(#1, FYM oct31-v108)_
- **Peacock Lagoon** · Let's Be Besties · colour · partner (code): aqua peacock _(#2, FYM nov01-v113)_
- **Electric Hibiscus** · Bougie Mahjong · colour · no partner code in FYM (allowed mat): turquoise + hot pink hibiscus, navy frame _(#3, FYM oct31-v108)_
- **James (Pastel Floral)** · Betty June & Jeannette · colour · no partner code in FYM (allowed mat): BJ&J James: aqua + pink _(#4, FYM oct31-v109)_
- **Aloha** · Let's Be Besties · colour · partner (code): aqua tropical, pink _(#11, FYM nov01-v113)_
- **Paisley Petals** · Let's Be Besties · colour · partner (code): mint paisley + coral _(#7, FYM nov01-v113)_
- **Teal Marble with Gold Splash** · Let's Be Besties · colour · partner (code): teal marble with gold _(#8, FYM nov01-v113)_
- **Winter Jewel** · Let's Be Besties · holiday · partner (code) **[holiday]**: teal snowflake medallion _(#16, FYM oct16lbb)_
- **Winter Berry Evergreen** · Amazon · holiday · non-partner, her ShopMy pick **[holiday]**: pale aqua winter berry _(#13, staged Amazon holiday pick (never in catalog))_

## Shangri-la (retired): 10 strong (3 holiday)
Built ~2026-10-21 · 16 cards live · 696 mats it never saw, 149 colour-qualified · sheet `assets/qa/album-missed-nov07/shangri-la.jpg`

- **Plaid Neoprene – Green with Pink** · Bam Bird Boutique · colour · partner (code): Bam Bird green plaid with pink: emerald + pink faces _(#1, FYM oct30-v104)_
- **Emerald Society** · Bougie Mahjong · colour · no partner code in FYM (allowed mat): emerald solid _(#2, FYM oct31-v108)_
- **Botanical Jewel** · Let's Be Besties · colour · partner (code): emerald botanical _(#4, FYM nov01-v113)_
- **Green Dragon Scales** · YOLO Mahjong · colour + motif · partner (code): green dragon scales (dragon motif) _(#5, FYM oct30-v106)_
- **Emerald Mirage Leatherette** · Britt Mills · colour · partner (code): Britt Mills Emerald Mirage _(#7, FYM oct25-audit)_
- **Plaid Neoprene – Green and Blue** · Bam Bird Boutique · colour · partner (code): Bam Bird green + navy plaid (navy layer) _(#11, FYM oct30-v104)_
- **Crimson Harvest Leatherette** · Britt Mills · colour · partner (code): Britt Mills Crimson Harvest: deep green + pink _(#9, FYM oct27-v101)_
- **Emerald Night Christmas** · Let's Be Besties · holiday · partner (code) **[holiday]**: emerald trees _(#13, FYM nov01-v113)_
- **Plaid Tidings** · My Fair Mahjong · holiday · partner (code) **[holiday]**: My Fair Mahjong Plaid Tidings (emerald centre) _(#14, FYM oct25-audit)_
- **Green Christmas Watercolor** · Etsy · holiday · no partner code in FYM (allowed mat) **[holiday]**: green holly _(#15, FYM oct26-etsy)_

## Sierra: 9 strong (1 holiday)
Built ~2026-10-15 · 18 cards live · 807 mats it never saw, 117 colour-qualified · sheet `assets/qa/album-missed-nov07/sierra.jpg`

- **Terracotta Floral Tapestry** · Luna EK Studio · colour · no partner code in FYM (allowed mat): terracotta tapestry _(#1, FYM nov03-etsy)_
- **Tiger Print** · YOLO Mahjong · colour · partner (code): orange tiger print _(#4, FYM oct30-v106)_
- **Tabitha** · House of Hearts Studio · colour · no partner code in FYM (allowed mat): cane + autumn leaves (House of Hearts) _(#7, FYM oct25-hoh)_
- **Vegan Leather (Chestnut)** · Sunday Mahjong · colour · no partner code in FYM (allowed mat): Sunday Chestnut vegan leather _(#11, FYM oct16)_
- **Blue Rattan Premium** · Sunday Mahjong · colour · no partner code in FYM (allowed mat): Sunday Blue Rattan: orange cane, blue frame _(#12, FYM nov01-v112)_
- **L'Été Indien Studio Print No. 1** · Fait à Main · colour · no partner code in FYM (allowed mat): Fait a Main brown/pink check _(#6, FYM oct26-partners)_
- **Giraffe Pattern** · Let's Be Besties · colour · partner (code): rust giraffe _(#2, FYM oct16lbb)_
- **Leopard Print** · YOLO Mahjong · colour · partner (code): leopard _(#9, FYM oct30-v106)_
- **Country Club Christmas** · Bougie Mahjong · holiday · no partner code in FYM (allowed mat) **[holiday]**: Country Club Christmas _(#13, FYM oct31-v108)_

## Smith: 6 strong (1 holiday)
Built ~2026-10-15 · 39 cards live · 807 mats it never saw, 123 colour-qualified · sheet `assets/qa/album-missed-nov07/smith.jpg`

- **Terracotta Floral Tapestry** · Luna EK Studio · colour · no partner code in FYM (allowed mat): terracotta tapestry _(#2, FYM nov03-etsy)_
- **Vegan Leather (Chestnut)** · Sunday Mahjong · colour · no partner code in FYM (allowed mat): Sunday Chestnut vegan leather _(#5, FYM oct16)_
- **Retro Riviera** · Let's Be Besties · colour · partner (code): navy/red/brown/cream swirl echoes the striped layers _(#9, FYM oct30-v104)_
- **L'Été Indien Studio Print No. 1** · Fait à Main · colour · no partner code in FYM (allowed mat): Fait a Main brown check _(#3, FYM oct26-partners)_
- **Cranberry Tapestry** · Let's Be Besties · colour · partner (code): cranberry/navy tapestry _(#12, FYM nov01-v113)_
- **Red Tartan Scalloped (Lewtemi)** · Amazon · holiday · non-partner, her ShopMy pick **[holiday]**: red tartan scalloped _(#16, staged Amazon holiday pick (never in catalog))_

## Solara: 8 strong (1 holiday)
Built ~2026-10-15 · 40 cards live · 807 mats it never saw, 218 colour-qualified · sheet `assets/qa/album-missed-nov07/solara.jpg`

- **Palm Blush** · Bougie Mahjong · colour · no partner code in FYM (allowed mat): coral solid with deep green border (green faces) _(#1, FYM oct31-v108)_
- **Kiki** · Betty June & Jeannette · colour · no partner code in FYM (allowed mat): BJ&J Kiki coral floral _(#2, FYM oct31-v109)_
- **Mandala Peonies Burst** · Let's Be Besties · colour · partner (code): coral peonies + teal medallion _(#9, FYM nov01-v113)_
- **Bellamy Bloom** · Anders Ruff · colour · partner (code): Anders Ruff Bellamy Bloom: coral centre _(#12, FYM oct25-audit)_
- **Lauren (Pink Ladybug)** · Betty June & Jeannette · colour · no partner code in FYM (allowed mat): BJ&J Lauren coral/pink floral _(#5, FYM oct31-v109)_
- **Cheeky Cockatoo** · Sophie Clima · colour · no partner code in FYM (allowed mat): Sophie Clima cockatoo, coral/orange _(#7, FYM oct20r3)_
- **Betty (Floral Monogram Game Surface)** · Betty June & Jeannette · colour · no partner code in FYM (allowed mat): BJ&J Betty pink floral _(#11, FYM oct20r3)_
- **Ditsy Christmas Maraschino** · Tigre de Tartan · holiday · partner (code) **[holiday]**: TdT Ditsy Christmas Maraschino, coral-red _(#13, FYM oct18)_

## Sorbet: 8 strong (2 holiday)
Built ~2026-10-22 · 25 cards live · 696 mats it never saw, 285 colour-qualified · sheet `assets/qa/album-missed-nov07/sorbet.jpg`

- **Golden Hour Ripple** · YOLO Mahjong · colour · partner (code): butter yellow ripple _(#2, FYM oct30-v106)_
- **Yellow and Bird Bam** · Wren Mats · colour · partner (code): Wren Yellow and Bird Bam _(#3, FYM oct25-audit)_
- **Limoncello** · Bougie Mahjong · colour + motif · no partner code in FYM (allowed mat): Limoncello lemons _(#6, FYM oct31-v108)_
- **Lemon Print** · Betty June & Jeannette · colour · no partner code in FYM (allowed mat): BJ&J Lemon Print: sage + pink + lemon _(#9, FYM oct31-v109)_
- **Koi Swimming** · Let's Be Besties · colour · partner (code): mint + coral koi _(#7, FYM nov01-v113)_
- **Walking on Sunshine** · Let's Be Besties · colour · partner (code): yellow folk florals _(#12, FYM nov01-v113)_
- **Holy Night** · Betty June & Jeannette · holiday · no partner code in FYM (allowed mat) **[holiday]**: pastel nativity _(#13, FYM oct31-v109)_
- **Oh Little Town** · Betty June & Jeannette · holiday · no partner code in FYM (allowed mat) **[holiday]**: pastel nativity Oh Little Town _(#15, FYM oct31-v109)_

## Spring Love (retired): 7 strong (1 holiday)
Built ~2026-10-21 · 18 cards live · 696 mats it never saw, 161 colour-qualified · sheet `assets/qa/album-missed-nov07/spring-love.jpg`

- **Plaid Neoprene – Pink on Pink** · Bam Bird Boutique · colour · partner (code): Bam Bird Pink on Pink plaid _(#1, FYM oct30-v104)_
- **Pink Leopard** · Mahj & Moon · colour · no partner code in FYM (allowed mat): Mahj & Moon pink leopard _(#4, FYM oct31-v108)_
- **Hot Pink Crocodile** · YOLO Mahjong · colour · partner (code): hot pink croc _(#6, FYM oct30-v106)_
- **Day Dreamer (Pink and Green)** · Betty June & Jeannette · colour · no partner code in FYM (allowed mat): BJ&J Day Dreamer pink + green _(#10, FYM oct31-v109)_
- **Tropical Palm Beach** · YOLO Mahjong · colour · partner (code): pink centre tropical _(#11, FYM oct30-v106)_
- **Peach Petals** · Let's Be Besties · colour · partner (code): pink petals _(#9, FYM nov01-v113)_
- **Peppermint Wishes** · My Fair Mahjong · holiday · partner (code) **[holiday]**: My Fair Mahjong Peppermint Wishes _(#14, FYM oct25-audit)_

## Sunday Tile Set: 9 strong (2 holiday)
Built ~2026-10-29 · 36 cards live · 630 mats it never saw, 79 colour-qualified · sheet `assets/qa/album-missed-nov07/sunday-tile-set.jpg`

- **Cloud Crane Floral Frame** · Luna EK Studio · colour + motif · no partner code in FYM (allowed mat): tan chinoiserie tapestry _(#1, FYM nov03-etsy)_
- **Tiger Stripes** · Let's Be Besties · colour · partner (code): ochre tiger stripes _(#4, FYM nov05-v115)_
- **Butterscotch Floral** · Let's Be Besties · colour · partner (code): olive/ochre frame floral _(#7, FYM nov01-v112)_
- **Grand Prix Estate** · Bougie Mahjong · colour · no partner code in FYM (allowed mat): olive equestrian _(#9, FYM oct31-v108)_
- **Happy Camper** · Bougie Mahjong · colour · no partner code in FYM (allowed mat): olive camp scene _(#12, FYM oct31-v108)_
- **Bird & Pear Blossom** · Mahj & Moon · colour · no partner code in FYM (allowed mat): Mahj & Moon tan bird & pear _(#3, FYM oct31-v108)_
- **Vino Amici** · Bougie Mahjong · colour · no partner code in FYM (allowed mat): vineyard sepia _(#8, FYM oct31-v108)_
- **Country Club Christmas** · Bougie Mahjong · holiday · no partner code in FYM (allowed mat) **[holiday]**: Country Club Christmas _(#13, FYM oct31-v108)_
- **Green Scottish Plaid** · Amazon · holiday · non-partner, her ShopMy pick **[holiday]**: olive Scottish plaid _(#16, staged Amazon holiday pick (never in catalog))_

## Sunset: 8 strong (1 holiday)
Built ~2026-10-22 · 15 cards live · 696 mats it never saw, 91 colour-qualified · sheet `assets/qa/album-missed-nov07/sunset.jpg`

- **Texas Mon Amour Peach** · Fait à Main · colour · no partner code in FYM (allowed mat): Fait a Main peach bandana _(#1, FYM oct26-partners)_
- **Orange Gingham** · Mahj & Moon · colour · no partner code in FYM (allowed mat): Mahj & Moon orange gingham _(#3, FYM oct31-v108)_
- **Pink Voltage** · Let's Be Besties · colour · partner (code): orange + pink + red stripes (the layers) _(#8, FYM nov01-v113)_
- **Fall Pop Garden** · Let's Be Besties · colour · partner (code): orange + pink florals _(#12, FYM nov01-v113)_
- **Botanical Garden** · Let's Be Besties · colour · partner (code): orange + aqua folk _(#5, FYM nov01-v113)_
- **Martini** · YOLO Mahjong · colour · partner (code): YOLO pink/orange martini _(#10, FYM oct30-v106)_
- **Pumpkin Patch** · Mahj & Moon · colour + motif · no partner code in FYM (allowed mat): Mahj & Moon pumpkin patch (fall) _(#4, FYM oct31-v108)_
- **Orange and Pink Christmas** · Let's Be Besties · holiday · partner (code) **[holiday]**: orange + pink Christmas _(#14, FYM nov01-v113)_

## Talulah: 8 strong (2 holiday)
Built ~2026-10-15 · 28 cards live · 807 mats it never saw, 600 colour-qualified · sheet `assets/qa/album-missed-nov07/talulah.jpg`

- **Brooklyn Branches** · Let's Be Besties · colour · partner (code): pale blue + pink blossom + brown fret (brown layer) _(#1, FYM oct16lbb)_
- **Lotus Cove** · Oh My Mahjong · colour · partner (code): OMM Lotus Cove: teal + pink, same brand _(#3, FYM nov05-v115)_
- **Honeybee Tiles** · Mahj & Moon · colour · no partner code in FYM (allowed mat): Mahj & Moon blue/peach honeybee _(#2, FYM oct31-v108)_
- **Garden Lilies** · Let's Be Besties · colour · partner (code): aqua + coral lilies _(#10, FYM oct16lbb)_
- **Serene Pastel Turtles** · YOLO Mahjong · colour · partner (code): pastel turtles _(#8, FYM oct30-v106)_
- **Pastel Coastal Beach** · YOLO Mahjong · colour · partner (code): pastel coastal _(#9, FYM oct30-v106)_
- **Pastel Christmas Tree** · Mahj & Moon · holiday · no partner code in FYM (allowed mat) **[holiday]**: Mahj & Moon aqua/pink Christmas tree _(#13, FYM oct31-v108)_
- **Peppermint Chinoiserie Christmas** · Bougie Mahjong · holiday · no partner code in FYM (allowed mat) **[holiday]**: peppermint chinoiserie _(#16, FYM oct31-v108)_

## Taylor: 7 strong (1 holiday)
Built ~2026-10-22 · 21 cards live · 696 mats it never saw, 300 colour-qualified · sheet `assets/qa/album-missed-nov07/taylor.jpg`

- **Lavender Flowers** · Let's Be Besties · colour · partner (code): lavender roses _(#1, FYM nov01-v113)_
- **Lavender Gator Skin** · Let's Be Besties · colour · partner (code): lavender gator _(#3, FYM nov01-v113)_
- **Purple Peacock Circle** · Let's Be Besties · colour · partner (code): lavender peacock _(#9, FYM nov01-v113)_
- **Summer Bloom** · Mahj & Moon · colour · no partner code in FYM (allowed mat): Mahj & Moon lavender floral _(#12, FYM oct31-v108)_
- **Pastel Parrot Round** · YOLO Mahjong · colour · partner (code): pastel parrots _(#4, FYM oct30-v106)_
- **Classic Ballet Pink** · Case-Mate · colour · non-partner, her ShopMy pick: Case-Mate Classic Ballet Pink _(#2, staged ShopMy (never in catalog))_
- **Pink Christmas Tree Gingham** · Amazon · holiday · non-partner, her ShopMy pick **[holiday]**: pink tree gingham _(#15, staged Amazon holiday pick (never in catalog))_

## Classic Tortoise: 8 strong (2 holiday)
Built ~2026-10-15 · 50 cards live · 807 mats it never saw, 479 colour-qualified · sheet `assets/qa/album-missed-nov07/tortoise.jpg`

- **Champagne Conservatory** · Bougie Mahjong · colour · no partner code in FYM (allowed mat): cream + champagne gold damask _(#2, FYM oct31-v108)_
- **Fern Berry Wreath** · Luna EK Studio · colour · no partner code in FYM (allowed mat): sepia/cream botanical wreath _(#5, FYM nov03-etsy)_
- **Herbal Drawing Butterfly Border** · Luna EK Studio · colour · no partner code in FYM (allowed mat): sepia herbal butterfly border _(#6, FYM nov03-etsy)_
- **Meadow Butterfly Border** · Luna EK Studio · colour · no partner code in FYM (allowed mat): cream meadow border _(#4, FYM nov03-etsy)_
- **Lotus Garden Frame** · Luna EK Studio · colour + motif · no partner code in FYM (allowed mat): cream/sage chinoiserie lotus garden _(#12, FYM nov03-etsy)_
- **Regency** · Mahj Squad · colour · partner (code): Mahj Squad Regency: cream + gilt (brand photo has props) _(#10, FYM oct16)_
- **Scandi Folk Christmas (Cream)** · Etsy · holiday · no partner code in FYM (allowed mat) **[holiday]**: cream Scandi folk _(#14, FYM oct26-etsy)_
- **Christmas Tree Gingham** · Amazon · holiday · non-partner, her ShopMy pick **[holiday]**: cream/red tree gingham _(#16, staged Amazon holiday pick (never in catalog))_

## Willow: 9 strong (2 holiday)
Built ~2026-10-15 · 51 cards live · 807 mats it never saw, 339 colour-qualified · sheet `assets/qa/album-missed-nov07/willow.jpg`

- **Jade Pagoda Chinoiserie** · Bougie Mahjong · colour + motif · no partner code in FYM (allowed mat): jade/sage pagoda chinoiserie (motif) _(#12, FYM oct31-v108)_
- **Evergreen Medallion** · Let's Be Besties · colour · partner (code): sage + forest medallion _(#1, FYM nov01-v113)_
- **Pandas** · Let's Be Besties · colour · partner (code): sage bamboo pandas _(#2, FYM nov01-v113)_
- **Grand Rose Medallion Chinoiserie** · Let's Be Besties · colour + motif · partner (code): sage leaves + pink roses chinoiserie _(#4, FYM nov01-v113)_
- **Palm Court Tennis Club** · Bougie Mahjong · colour + motif · no partner code in FYM (allowed mat): green palm tennis club _(#7, FYM oct31-v108)_
- **Blue Hydrangea** · Piper Chase Studios · colour · no partner code in FYM (allowed mat): blue hydrangea + green fret (navy layer) _(#8, FYM oct31-v109)_
- **Martini Shaken** · Let's Be Besties · colour · partner (code): olive/sage martini _(#9, FYM nov01-v113)_
- **Merrywood Leatherette** · Britt Mills · holiday · partner (code) **[holiday]**: Britt Mills Merrywood, sage centre _(#14, FYM oct27-v101)_
- **Ornamental Charm** · Let's Be Besties · holiday · partner (code) **[holiday]**: sage + pink ornaments _(#15, FYM oct30-v105)_
