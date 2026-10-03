from pathlib import Path
import re, hashlib, io
import requests
from bs4 import BeautifulSoup
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
FILMS = ROOT / 'films'
IMAGES = ROOT / 'assets' / 'images'
WIX = 'https://tinymousenet.wixsite.com/everyonesboat'
SCREENINGS = WIX + '/general-5'

session = requests.Session()
session.headers.update({'User-Agent':'Mozilla/5.0 TinyMouseFactory migration'})

def get(url):
    r = session.get(url, timeout=45)
    r.raise_for_status()
    return r

def text_lines(url):
    soup = BeautifulSoup(get(url).text, 'html.parser')
    return [re.sub(r'\s+', ' ', x).strip() for x in soup.stripped_strings if x.strip()]

def slice_lines(lines, start, end):
    try: a = next(i for i,x in enumerate(lines) if x == start)
    except StopIteration: return []
    try: b = next(i for i,x in enumerate(lines[a+1:], a+1) if x == end)
    except StopIteration: b = len(lines)
    return lines[a+1:b]

def el(soup, tag, text='', cls=None):
    node=soup.new_tag(tag)
    if cls: node['class']=cls.split()
    if text: node.string=text
    return node

def add_link(soup, parent, text, href):
    a=soup.new_tag('a', href=href); a.string=text; a['target']='_blank'; a['rel']='noopener'; parent.append(a); return a

def download_to_webp(url, name):
    try:
        r=get(url)
        im=Image.open(io.BytesIO(r.content))
        im=ImageOps.exif_transpose(im).convert('RGB')
        max_edge=1600
        if max(im.size)>max_edge:
            scale=max_edge/max(im.size); im=im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.LANCZOS)
        out=IMAGES/name
        im.save(out,'WEBP',quality=82,method=6)
        return '../assets/images/'+name
    except Exception as e:
        print('image download failed',url,e)
        return url

def replace_remote_images(soup):
    used={}
    for img in soup.find_all('img'):
        src=img.get('src','')
        if 'static.wixstatic.com' not in src: continue
        key=src.split('~mv2')[0].split('_')[-1]
        name=used.setdefault(src, f'minna-wix-{key[:10]}.webp')
        img['src']=download_to_webp(src,name)
        img['decoding']='async'
    return soup

main_lines=text_lines(WIX)
screen_lines=text_lines(SCREENINGS)

# Start from the approved draft design.
draft=(FILMS/'minna-draft.html').read_text(encoding='utf-8')
soup=BeautifulSoup(draft,'html.parser')

# Production metadata.
for m in soup.find_all('meta', attrs={'name':'robots'}): m.decompose()
soup.title.string='映画『みんなのふね』公式サイト｜Minna: A Boat for Everyone'
desc=soup.find('meta',attrs={'name':'description'})
desc['content']='石おのと樹齢250年の杉から丸木舟を作る「Jomonさんがやってきた！プロジェクト」を2年以上追ったドキュメンタリー映画『みんなのふね』公式サイト。上映会、監督トーク、受賞歴、作品情報。'
for x in soup.select('.minna-draft-note'): x.decompose()
# remove placeholders / draft-only wording
for x in soup.select('.minna-placeholder'): x.decompose()
for p in soup.find_all('p'):
    if '最新の映画祭受賞・公式選出情報' in p.get_text(): p.string='世界各地の映画祭にて受賞・公式選出されました。'

# Canonical / social / structured data.
head=soup.head
for tag in head.find_all(['link','meta'], attrs={'property':True}):
    if str(tag.get('property','')).startswith('og:'): tag.decompose()
for tag in head.find_all('meta', attrs={'name':re.compile('^twitter:')}): tag.decompose()
canon=head.find('link',rel='canonical')
if not canon:
    canon=soup.new_tag('link',rel='canonical'); head.append(canon)
canon['href']='https://tiny-mouse.net/films/minna.html'
meta_specs=[
('property','og:locale','ja_JP'),('property','og:type','video.movie'),('property','og:site_name','Tiny Mouse Factory'),
('property','og:title','映画『みんなのふね』 | Minna: A Boat for Everyone'),
('property','og:description','人・自然・地球——。石おのと一本の巨木から始まった、2年以上にわたる丸木舟づくりの記録。'),
('property','og:url','https://tiny-mouse.net/films/minna.html'),
('property','og:image','https://tiny-mouse.net/assets/images/minna-poster.webp'),
('name','twitter:card','summary_large_image'),('name','twitter:title','映画『みんなのふね』 | Minna: A Boat for Everyone'),
('name','twitter:description','石おのと一本の巨木から始まった、2年以上にわたる丸木舟づくりの記録。'),
('name','twitter:image','https://tiny-mouse.net/assets/images/minna-poster.webp')]
for kind,key,val in meta_specs:
    m=soup.new_tag('meta'); m[kind]=key; m['content']=val; head.append(m)
ld=soup.new_tag('script',type='application/ld+json')
ld.string='{"@context":"https://schema.org","@type":"Movie","name":"みんなのふね","alternateName":"Minna: A Boat for Everyone","dateCreated":"2025","duration":"PT91M","inLanguage":"ja","countryOfOrigin":{"@type":"Country","name":"Japan"},"image":"https://tiny-mouse.net/assets/images/minna-poster.webp","url":"https://tiny-mouse.net/films/minna.html","director":{"@type":"Person","name":"にしやまゆうき"},"musicBy":{"@type":"Person","name":"にしやまゆうき"},"productionCompany":{"@type":"Organization","name":"Tiny Mouse Factory"}}'
head.append(ld)

# Add a small in-page navigation under the global header.
header=soup.find('header')
sub=soup.new_tag('nav'); sub['class']=['minna-subnav']; sub['aria-label']='みんなのふね ページ内メニュー'
w=soup.new_tag('div'); w['class']=['wrap']; sub.append(w)
for label,href in [('STORY','#story'),('VOICES','#voices'),('SCREENING','#screening'),('AWARDS','#awards'),('PROJECT','#project'),('PEOPLE','#people'),('STAFF','#staff'),('PAST SCREENINGS','minna-screenings.html')]:
    a=soup.new_tag('a',href=href); a.string=label; w.append(a)
header.insert_after(sub)
style=soup.find('style')
style.string=(style.string or '')+'\n.minna-subnav{position:sticky;top:64px;z-index:8;background:rgba(235,228,212,.95);border-bottom:1px solid var(--minna-line);backdrop-filter:blur(12px)}.minna-subnav .wrap{display:flex;gap:22px;overflow:auto;padding-top:11px;padding-bottom:11px;scrollbar-width:none}.minna-subnav a{white-space:nowrap;color:#696155;text-decoration:none;font-size:10px;letter-spacing:.12em}.minna-subnav a:hover{color:#111}.director-comment{max-width:900px;margin-top:48px;padding-top:38px;border-top:1px solid var(--minna-line)}.director-comment p{font-size:15px;line-height:2.05;margin:0 0 22px}.director-sign{font-weight:600}.thanks-box{display:grid;grid-template-columns:1fr 1fr;gap:42px;align-items:center}.thanks-box img{width:100%;display:block}@media(max-width:900px){.thanks-box{grid-template-columns:1fr}.minna-subnav{top:56px}}'

# IDs for anchors.
for eyebrow, ident in [('Story','story'),('Voices / Reviews','voices'),('Screenings / Talks','screening'),('Awards / Film Festivals','awards'),('Project','project'),('Main Character','people'),('Staff','staff')]:
    node=soup.find(class_='eyebrow', string=lambda s: s and s.strip()==eyebrow)
    if node: node.find_parent('section')['id']=ident

# Ensure approved story line break stays.
lead=soup.select_one('.minna-lead')
if lead:
    lead.clear(); lead.append('「みんなが笑顔で乗れる舟を作ろう」'); lead.append(soup.new_tag('br')); lead.append('——縄文大工・雨宮国広が挑んだのは、石おのだけで樹齢250年の杉から巨大な丸木舟を生み出すこと。')

# Past-screenings button points to production page.
for a in soup.find_all('a'):
    if a.get('href')=='minna-screenings-draft.html':
        a['href']='minna-screenings.html'; a.string='過去の上映会一覧 →'

# Expand main-character profile using Wix content.
mc=soup.find(class_='eyebrow',string=lambda s:s and s.strip()=='Main Character')
if mc:
    prof=mc.find_parent('section').select_one('.profile-copy')
    if prof:
        prof.clear()
        paras=[
        '1969年、山梨県生まれ。丸太の皮むきのバイトをきっかけに大工の道へ。',
        'ログハウスビルダー→大工→二級建築士→宮大工と歩み、古民家や社寺文化財の修復等、手道具での伝統的な手法に傾倒する中、2009年に石おのと出会い、その素晴らしさに気づく。',
        '石川県・真脇遺跡にて石おの等を用いた縄文住居の復元、国立科学博物館での考古学実験「3万年前の航海 徹底再現プロジェクト」においては、伐採から石おのを使用して外洋航海用丸木舟を製作。手道具のみで自作した「縄文小屋」と呼ぶ小屋に暮らす。',
        '2025年、（公財）やまなし環境財団より、優れた環境保全活動を行っているとして「若宮賞」を受賞。',
        '現在は丸木舟で日本全国の海を沿岸のゴミ清掃をしながら漕ぎ回っている。纏う衣装はロードキル被害で命を落とした生き物たちの忘れ形見。']
        for t in paras: prof.append(el(soup,'p',t))

# Director: add photo and complete Wix comment.
dir_sec=None
for n in soup.find_all(class_='eyebrow'):
    if n.get_text(strip=True)=='Director / Music': dir_sec=n.find_parent('section'); break
if dir_sec:
    wrap=dir_sec.find(class_='wrap')
    # make current content a profile grid and add director photo
    if wrap and not wrap.find(class_='minna-person'):
        inner=soup.new_tag('div'); inner['class']=['minna-person']
        img=soup.new_tag('img',src='https://static.wixstatic.com/media/f5daca_f3d7023299d44d3790f2b3455f8ab9e9~mv2.jpg/v1/fill/w_980,h_735,al_c,q_85,usm_0.66_1.00_0.01,quality_auto/f5daca_f3d7023299d44d3790f2b3455f8ab9e9~mv2.jpg',alt='監督・にしやまゆうき'); img['loading']='lazy'
        right=soup.new_tag('div')
        for child in list(wrap.contents): right.append(child.extract())
        inner.append(img); inner.append(right); wrap.append(inner)
    comment_lines=slice_lines(main_lines,'監督のコメント','制作スタッフ')
    # Strip known non-comment artifacts/links.
    comment_lines=[x for x in comment_lines if x not in ('Spotify','Apple Podcast','Amazon Music') and not x.startswith('http')]
    # Keep only from the first actual sentence.
    try: start=next(i for i,x in enumerate(comment_lines) if x.startswith('電動工具も鉄製道具も使わないで'))
    except StopIteration: start=0
    comment_lines=comment_lines[start:]
    box=soup.new_tag('div'); box['class']=['wrap','director-comment']; box.append(el(soup,'div',"Director's Comment",'eyebrow')); box.append(el(soup,'h3','監督のコメント'))
    for t in comment_lines:
        if t in ('監督 にしやまゆうき','監督　にしやまゆうき'): continue
        box.append(el(soup,'p',t))
    sign=el(soup,'p','監督　にしやまゆうき','director-sign'); box.append(sign)
    dir_sec.append(box)

# Full staff credits parsed from Wix.
staff_sec=None
for n in soup.find_all(class_='eyebrow'):
    if n.get_text(strip=True) in ('Staff','Staff / Credits'): staff_sec=n.find_parent('section'); break
if staff_sec:
    dl=staff_sec.find('dl')
    staff_lines=slice_lines(main_lines,'制作スタッフ','サウンドトラック販売中')
    labels=['企画','プロデューサー','撮影','ドローンオペレーター','英語字幕作成','撮影協力','協力','印刷・出版','編集/MA','挿入曲','エンディングテーマ','制作','監督']
    # Build blocks between exact labels.
    positions=[]
    for i,x in enumerate(staff_lines):
        if x in labels: positions.append((i,x))
    if dl and positions:
        dl.clear()
        for j,(idx,label) in enumerate(positions):
            end=positions[j+1][0] if j+1<len(positions) else len(staff_lines)
            vals=[v for v in staff_lines[idx+1:end] if v and not v.startswith('Image')]
            dt=el(soup,'dt',label); dd=el(soup,'dd',' '.join(vals));
            if label in ('撮影協力','協力'): dd['class']=['long']
            dl.append(dt); dl.append(dd)
    eye=staff_sec.find(class_='eyebrow'); eye.string='Staff / Credits'

# Soundtrack + crowdfunding thank-you from Wix.
sound=None
for n in soup.find_all(class_='eyebrow'):
    if n.get_text(strip=True)=='Soundtrack': sound=n.find_parent('section'); break
if sound:
    wrap=sound.find(class_='wrap')
    if wrap:
        thank=soup.new_tag('div'); thank['class']=['thanks-box']; thank['style']='margin-top:48px;padding-top:38px;border-top:1px solid var(--minna-line)'
        txt=soup.new_tag('div'); txt.append(el(soup,'div','Crowdfunding','eyebrow')); txt.append(el(soup,'h3','編集資金クラウドファンディング')); txt.append(el(soup,'p','皆様の応援で達成致しました。')); txt.append(el(soup,'p','ご協力いただき誠にありがとうございます。'))
        img=soup.new_tag('img',src='https://static.wixstatic.com/media/f5daca_79c3f9adba2a420fa349ad6bf64d4d6b~mv2.jpg/v1/fill/w_660,h_371,al_c,q_80,usm_0.66_1.00_0.01,quality_auto/f5daca_79c3f9adba2a420fa349ad6bf64d4d6b~mv2.jpg',alt='映画「みんなのふね」クラウドファンディング'); img['loading']='lazy'
        thank.append(txt); thank.append(img); wrap.append(thank)

# Replace old email-copy paragraph with current contact form wording.
contact_eye=soup.find(class_='eyebrow',string=lambda s:s and s.strip()=='Contact')
if contact_eye:
    cp=contact_eye.find_parent('section').select_one('.minna-copy p')
    if cp: cp.string='上映会、監督トーク・講演、取材、作品に関するお問い合わせはTiny Mouse FactoryのCONTACTフォームよりご連絡ください。'

# Final image localization (all Wix CDN images now embedded in this page become local WebP).
soup=replace_remote_images(soup)
(FILMS/'minna.html').write_text(str(soup),encoding='utf-8')

# Build past-screenings page directly from the Wix history page.
joined='\n'.join(screen_lines)
events=[]
for m in re.finditer(r'(202[456]年.*?)(?=202[456]年|©2025|$)',joined,re.S):
    t=re.sub(r'\s+',' ',m.group(1)).strip()
    if len(t)<8: continue
    # stop accidental footer/nav capture
    if 'みんなのふね - Jomon-san Has Come' in t: t=t.split('みんなのふね - Jomon-san Has Come')[0].strip()
    events.append(t)
by={2026:[],2025:[],2024:[]}
for e in events:
    y=int(e[:4]);
    if y in by: by[y].append(e)
rows=[]
for y in (2026,2025,2024):
    rows.append(f'<section class="year"><div class="wrap"><h2>{y}</h2><div class="screen-list">')
    for e in by[y]:
        body=e[5:].strip(); parts=re.split(r'\s{2,}| / ',body,maxsplit=1); first=parts[0]
        mm=re.match(r'([^　 ]+)[　 ]+(.*)',first)
        if mm: date,place=mm.group(1),mm.group(2)
        else: date,place='',first
        note=(' / '+parts[1]) if len(parts)>1 else ''
        rows.append(f'<div class="screen-row"><div class="screen-date">{date}</div><div class="screen-place">{place}<span class="screen-note">{note}</span></div></div>')
    rows.append('</div></div></section>')
screen_html='''<!doctype html><html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>過去の上映会｜映画『みんなのふね』</title><meta name="description" content="映画『みんなのふね』の過去の上映会一覧。全国各地で開催された自主上映会の記録。"><link rel="canonical" href="https://tiny-mouse.net/films/minna-screenings.html"><link rel="icon" href="/favicon.ico" sizes="any"><link rel="stylesheet" href="../assets/style.css"><style>:root{--paper:#f3efe4;--paper2:#ebe4d4;--ink:#403a31;--line:#d5cbb8;--green:#586653}body{background:var(--paper);color:var(--ink);font-family:Arial,"Hiragino Kaku Gothic ProN","Yu Gothic",sans-serif}header{background:rgba(243,239,228,.96);border-bottom:1px solid var(--line)}.brand,.menu{color:#403a31}.brand img{filter:invert(1);opacity:.78}.screen-hero{padding:72px 0 46px}.screen-hero h1{font-size:clamp(42px,7vw,82px);line-height:1;margin:8px 0 22px}.screen-hero p{max-width:760px;line-height:2;color:#746b5f}.eyebrow{color:var(--green)}.year{padding:48px 0;border-top:1px solid var(--line)}.year:nth-of-type(even){background:var(--paper2)}.year h2{font-size:34px;margin:0 0 20px}.screen-list{border-top:1px solid var(--line)}.screen-row{display:grid;grid-template-columns:150px 1fr;gap:26px;padding:17px 0;border-bottom:1px solid var(--line);line-height:1.75}.screen-date{font-size:12px;color:#7b7266}.screen-place{font-size:14px}.screen-note{font-size:12px;color:#817769}.actions{display:flex;gap:12px;flex-wrap:wrap;margin-top:32px}.actions a{display:inline-block;padding:12px 18px;border:1px solid #877b69;color:#453d33;text-decoration:none;font-size:11px;letter-spacing:.08em}footer{border-top:1px solid var(--line);color:#81786b}@media(max-width:620px){.screen-row{grid-template-columns:1fr;gap:4px}}</style></head><body><header><div class="wrap nav"><a class="brand" href="../index.html"><img src="../assets/images/tmf-mark.gif" alt=""><span>TINY MOUSE FACTORY</span></a><nav class="menu"><a class="active" href="../films.html">FILMS</a><a href="../works.html">WORKS</a><a href="../about.html">ABOUT</a><a href="../contact.html">CONTACT</a></nav></div></header><main><div class="wrap screen-hero"><div class="eyebrow">Minna: A Boat for Everyone</div><h1>過去の上映会</h1><p>『みんなのふね』は2026年5月までの1年余、皆様のご協力による自主上映会でお届けしてきました。ご協力頂きました皆様に心より御礼申し上げます。</p><p>2026年6月より、上映会開催サービス「cinemo」にて取り扱いが始まりました。是非cinemoで上映会の開催をご検討くださいませ。</p><div class="actions"><a href="minna.html">映画公式ページへ →</a><a href="https://www.cinemo.info/147j" target="_blank" rel="noopener">cinemo 上映申込 →</a></div></div>'''+''.join(rows)+'''</main><footer><div class="wrap foot"><span>© Tiny Mouse Factory</span><span>みんなのふね / 過去の上映会</span></div></footer><script src="../assets/site.js" defer></script></body></html>'''
(FILMS/'minna-screenings.html').write_text(screen_html,encoding='utf-8')

# FILMS listing: switch the external Wix link to internal official page.
films=(ROOT/'films.html').read_text(encoding='utf-8')
films=re.sub(r'<a class="link" href="https://tinymousenet\.wixsite\.com/everyonesboat" target="_blank" rel="noopener">OFFICIAL SITE →</a>', '<a class="link" href="films/minna.html">OFFICIAL PAGE →</a>', films)
(ROOT/'films.html').write_text(films,encoding='utf-8')

# Sitemap: production pages only.
sm=ROOT/'sitemap.xml'; xml=sm.read_text(encoding='utf-8')
for url in ['https://tiny-mouse.net/films/minna.html','https://tiny-mouse.net/films/minna-screenings.html']:
    if url not in xml:
        xml=xml.replace('</urlset>',f'  <url><loc>{url}</loc><lastmod>2026-10-03</lastmod></url>\n</urlset>')
sm.write_text(xml,encoding='utf-8')
print('Minna migration completed')
