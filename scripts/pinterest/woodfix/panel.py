from PIL import Image, ImageDraw, ImageFont, ImageFilter
IB='/usr/share/fonts/opentype/inter/Inter-Bold.otf'; IS='/usr/share/fonts/opentype/inter/Inter-SemiBold.otf'
CREAM=(251,243,230); PINK=(232,90,130); PURPLE=(84,52,104)
def panel(src, dst, x0, x1, ytop, y0, y1, yend, pad=8):
    im = Image.open(src).convert('RGB')
    chunk = im.crop((x0, y1, x1, yend))           # remaining color rows (with labels)
    px0, px1, py0, py1 = x0 - pad, min(x1 + pad, 1080) if x1 < 1080 else 1080 - 0, ytop, yend + pad
    if x0 <= 0: px0 = 0
    # shadow
    sh = Image.new('RGBA', im.size, (0,0,0,0)); ImageDraw.Draw(sh).rounded_rectangle([px0+3, py0+5, px1+3, py1+5], 18, fill=(0,0,0,70))
    sh = sh.filter(ImageFilter.GaussianBlur(6)); im.paste(sh, (0,0), sh)
    d = ImageDraw.Draw(im); d.rounded_rectangle([px0, py0, px1, py1], 18, fill=CREAM)
    f1 = ImageFont.truetype(IB, 20); f2 = ImageFont.truetype(IS, 26)
    cx = (px0 + px1) // 2
    total_head = 30 + 34
    content = total_head + 14 + chunk.height
    top = py0 + max(12, ((py1 - py0) - content) // 2)
    d.text((cx, top), 'RACK MATCHES', font=f1, fill=PINK, anchor='ma')
    d.text((cx, top + 30), 'Bird & Bamboo', font=f2, fill=PURPLE, anchor='ma')
    cy = top + total_head + 14
    im.paste(chunk, (x0, cy))
    im.save(dst, quality=95)
