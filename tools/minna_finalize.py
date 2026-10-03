from pathlib import Path
import re
from bs4 import BeautifulSoup, NavigableString

ROOT=Path(__file__).resolve().parents[1]
FILMS=ROOT/'films'

# ---------- Main film page ----------
p=FILMS/'minna.html'
soup=BeautifulSoup(p.read_text(encoding='utf-8'),'html.parser')

# Remove zero-width characters imported from Wix.
for node in list(soup.find_all(string=True)):
    if isinstance(node, NavigableString):
        cleaned=re.sub(r'[\u200b\u200c\u200d\ufeff]','',str(node))
        if cleaned != str(node): node.replace_with(cleaned)
for tag in list(soup.find_all(['p','div'])):
    if tag.name=='p' and not tag.get_text(strip=True) and not tag.find(): tag.decompose()

# Story: keep approved opening and restore Wix copy.
story=soup.find('section',id='story')
if story:
    copy=story.select_one('.minna-copy')
    if copy:
        copy.clear()
        lead=soup.new_tag('p'); lead['class']=['minna-lead']
        lead.append('「みんなが笑顔で乗れる舟を作ろう」'); lead.append(soup.new_tag('br'))
        lead.append('——縄文大工・雨宮国広が挑んだのは、石おのだけで樹齢250年の杉から巨大な丸木舟を生み出すこと。')
        copy.append(lead)
        for t in [
            '丸木舟を作る為に頂く命は樹齢250年の杉。',
            'モノが溢れる時代に、敢えて原始に還り行動する意味とは。そこまでして頂く命に向き合う心とは。',
            '祖先が辿ったであろう世界を現代に蘇らせることで、初めて感じることができる、人類が忘れてしまった「何か」。',
            'そんな「Jomonさんがやってきた！プロジェクト」を2年以上に渡り追いかけるドキュメント映画。'
        ]:
            q=soup.new_tag('p'); q.string=t; copy.append(q)

# AIFF review: restore the full excerpt shown on the Wix page.
featured=soup.select_one('.voice-card.featured blockquote')
if featured:
    featured.clear()
    featured.append('スピード、近道、そして即時の満足感に囚われた時代に、この映画は瞑想のように感じられる。')
    featured.append(soup.new_tag('br')); featured.append(soup.new_tag('br'))
    featured.append('― 中略 ―')
    featured.append(soup.new_tag('br')); featured.append(soup.new_tag('br'))
    featured.append('まるで時の流れがゆっくりと進み、世界がデジタルの鼓動ではなく、人間の鼓動に再び同期していくかのような感覚に襲われる。')

# Project: restore original explanatory copy.
project=soup.find('section',id='project')
if project:
    copy=project.select_one('.minna-copy')
    if copy:
        copy.clear()
        for t in [
            '原始の知恵と道具を用いて、全国の子供たちと一緒に日本を一周するための巨大な丸木舟を作ろう、というプロジェクト。',
            'Part1・杉の木を伐る、Part2・全国を回って皆で丸木舟を作る、Part3・丸木舟に乗るという全3部構成で2021年から開始。',
            '参加する子供たちは自らの手で石おのを作り、巨大な杉の木と向き合う中で様々なことを考え、感じることをテーマに掲げ、活動する。',
            'プロジェクトの原資はクラウドファンディングで集められている。'
        ]:
            q=soup.new_tag('p'); q.string=t; copy.append(q)

# Director profile: restore Wix bio while keeping link to the current About page.
dir_sec=None
for eye in soup.select('.eyebrow'):
    if eye.get_text(strip=True)=='Director / Music':
        dir_sec=eye.find_parent('section'); break
if dir_sec:
    copy=dir_sec.select_one('.minna-copy')
    if copy:
        copy.clear()
        for t in [
            '1981年、兵庫県生まれ。21歳の時、作曲家になると言いだし、大学中退。27歳で編曲家としてスタート。',
            '作曲、音楽学校講師等を経て、31歳で写真・映像撮影も業務として開始。規模は小さくても作れるものがある、との思いから、屋号をTiny Mouse Factoryと名付ける。',
            '2019年「3万年前の航海 徹底再現プロジェクト」では映画・VRコンテンツ・TV番組の撮影クルーとして同行。ここでJomonさんと出会う。',
            '主な業務は国立公園や自治体PV、企業用映像、MV等の撮影、編集。全国を動き回る傍ら、BGM制作等も並行して行っている。',
            '自らが出演するポッドキャスト「にしやま・メロンの創作休憩室」配信中。'
        ]:
            q=soup.new_tag('p'); q.string=t; copy.append(q)

# Rebuild the director comment cleanly. This prevents Wix hidden characters from
# merging the staff credits into the comment block.
comment=soup.select_one('.director-comment')
if comment:
    comment.clear()
    e=soup.new_tag('div'); e['class']=['eyebrow']; e.string="Director's Comment"; comment.append(e)
    h=soup.new_tag('h3'); h.string='監督のコメント'; comment.append(h)
    paras=[
        '電動工具も鉄製道具も使わないで、「石おの」だけで丸木舟を作る映画。',
        'この映画を何度も観ていると、ふと「これは歩いて廻るお遍路さんのようだ」と思うようになりました。電車も自動車もバスも自転車も使わない。何なら住んでいる場所から一番札所まですら歩いていくような感覚。',
        '文明の利器をフル活用すれば、お遍路さんはたぶん1週間もかからず終えられるでしょう。歩いたら何か月、いや年単位でかかるかもしれません。それを敢えてやる意味…',
        'それは、「遅いからこそ見える世界がある」ということなんじゃないでしょうか。歩みの鈍いカメだからこそ見える世界。足元の草花を眺め、遠くの山が少しずつ近づいてきて、その向こうに青い海が見え、町の人々と話し、時に立ち止まって振り返る。あっという間に通り過ぎては出会うことのない世界。それをじっくり噛みしめながら、ゆっくりでもよいという気持ちで歩く。',
        '「早ければ早いほど良い」「楽ができるなら楽がしたい」というのは、人の性のひとつでしょう。僕もそうです。でももし、「ゆっくりでもよい」と自分で自分を解放することができたなら、きっと全く違う気付きと哲学が心に浮かぶことでしょう。',
        '名前がイメージとして強すぎるので誤解されがちですが（笑）、彼は決して考古学的に正確な縄文人／文化を追及・模倣するわけでもなく、ファッションとして原始人をやっているわけでもありません。ただ現代において、石おのの「歩みの遅い素晴らしさ」に気付いただけなんです。',
        '縄文大工・雨宮国広はチェーンソーを扱うログハウスビルダーからキャリアをスタートし、鉄の手道具（手斧、鉞など）を経由して石おのにたどり着きました。そう、彼はしっかり現代の利器の持つ力を知っている「現代人の職人」なのです。それがゆえに彼は現代社会と自分の理想のギャップに苦しむ毎日を何年も何年も送ることになります。',
        'しっかり彼自身の足で歩んだからこそ見えた「彼の思う世界」と「現代社会」とのズレを、一体どうすればいいのかと悩み、そしてこんなとんでもなく巨大なプロジェクトを、最初は一人で実行したわけです。それがこの「Jomonさんがやってきた！プロジェクト」です。',
        'Jomonさんは映像としてプロジェクトの様子を残し、たくさんの方に命と人と地球のかかわり方を考えてもらうために、数多くの大手映像制作会社に企画を持ち込んだそうですが、全て断られてしまったそうです。2年以上に及ぶプロジェクトを映像で記録し、映像作品として完成させるということは、制作予算も巨大になります。制作会社も、やりたくても実行できなかったのかもしれません。',
        '僕ならなんとかできるかもしれないと思いました。大きな会社にできないなら、ちっぽけな個人事業主の出番だ、と。とりあえず機材と自分の身ひとつがあれば、なんとかなるだろう、と思ったわけです。気合で何とか出来るだろう、と。',
        'まずは自費で撮れるだけ撮って、記録できるだけ記録してみよう、と。例え場当たり的だと言われようと、無理に決まっていると言われても、なんとか続けて行こうと。相手は命あるもの。撮れずに通り過ぎてしまった時間はもう取り戻せないからです。',
        '制作決定から日数を経る毎に、僕一人の力がどれだけ微弱でひ弱なものか、よくわかりました。どれだけ支えてもらったのか、数え切れないほどの救いと助けが奇跡のように起きたのです。',
        'そう、僕もいつの間にか遅い遅い速度で、たくさんの人に背中を押してもらいながら、ゆっくりと歩き続けることができました。何度も「だめかもしれない」と思いました。悲しくなる日もありました。でも「やめたい」とは思いませんでした。「後押し」とは本当に強い力なんです。初めて知ることができました。',
        '何とか最後まで撮り切って、皆さんのところへお届けできることになりました。何度も頓挫する可能性のあった、個人の手に負えないとても大きなプロジェクトを映画としてお届けできる。これはたくさんの方々の力が成しえた奇跡なんです。',
        'これは本当にみんなで作った「みんなのふね」なのです。',
        'みんな、やったぜー！'
    ]
    for t in paras:
        q=soup.new_tag('p'); q.string=t; comment.append(q)
    sig=soup.new_tag('p'); sig['class']=['director-sign']; sig.string='監督　にしやまゆうき'; comment.append(sig)

# Remove any draft language in awards.
for q in soup.find_all('p'):
    if 'ドラフト' in q.get_text(): q.string='世界各地の映画祭にて受賞・公式選出されました。'

p.write_text(str(soup),encoding='utf-8')

# ---------- Past screenings page ----------
sp=FILMS/'minna-screenings.html'
s=BeautifulSoup(sp.read_text(encoding='utf-8'),'html.parser')
main=s.find('main')
for sec in main.find_all('section',class_='year'): sec.decompose()

events={
2026:[
('3月29日','加里屋まちづくり会館（兵庫県赤穂市）','主催: NPO法人赤穂里うみカヤックス'),
('3月15日','サイボウズ（株）松山オフィス（愛媛県松山市）','主催: マザーアースグリーンジャパン（MGJ）'),
('3月14日','中島 ゆうきの里（愛媛県松山市）','主催: マザーアースグリーンジャパン（MGJ）'),
('3月13日','大三島 OHANA in 御島（愛媛県今治市大三島町）','主催: マザーアースグリーンジャパン（MGJ）'),
('3月12日','久万高原町 まちなか交流館（愛媛県久万高原町）','主催: マザーアースグリーンジャパン（MGJ）'),
('3月7日','Jomonさんがやってきた！支援者の会（山梨県富士河口湖町）',''),
('2月7日','妙心寺（山梨県中央市）','主催: 個人様'),
('1月11日','すずめのお宿（大阪府千早赤阪村）','主催: 個人様')],
2025:[
('12月20日','東京都公文書館（東京都国分寺市）','主催: 多摩きた生活クラブ'),
('12月6・7日','HAMAYOUリゾート（山梨県富士河口湖町・ショート版）',''),
('11月29日','国立民族学博物館（大阪府吹田市・ショート版）',''),
('11月24日','東リ 伊丹ホール（伊丹市立文化会館）','主催: PRANAVA YOGA様'),
('11月8日','釈迦堂遺跡博物館',''),
('10月31日〜11月10日','シネまるむすび（岡山県総社市）','主催: 円◎結様'),
('9月21日','鳥取県立むきばんだ史跡公園',''),
('8月25日','東金中央コミュニティセンター（千葉県東金市）','主催: 二階シネマ様'),
('7月20日','二階シネマ（千葉県東金市）','主催: 二階シネマ様'),
('7月12日','ハカルAZUMINO（長野県安曇野市）','主催: 個人様 ※監督上映キャラバン'),
('6月25日','宮遺跡公園（長野県長野市）','主催: 個人様'),
('6月24日','パタゴニア白馬ストア（長野県白馬村）','主催: 個人様'),
('6月15日','ホっこりハウス（富山県小矢部市）','主催: 個人様'),
('5月23・24日','大菩薩の風ビエンナーレ（山梨県甲州市）','※監督上映キャラバン'),
('3月29日','佐賀地域交流センター（山口県平生町）','主催: ミンナ乗船クルー'),
('3月29日','あわくら会館（岡山県西粟倉村）','主催: あわくら会館・図書館 / 協力: 合同会社887'),
('3月27日','浜北さくら台病院（静岡県浜松市）','※デイサービスご利用者様向け上映会'),
('3月23日','呉YMCA（広島県呉市）','主催: えのきのはたけ郷原市民農園有限責任事業組合'),
('3月21日','都留文科大学','主催: つる環境マルシェ'),
('3月16日','和歌山県那智勝浦町','個人主催上映会'),
('3月8日','勝沼市民会館（山梨県甲州市）','主催: 甲州環境市民会議'),
('3月1日','東栄町体験交流館のき山学校','後援: 東栄町教育委員会 / 東栄町観光まちづくり協会'),
('2月9日','ゆめトピア長船（岡山県瀬戸内市）','主催: 瀬戸内市ボランティアチーム'),
('1月29日','みずもり 岡山店（岡山県新庄村）','主催: 888'),
('1月6・9日','kettle（東京都府中市・特別先行上映）','主催: タイニーマウスファクトリー')],
2024:[('12月7・8日','HAMAYOUリゾート（山梨県富士河口湖町）','初号試写 / 特別先行上映')]
}
for year in (2026,2025,2024):
    sec=s.new_tag('section'); sec['class']=['year']
    wrap=s.new_tag('div'); wrap['class']=['wrap']; sec.append(wrap)
    h=s.new_tag('h2'); h.string=str(year); wrap.append(h)
    lst=s.new_tag('div'); lst['class']=['screen-list']; wrap.append(lst)
    for date,place,note in events[year]:
        row=s.new_tag('div'); row['class']=['screen-row']
        d=s.new_tag('div'); d['class']=['screen-date']; d.string=date
        pl=s.new_tag('div'); pl['class']=['screen-place']; pl.append(place)
        if note:
            nn=s.new_tag('span'); nn['class']=['screen-note']; nn.string=' / '+note; pl.append(nn)
        row.append(d); row.append(pl); lst.append(row)
    main.append(sec)
sp.write_text(str(s),encoding='utf-8')
print('Minna pages finalized')
