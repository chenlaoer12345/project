import lxml.html
import requests
from bs4 import BeautifulSoup

def wuma_image_empty_dict():
    keys = [
        "full_sample"
    ]
    meta_dict = {key: "" for key in keys}
    return meta_dict

def empty_dict():
    """make a empty dict for task"""
    keys = [
        "stars",
        "star_e",
        "star_j",
        "star_c",
        "performer_cover_image_url",
        "company",
        "company_name_e",
        "company_name_c",
        # "company_name_j",
        "genres",
        "code",
        "series",
        "series_description",
        "movie_length",
        "released_date",
        "type",
        "type_e",
        "movie_small_sample_img",
        "movie_sample_img",
        "movie_sample_video_poster",
        "title",
        "title_e",
        "movie_sample_video_url",
        "avgle_embedded_url",
        "magnet_dict",
        "full_sample",
        "embedded_url",
        # "movie_sample_img_321",
        # "movie_small_sample_img_321"
        #            "magnet_name",
        #            "magnet_time",
        #            "magnet_file_size"
    ]
    meta_dict = {key: "" for key in keys}
    return meta_dict


def lxml_page(html):
    """make requested html become xpath object
       return: xpath selector
    """
    selector = lxml.html.fromstring(html)
    return selector


genre_data_e = [{'Theme': ['Affair', 'Asian', 'Bath', 'Beauty Shop', 'Bizarre', 'Busty Fetish', 'Conceived', 'Couple',
                           'Cruel Expression', 'Cuckold', 'Dance', 'Dark System', 'Dead Drunk', 'Delusion', 'Eros',
                           'Evil', 'Fan Appreciation', 'Fetish', 'France', 'Friendship', 'Futanari', 'Gay',
                           'Image Club', 'Incest', 'Korean', 'Leg Fetish', 'Lesbian', 'Lesbian Kiss', 'Molester',
                           'Nampa', 'Nasty, Hardcore', 'Normal', 'Nude', 'Other Fetish', 'Peeping', 'Planning', 'Prank',
                           'Rape', 'Reserved Role', 'School Stuff', 'Sexy', 'Shotacon', 'Slave', 'Sport',
                           'Submissive Men', 'Sweat', 'Talent', 'Tentacle', 'Time Stop', 'Topic Work', 'Tsundere',
                           'Virgin', 'Virgin Man', 'Voyeur', 'Youth']}, {
                    'Character': ['Anchorwoman', 'Beautiful Girl', 'Black Actor', 'Booth Girl', 'Bride, Young Wife',
                                  'Bus Guide', 'Childhood Friend', 'Companion', 'Cosplayers', 'Daughter', 'Entertainer',
                                  'College Students', 'Female Teacher', 'Fighters', 'Freeter', 'Gal', 'Hostesses',
                                  'Idol', 'Instructor', 'Landlady, Hostess', 'Look-alike', 'Married Woman', 'Miss',
                                  'Model', 'Mother', 'Stepmother', 'Nurse', 'Older Sister', 'Other Asian',
                                  'Other Students', 'Princess', 'Prostitutes', 'Race Queen', 'School Girls',
                                  'Secretary', 'Sister', 'Slut', 'Tutor', 'Various Professions', 'Waitress',
                                  'White Actress', 'Widow', 'Female Doctor', 'Female Investigator', 'Young Gals']}, {
                    'Costume': ['Anime Characters', 'Blazer', 'Bloomers', 'Body Conscious', 'Bunny Girl', 'Catgirl',
                                'Cheongsam', 'Cosplay', 'Cosplay Costumes', 'Cross Dressing', 'Doll', 'Erotic Wear',
                                'Female Ninja', 'Female Warrior', 'Glasses', 'Hat Type', 'Kimono, Mourning',
                                'Knee Socks', 'Leotard', 'Lingerie', 'Lolita Cosplay', 'Loose Socks', 'Maid',
                                'Mini Skirt', 'Mini Skirt Police', 'Miniskirt', 'Naked Apron', 'Nun', 'OL', 'Pantyhose',
                                'Priestess', 'Sailor Suit', 'School Swimsuit', 'School Uniform', 'Stewardess',
                                'Swimsuit', 'Underwear', 'Uniform', 'Yukata']}, {
                    'Body Type': ['BBW', 'Big Tits', 'Breasts', 'Butt', 'Huge Butt', 'Lolita', 'Mature Woman', 'Mini',
                                  'Muscle', 'Pregnant Woman', 'Shaved', 'Slender', 'Sun tan', 'Tall', 'Tits',
                                  'Transsexual', 'Ultra-Huge Tits']}, {
                    'Sex Acts': ['69', '3p, 4p', 'Anal', 'Blow', 'Breast Milk', 'Bukkake', 'Coprophagy', 'Cowgirl',
                                 'Creampie', 'Cum', 'Cunnilingus', 'Deep Throating', 'Defecation', 'Dirty Words',
                                 'Facesitting', 'Facials', 'Finger Fuck', 'Fisting', 'Footjob', 'Handjob', 'Kiss',
                                 'Massage', 'Masturbation', 'Piss Drinking', 'Promiscuity', 'Shower', 'Squirting',
                                 'Titty Fuck', 'Urination']}, {
                    'Sex Plays': ['Abuse', 'Bondage', 'Car Sex', 'Cervix', 'Confinement', 'Drug', 'Egg Vibrator',
                                  'Electric Massager', 'Enema', 'Exposure', 'Foreign Objects', 'Gangbang',
                                  'Humiliation', 'Hypnosis', 'Impromptu Sex', 'Lotion', 'Outdoors', 'Rape', 'Restraint',
                                  'Restraints', 'Scatology', 'SM', 'Speculum', 'Toy', 'Training', 'Undressing',
                                  'Urethral Cathing', 'Vibe']}, {
                    'Genre': ['3D', '4HR+', 'Action', 'Adult Anime', 'Adult Movie', 'Adventure', 'Amateur',
                              'Best, Omnibus', 'Chroma Key', 'Classic', 'Close Up', 'Comedy', 'Culture', 'Debut',
                              'Debut Production', 'Digital Mosaic', 'Documentary', 'Drama', 'Fighting Action',
                              'For Women', 'Girl Movie', 'Gravure', 'Historical Play', 'Hobby, Culture', 'Horror',
                              'How To', 'Image Video', 'Independents', 'Interview', 'Love', 'Love Romance',
                              'Love Story', 'Male', 'Multiple Story', 'Omnibus', 'Original Collaboration',
                              'Oversea Import', 'Overseas', 'Parody', 'POV', 'Psycho, Thriller', 'R-15', 'R-18',
                              'Reprinted Edition', 'Risky Mosaic', 'Sensuality', 'SF', 'Simulation', 'Solowork',
                              'Special Effects', 'Subjectivity', 'Suspense', 'Touch Typing', 'US/EU Porn',
                              'User Submission', 'VR']}, {'Media': ['Blu-ray', 'HD DVD', 'MicroSD', 'UMD', 'VHS']}]
genre_data_j = [{'主題': ['不倫', 'アジア', 'お風呂', 'エステ', '猟奇', '巨乳フェチ', '孕ませ', 'カップル', '残虐表現', '寝取り、寝取られ', 'ダンス', 'ダーク系',
                        '泥酔', '妄想', 'エロス', '鬼畜系', 'ファン感謝・訪問', 'フェチ', 'フランス', '友情', 'ふたなり', 'ゲイ', 'イメクラ', '近親相姦', '韓国',
                        '脚フェチ', 'レズ', 'レズキス', '痴漢', 'ナンパ', '淫乱、ハード系', 'ノーマル', '全裸', 'その他フェチ', '覗き', '企画', 'イタズラ', 'レイプ',
                        '逆ナン', '学園もの', 'セクシー', 'ショタ', '奴隷', 'スポーツ', 'M男', '汗だく', 'タレント', '触手', '時間停止', '話題作', 'ツンデレ',
                        '処女', '童貞', '盗撮', '青春']}, {
                    'キャラクター': ['女子アナ', '美少女', '黒人男優', 'キャンギャル', '花嫁、若妻', 'バスガイド', '幼なじみ', 'コンパニオン', 'コスプレイヤー', '令嬢',
                               '芸能人', '女子大生', '女教師', '格闘家', 'フリーター', 'ギャル', 'キャバ嬢', 'アイドル', 'インストラクター', '女将、女主人',
                               'そっくりさん', '人妻', 'お嬢様', 'モデル', 'お母さん', '義母', '看護婦', 'お姉さん', 'アジア女優', 'その他学生', 'お姫様',
                               '風俗嬢', 'レースクィーン', '女子校生', '秘書', '妹', '痴女', '家庭教師', '職業色々', 'ウェイトレス', '白人女優', '未亡人', '女医',
                               '女捜査官', 'コギャル']}, {
                    'コスチューム': ['アニメキャラクター', 'ブレザー', 'ブルマ', 'ボディコン', 'バニーガール', 'ネコミミ', 'チャイナドレス', 'コスプレ', 'コスプレ衣装',
                               '女装・男の娘', 'ドール', '着エロ', 'くノ一', '女戦士', 'めがね', 'ハットタイプ', '和服、喪服', 'ニーソックス', 'レオタード',
                               'ランジェリー', 'ゴスロリ', 'ルーズソックス', 'メイド', 'ミニスカ', 'ミニスカポリス', 'ミニスカート', '裸エプロン', 'シスター', 'OL',
                               'パンスト', '巫女', 'セーラー服', 'スクール水着', '学生服', 'スチュワーデス', '水着', 'パンチラ', '制服', '浴衣']}, {
                    'ボディタイプ': ['ぽっちゃり', '巨乳', '美乳', '尻フェチ', '巨尻', 'ロリ系', '熟女', 'ミニ系', '筋肉', '妊婦', 'パイパン', 'スレンダー',
                               '日焼け', '長身', '微乳', 'ニューハーフ', '超乳']}, {
                    'セックス行為': ['シックスナイン', '3P、4P', 'アナル', 'フェラ', '母乳', 'ぶっかけ', '食糞', '騎乗位', '中出し', 'ごっくん', 'クンニ',
                               'イラマチオ', '脱糞', '淫語', '顔面騎乗', '顔射', '指マン', 'フィスト', '足コキ', '手コキ', 'キス・接吻', 'マッサージ', 'オナニー',
                               '飲尿', '乱交', 'シャワー', '潮吹き', 'パイズリ', '放尿']}, {
                    'セックスプレイ': ['凌辱', 'ボンテージ', 'カーセックス', 'ポルチオ', '監禁', 'ドラッグ', 'ローター', '電マ', '浣腸', '露出', '異物挿入', '輪姦',
                                '羞恥', '催眠', '即ハメ', 'ローション', '野外', '強姦', '拘束', '縛り', 'スカトロ', 'SM', 'クスコ', 'おもちゃ', '調教',
                                '脱衣', '尿道カテーテル', 'バイブ']}, {
                    'ジャンル': ['3D', '4時間以上作品', 'アクション', 'アダルトアニメ', '成人向け映画', 'アドベンチャー', '素人', 'ベスト、総集編', 'クロマキー',
                             'クラシック', '局部アップ', 'コメディー', 'カルチャー', 'デビュー作', 'デビュー作品', 'デジモ', 'ドキュメント', 'ドラマ', 'アクション格闘',
                             '女性向け', '美少女ムービー', 'グラビア', '時代劇', '趣味、教養', 'ホラー', 'How To', 'イメージビデオ', 'インディーズ', 'インタビュー',
                             '恋愛', 'ラブロマンス', 'ラブストーリー', '男性', '複数話', 'オムニバス', '原作コラボ', '海外輸入', '海外', 'パロディ', 'ハメ撮り',
                             'サイコ、スリラー', 'R-15', 'R-18', '復刻版', 'ギリモザ', '官能作品', 'SF', 'シミュレーション', '単体作品', '特撮', '主観',
                             'サスペンス', 'タッチタイピング', '洋ピン', '投稿', 'VR']},
                {'メディア': ['Blu-ray（ブルーレイ）', 'HD DVD', 'microSD', 'UMD', 'VHS']}]
genre_data_c = [{'主题': ['出轨', '亚洲', '洗澡', '美容院', '奇异的', '恋乳癖', '受孕', '情侣', '残忍画面', '白天出轨', '跳舞', '暗黑系', '烂醉如泥的', '妄想',
                        '性爱', '魔鬼系', '粉丝感谢', '恋物癖', '法国', '友谊', '双性人', '男同性恋', '形象俱乐部', '乱伦', '韩国', '恋腿癖', '女同性恋',
                        '女同接吻', '性骚扰', '猎艳', '淫乱、真实', '正常', '全裸', '其他恋物癖', '偷窥', '企画', '恶作剧', '强奸', '倒追', '学校作品', '性感的',
                        '正太控', '奴隶', '运动', 'M男', '流汗', '天赋', '触手', '时间停止', '主题工作', '蛮横娇羞', '处女', '处男', '偷窥', '青年']}, {
                    '角色': ['女主播', '美少女', '黑人演员', '展场女孩', '新娘、年轻妻子', '车掌小姐', '童年朋友', '伴侣', '角色扮演者', '女儿', '艺人', '女大学生',
                           '女教师', '格斗家', '飞特族', '辣妹', '礼仪小姐', '偶像', '讲师', '老板娘、女主人', '明星脸', '已婚妇女', '大小姐', '模特儿', '母亲',
                           '后母', '护士', '姐姐', '亚洲女演员', '其他学生', '公主', '妓女', '赛车女郎', '高中女生', '秘书', '妹妹', '荡妇', '家教',
                           '各种职业', '服务生', '白人', '寡妇', '女医生', '女检察官', '年轻女孩']}, {
                    '服装': ['动画人物', '制服外套', '运动短裤', '身体意识', '兔女郎', '猫耳女', '旗袍', '角色扮演', 'COSPLAY服饰', '女装人妖', '娃娃',
                           '猥亵穿着', '女忍者', '女战士', '眼镜', '帽型', '和服、丧服', '及膝袜', '紧身衣', '内衣', '萝莉角色扮演', '泡泡袜', '女佣', '迷你裙',
                           '迷你裙警察', '超短裙', '裸体围裙', '修女', 'OL', '连裤袜', '女祭司', '水手服', '学校泳装', '校服', '空中小姐', '泳装', '内衣',
                           '制服', '浴衣']}, {
                    '体型': ['胖女人', '巨乳', '乳房', '屁股', '巨大屁股', '萝莉塔', '成熟的女人', '瘦小身型', '肌肉', '孕妇', '无毛', '苗条', '晒黑', '高',
                           '平胸', '变性者', '超乳']}, {
                    '行为': ['69', '多P', '肛交', '口交', '母乳', '颜射', '食粪', '女上位', '中出', '吞精', '舔阴', '深喉', '排便', '淫语', '颜面骑乘',
                           '颜射', '手指插入', '拳交', '足交', '打手枪', '接吻', '按摩', '自慰', '饮尿', '滥交', '淋浴', '潮吹', '乳交', '放尿']}, {
                    '玩法': ['凌辱', '紧缚', '汽车性爱', '子宫颈', '监禁', '药物', '跳蛋', '女优按摩棒', '灌肠', '露出', '插入异物', '轮奸', '羞耻', '催眠',
                           '即兴性交', '乳液', '户外', '强奸', '拘束', '捆绑', '粪便', 'SM', '鸭嘴', '玩具', '调教', '脱衣', '导尿', '按摩棒']}, {
                    '类别': ['3D', '4小时以上作品', '行动', '成人动漫', '成人电影', '冒险', '业余', '精选、综合', '去背影片', '经典', '局部特写', '喜剧', '文化',
                           '首次亮相', '首次亮相', '数位马赛克', '纪录片', '戏剧', '战斗行动', '给女性观众', '美少女电影', '写真偶像', '历史剧', '爱好、文化', '恐怖',
                           '教学', '介绍影片', '独立制作', '访问', '恋爱', '爱情浪漫', '爱情故事', '男性', '故事集', '综合短篇', '原作改编', '国外进口', '海外',
                           '滑稽模仿', '第一人称摄影', '心理、惊悚片', 'R-15', 'R-18', '重印版', '薄马赛克', '感官作品', '科幻', '模拟', '单体作品', '特效',
                           '主观视角', '悬疑', '触摸打字', '西洋片', '投稿', 'VR']}, {'媒体': ['蓝光', 'HD DVD', 'MicroSD', 'UMD', 'VHS']}]


def get_genre_type(genre):
    genre_data = {"genre_c": genre,
                  "genre_type_c": "无分类",
                  "genre_type_j": "分類なし",
                  "genre_type_e": "No classification",
                  "genre_e": "",
                  "genre_j": "",
                  }
    for e, j, c in zip(genre_data_e, genre_data_j, genre_data_c):
        for (k, v), (f, r), (i, g) in zip(e.items(), j.items(), c.items()):
            for a, b, d in zip(v, r, g):
                # for chinese
                if d == genre:
                    genre_data["genre_e"] = a
                    genre_data["genre_j"] = b
                    genre_data["genre_c"] = d
                    genre_data["genre_type_c"] = i
                    genre_data["genre_type_j"] = f
                    genre_data["genre_type_e"] = k
                # for japanese
                if b == genre:
                    genre_data["genre_e"] = a
                    genre_data["genre_j"] = b
                    genre_data["genre_c"] = d
                    genre_data["genre_type_c"] = i
                    genre_data["genre_type_j"] = f
                    genre_data["genre_type_e"] = k
                # for english
                if a == genre:
                    genre_data["genre_e"] = a
                    genre_data["genre_j"] = b
                    genre_data["genre_c"] = d
                    genre_data["genre_type_c"] = i
                    genre_data["genre_type_j"] = f
                    genre_data["genre_type_e"] = k
    return genre_data


def get_different_type(movie_type):
    type_e = ""
    if movie_type == '有码':
        type_e = "Censored"
    if movie_type == str('无码'):
        type_e = 'Uncensored'
    return type_e


def parse_url(url, headers):
    page = requests.get(url, headers=headers)
    if page.status_code == 404:
        print("-----------------code not found in this website-----------------------")
        return None
    soup = BeautifulSoup(page.content.decode(), 'lxml')
    return soup












