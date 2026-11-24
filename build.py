# 홈페이지 네 나라 말 만들기: src/index.html(한국어 원본) → index.html, en/, zh/, ja/
# 쓰는 법: python3 build.py
import re, os

SRC = open('src/index.html', encoding='utf-8').read()

LANGS = {
 'ko': dict(dir='', html='ko', label='한국어 <small>Korean</small>', logo_sub='', brand='조선 타이쿤',
   title='조선 타이쿤 · Joseon Tycoon',
   desc='초가 한 채에서, 팔도 제일의 고을로. 조선 시대 마을 건설 · 경영 시뮬레이션 — Steam 출시 예정.',
   ogdesc='초가 한 채에서, 팔도 제일의 고을로. Steam 출시 예정.'),
 'en': dict(dir='en', html='en', label='English', logo_sub='', brand='Joseon Tycoon',
   title='Joseon Tycoon · Joseon-era city builder',
   desc='From a single thatched hut to the finest town in the land. A village-building and management sim set in Joseon-era Korea — coming soon to Steam.',
   ogdesc='From a single thatched hut to the finest town in the land. Coming soon to Steam.'),
 'zh': dict(dir='zh', html='zh-Hans', label='简体中文 <small>Chinese</small>', logo_sub='', brand='朝鲜大亨',
   title='朝鲜大亨 Joseon Tycoon · 朝鲜时代城市建造',
   desc='从一间茅草屋，到八道第一的城镇。以朝鲜时代为背景的村落建设与经营模拟游戏，即将登陆 Steam。',
   ogdesc='从一间茅草屋，到八道第一的城镇。即将登陆 Steam。'),
 'ja': dict(dir='ja', html='ja', label='日本語 <small>Japanese</small>', logo_sub='', brand='朝鮮タイクーン',
   title='朝鮮タイクーン Joseon Tycoon · 朝鮮時代の街づくり',
   desc='一軒の藁葺き屋根から、八道一の町へ。朝鮮時代を舞台にした村づくり・経営シミュレーション。Steamで近日発売。',
   ogdesc='一軒の藁葺き屋根から、八道一の町へ。Steamで近日発売。'),
}

# 한국어 → (영어, 중국어, 일본어)
T = {
 '조선 타이쿤': ('Joseon Tycoon', '朝鲜大亨', '朝鮮タイクーン'),
 '트레일러': ('Trailer', '预告片', 'トレーラー'),
 '게임 소개': ('About', '游戏介绍', 'ゲーム紹介'),
 '스크린샷': ('Screenshots', '截图', 'スクリーンショット'),
 'Steam 찜하기': ('Wishlist', '加入愿望单', 'ウィッシュリスト'),
 'Steam 출시 예정': ('Coming soon to Steam', '即将登陆 Steam', 'Steamで近日発売'),
 'Steam 출시 예정 · 한국어 · English · 中文 · 日本語': ('Coming soon to Steam · 한국어 · English · 中文 · 日本語', '即将登陆 Steam · 한국어 · English · 中文 · 日本語', 'Steamで近日発売 · 한국어 · English · 中文 · 日本語'),
 '손수 일구는': ('Build it by hand —', '亲手打造', '自らの手で築く'),
 '나만의 조선 고을': ('your own Joseon town', '属于你的朝鲜城镇', '自分だけの朝鮮の町'),
 '조선시대': ('JoseonEra', '朝鲜时代', '朝鮮時代'),
 '시티빌더': ('CityBuilder', '城市建造', '街づくり'),
 '픽셀아트': ('PixelArt', '像素风', 'ドット絵'),
 '힐링경영': ('CozyManagement', '治愈经营', 'まったり経営'),
 '조선 시대 시티빌더': ('Joseon-era city builder', '朝鲜时代城市建造', '朝鮮時代の街づくり'),
 'Steam에서 찜하기': ('Wishlist on Steam', '在 Steam 加入愿望单', 'Steamでウィッシュリスト'),
 '트레일러 보기': ('Watch trailer', '观看预告片', 'トレーラーを見る'),
 '내려 보기': ('Scroll', '向下浏览', 'スクロール'),
 '해 질 녘 굴뚝마다': ('At dusk, from every chimney', '黄昏时分，家家户户', '夕暮れ、どの煙突からも'),
 '연기가 오르면': ('the smoke begins to rise', '炊烟袅袅升起', '煙が立ちのぼれば'),
 '소리 켜고 처음부터': ('Sound on, from the start', '开启声音从头播放', '音声ありで最初から'),
 '초가 한 채에서,': ('From a single thatched hut', '从一间茅草屋，', '一軒の藁葺き屋根から、'),
 '팔도 제일의 고을로': ('to the finest town in the land', '到八道第一的城镇', '八道一の町へ'),
 '조선 시대 고을을 일구는 마을 건설 · 경영 시뮬레이션. 길을 내고 백성을 불러 일터를 세우면, 고을이 눈앞에서 살아 움직여요.':
   ('A village-building and management sim set in Joseon-era Korea. Lay roads, invite settlers and raise workplaces — and watch your town come alive before your eyes.',
    '以朝鲜时代为背景的村落建设与经营模拟游戏。修路、招来百姓、建起作坊，城镇就会在你眼前生机勃勃地运转起来。',
    '朝鮮時代を舞台にした村づくり・経営シミュレーション。道を敷き、民を呼び、仕事場を建てれば、町が目の前で生き生きと動き出します。'),
 '초가 한 채에서 시작해요': ('Start with one thatched hut', '从一间茅草屋开始', '藁葺き一軒からはじまる'),
 '길을 내고 백성을 부르면, 빈 들판이 고을로 자라요.': ('Lay a road and call in settlers — an empty field grows into a town.', '修好道路、招来百姓，空旷的田野会慢慢长成城镇。', '道を敷いて民を呼べば、何もない野原が町へと育ちます。'),
 '누구에게나 하루가 있어요': ('Everyone has a day to live', '每个人都有自己的一天', '誰にでも一日がある'),
 '일터로 가는 백성, 서당에 가는 양반, 구경 온 나그네까지.': ('Commoners off to work, yangban to the village school, travelers in to sightsee.', '去上工的百姓、去书堂的两班，还有来观光的旅人。', '仕事場へ向かう民、書堂へ通う両班、見物に来た旅人まで。'),
 '고을마다 숨은 상징 건축': ('A hidden landmark in every town', '每座城镇都藏着地标建筑', '町ごとに隠された名所建築'),
 '장이 넘어갈 때마다 새 고을과 새 이야기가 열려요.': ('Each new chapter opens a new town and a new story.', '每翻开新的一章，就会开启新的城镇与新的故事。', '章が進むたびに、新しい町と新しい物語が開きます。'),
 '초가집': ('Thatched house', '茅草屋', '藁葺きの家'),
 '주막': ('Tavern', '酒幕', '酒幕'),
 '벌목장': ('Logging camp', '伐木场', '伐採場'),
 '어장': ('Fishery', '渔场', '漁場'),
 '막새 가마': ('Roof-tile kiln', '瓦当窑', '瓦窯'),
 '여관': ('Inn', '客栈', '旅籠'),
 '실학당': ('Silhak academy', '实学堂', '実学堂'),
 '양반가': ('Yangban house', '两班宅邸', '両班の屋敷'),
 '정자': ('Pavilion', '亭子', '東屋'),
 '장승': ('Jangseung totems', '长丞', 'チャンスン'),
 '교역소': ('Trading post', '交易所', '交易所'),
 '석탑': ('Stone pagoda', '石塔', '石塔'),
 '도움말 없이도 보이는 살림': ('See every craft at work', '一眼看懂的日常', '説明いらずの暮らし'),
 '베고, 나르고, 만드는 모든 공정이 화면 위에서 그대로 보여요.': ('Every chop, haul and craft plays out right on screen.', '砍伐、搬运、制作——每道工序都在画面上真实呈现。', '伐る、運ぶ、作る。すべての工程が画面の上でそのまま見えます。'),
 '장인의 손끝에서 물건이 나고': ("Goods born of artisans' hands", '匠人手中造出百物', '職人の手から品が生まれ'),
 '생산 줄을 이어 백성과 양반의 집을 다섯 단계까지 키워요.': ('Link production chains and grow homes for commoners and yangban through five tiers.', '串起生产链，把百姓与两班的住宅升到第五阶。', '生産の流れをつなぎ、民と両班の家を五段階まで育てます。'),
 '불, 도둑, 왜구, 그리고 혹한기': ('Fire, thieves, pirates — and the deep freeze', '火灾、盗贼、倭寇，还有严冬', '火事、盗賊、倭寇、そして厳冬'),
 '교지와 재해를 이겨 내고 고을을 지켜요.': ('Fulfil royal decrees, weather disasters and keep your town standing.', '完成王命、战胜灾害，守护你的城镇。', '王命をこなし、災いを乗り越えて町を守ります。'),
 '고을 둘러보기': ('Tour the town', '城镇一览', '町を見て回る'),
 '곧 Steam에서 만나요': ('See you soon on Steam', '即将在 Steam 与你相见', 'まもなくSteamで'),
 '찜해 두시면 출시 날 알려 드려요.': ("Wishlist now and Steam will let you know on launch day.", '加入愿望单，发售当天 Steam 会通知你。', 'ウィッシュリストに入れておけば、発売日にお知らせが届きます。'),
 '유튜브 개발일지': ('Dev diary on YouTube', 'YouTube 开发日志', 'YouTube 開発日誌'),
 '디스코드': ('Discord', 'Discord', 'Discord'),
 '유튜브': ('YouTube', 'YouTube', 'YouTube'),
 '© 2026 Bamtee Studio · 조선 타이쿤 (Joseon Tycoon)': ('© 2026 Bamtee Studio · Joseon Tycoon (조선 타이쿤)', '© 2026 Bamtee Studio · 朝鲜大亨 (Joseon Tycoon)', '© 2026 Bamtee Studio · 朝鮮タイクーン (Joseon Tycoon)'),
 '조선 타이쿤 · 초가 한 채에서, 팔도 제일의 고을로': ('Joseon Tycoon — From a thatched cottage to Joseon’s finest town', '朝鲜大亨 — 从一间茅屋，到八道第一名邑', '朝鮮タイクーン — 一軒の草ぶき小屋から、八道一の町へ'),
 '아래로': ('Scroll down', '向下', '下へ'),
 '트레일러 재생': ('Play trailer', '播放预告片', 'トレーラーを再生'),
 '조선 타이쿤의 건물과 일꾼들': ('Buildings and people of Joseon Tycoon', '朝鲜大亨的建筑与人们', '朝鮮タイクーンの建物と人々'),
 '아직 비밀인 상징 건축': ('A landmark still under wraps', '尚未揭晓的地标建筑', 'まだ秘密の名所建築'),
 '일터마다 일꾼이 나무를 켜고 짐을 쌓는 모습': ('Workers sawing timber and stacking goods at every workplace', '各处作坊里工人锯木、堆货的景象', '仕事場ごとに職人が木を挽き、荷を積む様子'),
 '제련소 창과 생산 줄이 이어진 고을': ('A town linked by production chains, with the smelter window open', '打开冶炼所窗口、生产链相连的城镇', '製錬所の画面と生産の流れがつながった町'),
 '눈 덮인 혹한기의 강가 고을': ('A riverside town under snow in the deep freeze', '严冬时节白雪覆盖的河畔城镇', '厳冬の雪に覆われた川辺の町'),
 '기와집과 객사가 들어선 눈 내린 고을': ('A snowy town of tiled houses and a guesthouse', '瓦房与客舍林立的雪中城镇', '瓦屋根の家と客舎が並ぶ雪の町'),
 '강가에 교역소를 연 무역 고을': ('A trading town with a riverside trading post', '在河边开设交易所的贸易城镇', '川辺に交易所を開いた交易の町'),
 '눈 쌓인 기와지붕 가까이': ('Snow-covered tiled roofs, up close', '积雪瓦顶特写', '雪の積もった瓦屋根を近くで'),
 '바닷가에 길을 낸 초가 마을': ('A thatched village with roads along the coast', '沿海修路的茅草屋村落', '海辺に道を通した藁葺きの村'),
 '숲에 둘러싸인 고을 전경': ('A town surrounded by forest', '被森林环绕的城镇全景', '森に囲まれた町の全景'),
 '길을 따라 늘어선 첫 초가들': ('The first thatched huts lining the road', '沿路排开的第一批茅草屋', '道沿いに並ぶ最初の藁葺き屋根'),
 '스크린샷 크게 보기': ('Screenshot viewer', '截图大图', 'スクリーンショット拡大'),
 '닫기': ('Close', '关闭', '閉じる'),
 '이전 사진': ('Previous', '上一张', '前の写真'),
 '다음 사진': ('Next', '下一张', '次の写真'),
}
PREFIX = {'크게 보기: ': ('View larger: ', '查看大图：', '拡大表示：')}
IDX = {'en': 0, 'zh': 1, 'ja': 2}
FONTS = {
 'zh': '<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;600&amp;family=Noto+Serif+SC:wght@700&amp;display=swap" rel="stylesheet">',
 'ja': '<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;600&amp;family=Noto+Serif+JP:wght@700&amp;display=swap" rel="stylesheet">',
}
SITE = 'https://joseontycoon.com/'

def build(code):
    L = LANGS[code]; s = SRC
    up = '../' if L['dir'] else ''
    # 머리
    s = s.replace('<html lang="ko">', f'<html lang="{L["html"]}">', 1)
    s = re.sub(r'<title>.*?</title>', f'<title>{L["title"]}</title>', s, count=1)
    s = re.sub(r'(<meta name="description" content=")[^"]*', lambda m: m.group(1) + L['desc'], s, count=1)
    s = re.sub(r'(<meta property="og:title" content=")[^"]*', lambda m: m.group(1) + L['title'], s, count=1)
    s = re.sub(r'(<meta property="og:description" content=")[^"]*', lambda m: m.group(1) + L['ogdesc'], s, count=1)
    alt = ''.join(f'<link rel="alternate" hreflang="{LANGS[c]["html"]}" href="{SITE}{LANGS[c]["dir"] + "/" if LANGS[c]["dir"] else ""}">\n' for c in LANGS)
    alt += f'<link rel="alternate" hreflang="x-default" href="{SITE}">\n<link rel="canonical" href="{SITE}{L["dir"] + "/" if L["dir"] else ""}">\n'
    s = s.replace('</head>', alt + FONTS.get(code, '') + '\n</head>', 1)
    # 말 바꾸기 (본문, 스크립트 앞까지만)
    cut = s.index('<script>', s.index('<body'))
    head, body, tail = s[:s.index('<body')], s[s.index('<body'):cut], s[cut:]
    body = body.replace('{{LANG_LABEL}}', L['label'])
    if code != 'ko':
        i = IDX[code]
        for k, vs in PREFIX.items():
            body = re.sub('="' + re.escape(k) + '([^"]*)"', lambda m: '="' + vs[i] + T.get(m.group(1), (m.group(1),)*3)[i] + '"', body)
        for k in sorted(T, key=len, reverse=True):
            v = T[k][i]
            body = re.sub(r'>(\s*)' + re.escape(k) + r'(\s*)<', lambda m: '>' + m.group(1) + v + m.group(2) + '<', body)
            body = body.replace('="' + k + '"', '="' + v + '"')
        for k, vs in PREFIX.items():
            body = body.replace('="' + k, '="' + vs[i])
    body = body.replace('{{LOGO_SUB}}', L['logo_sub'])
    for c in LANGS:
        href = up + (LANGS[c]['dir'] + '/' if LANGS[c]['dir'] else '')
        body = body.replace('{{L_' + c + '}}', href or './')
    body = body.replace(f'data-l="{code}"', f'data-l="{code}" aria-current="page"')
    s = head + body + tail
    if code != 'ko':
        s = s.replace('assets/logo.png', f'assets/logo-{code}.png')
    here = code
    root = up or './'
    redir = ("<script>(function(){try{if(localStorage.getItem('jt-lang')||/bot|crawl|spider|slurp|facebookexternalhit|preview/i.test(navigator.userAgent))return;"
             "var ls=(navigator.languages&&navigator.languages.length?navigator.languages:[navigator.language||'']);var l=(ls[0]||'').toLowerCase();if(!l)return;"
             "var t=l.indexOf('ko')===0?'ko':l.indexOf('zh')===0?'zh':l.indexOf('ja')===0?'ja':'en';if(t==='" + here + "')return;"
             "location.replace('" + root + "'+(t==='ko'?'':t+'/')+location.hash);}catch(e){}})();</script>\n")
    s = s.replace('</head>', redir + '</head>', 1)
    if up:
        s = re.sub(r'(?<![\w./])assets/', up + 'assets/', s)
    # 남은 한글 검사 (한국어 본문 외)
    if code != 'ko':
        b2 = s[s.index('<body'):s.index('<script>', s.index('<body'))]
        left = [t for t in re.findall(r'>([^<>]*[가-힣][^<>]*)<|="([^"]*[가-힣][^"]*)"', b2)]
        left = [a or b for a, b in left if (a or b).strip() not in ('조선', '타이쿤', '한국어', '[문의 이메일]', '한국어 · English · 中文 · 日本語', '한국어 ', 'Coming soon to Steam · 한국어 · English · 中文 · 日本語', '即将登陆 Steam · 한국어 · English · 中文 · 日本語', 'Steamで近日発売 · 한국어 · English · 中文 · 日本語') and '(조선 타이쿤)' not in (a or b)]
        if left: print(code, '한글 남음:', left)
    out = (L['dir'] + '/' if L['dir'] else '') + 'index.html'
    os.makedirs(os.path.dirname(out) or '.', exist_ok=True)
    open(out, 'w', encoding='utf-8').write(s)
    print('만듦', out)

for c in LANGS: build(c)
