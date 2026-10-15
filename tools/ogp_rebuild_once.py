from pathlib import Path
import re
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps

ROOT = Path(".")
IMG = ROOT / "assets/images"
W, H = 1200, 630
JP_REG = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
JP_BOLD = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
LATIN = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
def font(sz, bold=False):
    p = JP_BOLD if bold else JP_REG
    if not Path(p).exists():
        p = LATIN
    return ImageFont.truetype(p, sz)

def rgb(path):
    with Image.open(IMG / path) as im:
        return im.convert("RGB").copy()

def put_cover(base, path, dim=125, blur=0, centering=(.5,.45)):
    im = ImageOps.fit(rgb(path), (W,H), method=Image.Resampling.LANCZOS, centering=centering)
    if blur: im = im.filter(ImageFilter.GaussianBlur(blur))
    base.paste(im,(0,0))
    base.alpha_composite(Image.new("RGBA",(W,H),(0,0,0,dim)))

def text(d,xy,s,sz,color,bold=False,spacing=None):
    d.text(xy,s, font=font(sz,bold), fill=color, spacing=spacing or 4)

def poster_panel(base,path,top=36,height=558,right=52):
    src=rgb(path); w=round(src.width*height/src.height)
    img=src.resize((w,height),Image.Resampling.LANCZOS)
    x=W-right-w
    sh=Image.new("RGBA",(w+20,height+20),(0,0,0,0))
    sd=ImageDraw.Draw(sh);sd.rounded_rectangle((10,10,w+10,height+10),radius=2,fill=(0,0,0,175))
    sh=sh.filter(ImageFilter.GaussianBlur(12))
    base.alpha_composite(sh,(x-4,top+1))
    base.paste(img,(x,top))
    return x

def rule(d,x1,y,x2,color=(194,182,156,180)):
    d.line((x1,y,x2,y), fill=color, width=2)

def build_home():
    b=Image.new("RGBA",(W,H),(8,10,10,255))
    d=ImageDraw.Draw(b)
    # Keep the dark, restrained identity of the home page.
    d.rectangle((0,0,18,H), fill=(125,132,117,255))
    d.ellipse((480,45,720,285), outline=(97,107,104,170), width=2)
    with Image.open(IMG/"tmf-mark.gif") as mark:
        img=mark.convert("RGBA")
        img.thumbnail((330,240), Image.Resampling.LANCZOS)
        b.alpha_composite(img,((W-img.width)//2,52))
    text(d,(188,310),"TINY MOUSE FACTORY",65,(245,244,240,255),True)
    rule(d,340,429,860,(108,116,110,255))
    text(d,(355,458),"FILM  /  DOCUMENTARY  /  MUSIC",24,(178,183,175,255))
    return b

def build_yuragi():
    b=Image.new("RGBA",(W,H),(11,11,11,255))
    put_cover(b,"yuragi-fire.webp",dim=198,blur=8)
    d=ImageDraw.Draw(b)
    d.rectangle((0,0,735,H),fill=(11,12,13,130))
    poster_panel(b,"yuragi-poster.webp",top=31,height=569,right=49)
    text(d,(64,98),"DOCUMENTARY FILM",23,(212,182,143,255))
    text(d,(57,190),"揺らぎの聲",76,(255,250,243,255),True)
    rule(d,63,312,669,(178,151,122,255))
    text(d,(63,342),"FORGING A PRAYER",38,(249,243,235,255))
    text(d,(65,400),"VOICE OF THE KATANA",25,(220,213,201,255))
    text(d,(65,550),"TINY MOUSE FACTORY",18,(202,202,202,255))
    return b

def build_minna(screenings=False):
    b=Image.new("RGBA",(W,H),(242,235,220,255))
    d=ImageDraw.Draw(b)
    d.rectangle((0,0,22,H),fill=(106,119,100,255))
    d.ellipse((-195,-210,425,410),outline=(212,202,179,255),width=4)
    poster_panel(b,"minna-poster.webp",top=30,height=572,right=45)
    text(d,(72,91),"DOCUMENTARY FILM  /  2025",23,(95,113,83,255))
    if screenings:
        text(d,(68,194),"みんなのふね",59,(53,65,51,255),True)
        text(d,(72,296),"過去の上映会",52,(65,75,59,255),True)
        text(d,(74,389),"PAST SCREENINGS",26,(119,106,85,255))
    else:
        text(d,(66,218),"みんなのふね",76,(53,65,51,255),True)
        text(d,(72,333),"MINNA: A BOAT",27,(104,105,84,255))
        text(d,(72,371),"FOR EVERYONE",27,(104,105,84,255))
    rule(d,73,478,724,(171,166,137,255))
    text(d,(74,533),"TINY MOUSE FACTORY",19,(114,116,102,255))
    return b

def build_films():
    b=Image.new("RGBA",(W,H),(18,19,18,255))
    d=ImageDraw.Draw(b)
    d.rectangle((0,0,18,H),fill=(169,155,136,255))
    poster_panel(b,"minna-poster.webp",top=74,height=465,right=36)
    poster_panel(b,"yuragi-poster.webp",top=74,height=465,right=390)
    text(d,(65,150),"DOCUMENTARY",28,(187,187,172,255))
    text(d,(60,208),"FILMS",89,(250,247,240,255),True)
    rule(d,65,338,464,(138,133,121,255))
    text(d,(65,374),"TINY MOUSE",26,(221,217,208,255))
    text(d,(65,410),"FACTORY",26,(221,217,208,255))
    return b

def build_photo_page(photo, heading, subtitle, color=(13,16,17,255)):
    b=Image.new("RGBA",(W,H),color)
    put_cover(b,photo,dim=105,blur=1)
    # Graduated dark overlay keeps titles legible without covering the still.
    sh=Image.new("RGBA",(W,H),(0,0,0,0))
    p=sh.load()
    for x in range(W):
        a=int(224*max(0,1-x/930)**1.3)
        for y in range(H):p[x,y]=(8,11,14,a)
    b.alpha_composite(sh)
    d=ImageDraw.Draw(b)
    d.rectangle((0,0,15,H),fill=(173,168,149,255))
    text(d,(77,157),heading,85,(250,249,246,255),True)
    rule(d,80,288,635,(183,183,167,255))
    text(d,(80,323),subtitle,26,(234,235,229,255))
    text(d,(80,544),"TINY MOUSE FACTORY",22,(236,237,232,255))
    return b

names = {
    "ogp-top-v2.jpg":build_home(),
    "ogp-yuragi-v2.jpg":build_yuragi(),
    "ogp-minna-v2.jpg":build_minna(),
    "ogp-minna-screenings-v2.jpg":build_minna(True),
    "ogp-films-v2.jpg":build_films(),
    "ogp-works-v2.jpg":build_photo_page("tokyo-tower.webp","WORKS","FILM  /  DRONE  /  VR  /  MUSIC"),
    "ogp-about-v2.jpg":build_photo_page("about-cinematography.webp","ABOUT","YUKI NISHIYAMA  /  FILMMAKER"),
    "ogp-contact-v2.jpg":build_photo_page("hero.webp","CONTACT","FILM  /  VIDEO  /  MUSIC"),
}
for name,im in names.items():
    dest=IMG/name
    im.convert("RGB").save(dest,"JPEG",quality=92,subsampling=0,optimize=True,progressive=True)
    check=Image.open(dest); check.load()
    assert check.size==(1200,630) and check.format=="JPEG"
    print("created",name,dest.stat().st_size)

mapping = {
    "index.html":"ogp-top-v2.jpg",
    "films/yuragi.html":"ogp-yuragi-v2.jpg",
    "films/minna.html":"ogp-minna-v2.jpg",
    "films/minna-screenings.html":"ogp-minna-screenings-v2.jpg",
    "films.html":"ogp-films-v2.jpg",
    "works.html":"ogp-works-v2.jpg",
    "about.html":"ogp-about-v2.jpg",
    "contact.html":"ogp-contact-v2.jpg",
}
def replace_or_add_meta(s, attr, key, value):
    tag=f'<meta {attr}="{key}" content="{value}">'
    pattern=r'<meta\b(?=[^>]*\b'+re.escape(attr)+r'\s*=\s*["\x27]'+re.escape(key)+r'["\x27])[^>]*>'
    if re.search(pattern,s,re.I):
        return re.sub(pattern,lambda _:tag,s,flags=re.I)
    return s.replace("</head>",tag+"\n</head>",1)
for filename,ogp in mapping.items():
    path=ROOT/filename
    html=path.read_text(encoding="utf-8")
    u="https://tiny-mouse.net/assets/images/"+ogp
    for attr,key,val in [
        ("property","og:image",u),
        ("property","og:image:secure_url",u),
        ("property","og:image:width","1200"),
        ("property","og:image:height","630"),
        ("property","og:image:type","image/jpeg"),
        ("name","twitter:image",u),
        ("name","twitter:card","summary_large_image"),
    ]:
        html=replace_or_add_meta(html,attr,key,val)
    if filename=="films/minna-screenings.html":
        vals=[
            ("property","og:locale","ja_JP"),
            ("property","og:type","website"),
            ("property","og:site_name","Tiny Mouse Factory"),
            ("property","og:title","過去の上映会｜映画『みんなのふね』"),
            ("property","og:description","映画『みんなのふね』の過去の上映会一覧。全国各地の上映記録。"),
            ("property","og:url","https://tiny-mouse.net/films/minna-screenings.html"),
            ("name","twitter:title","過去の上映会｜映画『みんなのふね』"),
        ]
        for attr,key,val in vals: html=replace_or_add_meta(html,attr,key,val)
    path.write_text(html,encoding="utf-8")
    assert html.count(u)>=2
    print("updated",filename)
