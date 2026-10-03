from pathlib import Path
from bs4 import BeautifulSoup

ROOT=Path(__file__).resolve().parents[1]
p=ROOT/'films/minna.html'
s=BeautifulSoup(p.read_text(encoding='utf-8'),'html.parser')

def set_paras(container,texts):
    container.clear()
    for t in texts:
        q=s.new_tag('p'); q.string=t; container.append(q)

# Boat/origin copy from the original Wix site.
boat=None
for eye in s.select('.eyebrow'):
    if eye.get_text(strip=True)=='The Boat': boat=eye.find_parent('section'); break
if boat:
    copy=boat.select_one('.minna-copy')
    if copy:
        set_paras(copy,[
            '日本一周しながら沿岸ゴミを拾い続ける丸木舟『ミンナ』。無謀で果てしないように思える航海は何故始まったのか。そしてこの丸木舟はどのように生まれたのか。',
            'それは勢いや思いつきではない、果てしない試行錯誤の上で歩み続けた日々があったから。彼らがなぜこんなことをしているのか、この映画はその理由の「オリジン」をもう一度辿りなおすために存在します。'
        ])

# Screening information and director-talk plan from Wix, with contact routed to the shared form.
screen=s.find('section',id='screening')
if screen:
    copy=screen.select_one('.minna-copy')
    if copy:
        copy.clear()
        for t in [
            '本作の上映会を、誰でも主催者になれるサービス・cinemoで募集中！ご希望の方はcinemoサイトよりお申込みください。',
            'cinemoは社会問題解決に向けた映画配給を行うユナイテッドピープル株式会社が運営しています。',
        ]:
            q=s.new_tag('p'); q.string=t; copy.append(q)
        h=s.new_tag('h3'); h.string='監督トーク付上映会プラン'; copy.append(h)
        for t in [
            '監督自ら、映画上映後のトークイベントを行うことができます。',
            'Jomonさんが願うこと、撮影中に起きたこと、映画に込めた思い、お客様とのコミュニケーション等、様々なご要望に応えます。対談・独演など、ご希望のスタイルでお話します。',
            '実際に作成した石おのや杉の実物をお持ちして、映画の世界をより実感頂けます（杉の実物は壊れやすいため、車で運搬・移動できる範囲に限らせていただきます）。'
        ]:
            q=s.new_tag('p'); q.string=t; copy.append(q)
    actions=screen.select_one('.minna-actions')
    if actions:
        actions.clear()
        a=s.new_tag('a',href='https://www.cinemo.info/147j'); a['target']='_blank'; a['rel']='noopener'; a.string='cinemo 上映申込 →'; actions.append(a)
        a=s.new_tag('a',href='https://www.cinemo.info/cinemo.html'); a['target']='_blank'; a['rel']='noopener'; a.string='cinemoについて →'; actions.append(a)
        a=s.new_tag('a',href='../contact.html'); a.string='監督トーク・講演の相談 →'; actions.append(a)

# Home viewing: preserve the streaming note from Wix.
home=None
for eye in s.select('.eyebrow'):
    if eye.get_text(strip=True)=='Home Viewing': home=eye.find_parent('section'); break
if home:
    copy=home.select_one('.minna-copy')
    if copy:
        set_paras(copy,[
            'Blu-ray・DVD・パンフレットはTiny Mouse Factoryのオンラインストアで販売しています。',
            'オンライン配信については現在準備中です。今しばらくお待ちください。'
        ])

# Add podcast service links to the director profile, matching the old Wix information.
dir_sec=None
for eye in s.select('.eyebrow'):
    if eye.get_text(strip=True)=='Director / Music': dir_sec=eye.find_parent('section'); break
if dir_sec:
    actions=dir_sec.select_one('.minna-actions')
    if actions and not any('Spotify' in a.get_text() for a in actions.find_all('a')):
        links=[
            ('Spotify','https://open.spotify.com/show/033j9w4kNMvpdAADB5e2Hw'),
            ('Apple Podcast','https://podcasts.apple.com/jp/podcast/%E3%81%AB%E3%81%97%E3%82%84%E3%81%BE-%E3%83%A1%E3%83%AD%E3%83%B3%E3%81%AE%E5%89%B5%E4%BD%9C%E4%BC%91%E6%86%A9%E5%AE%A4-%E9%9B%91%E8%AB%87%E3%81%8B%E3%82%89%E7%94%9F%E3%81%BE%E3%82%8C%E3%82%8B%E5%89%B5%E4%BD%9C%E3%81%AE%E8%A9%B1/id1896805945'),
            ('Amazon Music','https://music.amazon.co.jp/podcasts/56dbdfcd-a360-470d-9c0c-4ed8e3b2bcfc/%E3%81%AB%E3%81%97%E3%82%84%E3%81%BE%E3%83%BB%E3%83%A1%E3%83%AD%E3%83%B3%E3%81%AE%E5%89%B5%E4%BD%9C%E4%BC%91%E6%86%A9%E5%AE%A4---%E9%9B%91%E8%AB%87%E3%81%8B%E3%82%89%E7%94%9F%E3%81%BE%E3%82%8C%E3%82%8B%E5%89%B5%E4%BD%9C%E3%81%AE%E8%A9%B1')]
        for label,url in links:
            a=s.new_tag('a',href=url); a['target']='_blank'; a['rel']='noopener'; a.string=label+' →'; actions.append(a)

p.write_text(str(s),encoding='utf-8')
print('polished')
