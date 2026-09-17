from PIL import Image, ImageDraw, ImageFont
FB = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
def grad(w, h):
    im = Image.new('RGB', (w, h)); d = ImageDraw.Draw(im)
    for y in range(h):
        t = y / h
        d.line([(0, y), (w, y)], fill=(int(20 + 30 * t), int(18 + 10 * t), int(60 + 70 * (1 - t))))
    return im
f = lambda s: ImageFont.truetype(FB, s)
im = grad(512, 512); d = ImageDraw.Draw(im)
d.rounded_rectangle([96, 100, 416, 320], radius=36, outline=(255, 196, 0), width=14)
d.polygon([(222, 150), (222, 270), (322, 210)], fill=(255, 196, 0))
d.rectangle([200, 320, 312, 340], fill=(255, 196, 0)); d.rectangle([160, 340, 352, 356], fill=(255, 196, 0))
t = 'Andinoid TV'; w = d.textlength(t, font=f(56)); d.text(((512 - w) / 2, 390), t, font=f(56), fill='white')
for p in ('src/plugin.program.andinoidtv/icon.png', 'src/repository.andinoidtv/icon.png'): im.save(p)
fa = grad(1280, 720); d = ImageDraw.Draw(fa)
t = 'Andinoid TV'; w = d.textlength(t, font=f(110)); d.text(((1280 - w) / 2, 260), t, font=f(110), fill='white')
t = 'Películas · Series · Anime · TV'; w = d.textlength(t, font=f(40)); d.text(((1280 - w) / 2, 410), t, font=f(40), fill=(255, 196, 0))
for p in ('src/plugin.program.andinoidtv/fanart.jpg', 'src/repository.andinoidtv/fanart.jpg'): fa.save(p, quality=85)
