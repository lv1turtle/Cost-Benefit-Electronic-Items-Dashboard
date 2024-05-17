from preprocessor import Preprocessor
import pandas as pd
import re

def get_posts_with_ssd_type(posts_file):
    """
    m.2, sata 타입의 ssd 키워드들로 모든 핫딜 게시물에서 1차 필터링
    :param posts_file 모든 핫딜 게시물:
    :return m.2 혹은 sata 키워드를 제목에 갖고 있는 게시물 데이터프레임:
    """
    ssd_type = ['m.2', 'sata']
    posts = pd.DataFrame(columns=[
        'post_title', 'product_name', 'price', 'shop_type',
        'votes', 'views', 'created_at', 'components_of_computer'
    ])
    for keyword in ssd_type:
        preprocessor = Preprocessor(posts_file)
        processed = preprocessor.extract_rows_by_keyword_exactly(
            keyword=keyword, target_column='title',
            ignore_case_sensitive=True
        )
        for row in processed.itertuples():
            posts.loc[len(posts)] = [
                row.title, keyword, row.price, row.shop_type,
                row.votes, row.views, row.created_at, 'SSD'
            ]
        print(f"{keyword}")
    return posts



def delete_rows_ssd(ssd_file):
    """
    있어선 안될 키워드들을 포함하는 게시물 행을 삭제
    :param ssd_file: 'get_posts_with_ssd_type()'로 1차 필터링된 핫딜 게시물 파일:
    :return 2차 필터링된 핫딜 게시물 목록 데이터레임:
    """
    keywords = [
        '케이스', '본체', '라이젠', '3060', 'rx6600', 'b760m', 'x300 8tb', 'scs3a sata 카드',
        '5600g', '5600x', '블루레이', '중고', '12400f'
    ]
    df = pd.read_csv(ssd_file)
    df = df.drop(df.columns[0], axis=1)
    for keyword in keywords:
        idx = df[df['post_title'].str.lower().str.contains(keyword.lower())].index
        df = df.drop(idx)
    df = df.sort_values(by=['product_name'], ignore_index=True)
    return df

def get_ssd_posts_by_company(all_ssd_posts):
    """
    게시글로부터 얻어낸 ssd 제조사와 그와 관련된 키워드들을 통해 제조사별 게시글 csv 파일을 생성하여 저장
    제조사는 다나와 웹페이지로부터 가져옴
    :return:
    """
    companies = {
        '삼성': ['삼성', 'samsung', 'pm9a1', '970 evo'],
        'WD': ['wd', 'western digital', 'sn740'],
        '마이크론': ['마이크론', '크루셜', '크루시얼', 'crucial'],
        '기가바이트': ['기가바이트', 'gigabyte'],
        '킹스턴': ['킹스턴', '킹스톤', 'kingston'],
        'sk하이닉스': ['sk하이닉스', 'sk hynix', 'sk하이닉스', 'p41', 'p31'],
        'Netac':['Netac'],
        '씨게이트': ['씨게이트', '시게이트', 'seagate', '파이어쿠다', '바라쿠다'],
        '커세어': ['커세어', 'corsair'],
        '샌디스크': ['샌디스크', 'sandisk'],
        '에이서': ['에이서', 'acer'],
        'pny': ['pny'],
        'msi': ['msi'],
        'adata': ['adata'],
        '마이크로닉스': ['마이크로닉스', 'warp'],
        '에센코어': ['에센코어', 'essencore'],
        'hiksemi': ['hiksemi'],
        '렉사': ['렉사', 'lexar'],
        '컬러풀': ['컬러풀', 'colorful'],
        '바이오스타': ['바이오스타', 'biostar'],
        '키오시아': ['키오시아', 'kioxia'],
        'fastro': ['fastro'],
        '유니온': ['유니온', 'union'],
        '타임텍': ['타임텍', 'timetec'],
        'hikvision': ['hikvision'],
        'leven': ['leven'],
        'teamgroup': ['teamgroup'],
        'sabrent': ['sabrent']
    }
    preprocessor = Preprocessor(all_ssd_posts)
    for company in companies:
        merged = pd.DataFrame()
        for keyword in companies[company]:
            processed = preprocessor.extract_rows_by_keyword_exactly(
                keyword=keyword, target_column='post_title',
                ignore_case_sensitive=True
            )
            merged = pd.concat([merged, processed.loc[:, (processed.columns != 'Unnamed: 0')]], ignore_index=True)
        merged.to_csv(f"posts/ssd/{company}_ssd.csv")

def set_ssd_keywords():
    """
    get_company_ssd_posts()의 csv 파일을 참고하여 얻어낸 제품 목록과 제품 키워드들을 csv파일로 저장
    :return:
    """
    company_products = {
        'samsung': [
            '990 pro, 990 pro', '980 pro, 980 pro', '970 pro, 970 pro',
            'pm9a1, pm9a1', '970 evo plus, 970 evo plus',
        ],
        'gigabyte': [
            'aorus gen4, aorus', 'm30 2280, m30 m.2 2280'
        ],
        'lexar': [
            'ns100, ns100', 'nm800, nm800', 'nm620, nm620', 'nm790, nm790'
        ],
        'micronics': [
            'warp gx1, warp gx1', 'warp bx4, warp bx4', 'warp gx4, warp gx4'
        ],
        'micron': [
            'p3 plus, p3', 'p5 plus, p5', 't500, t500', 't700, t700',
            '2200 M.2, 2200 M.2', 'p2, p2', 'mx500, mx500'
        ],
        'sandisk': [
            'ultra, ultra', 'sata, sata'
        ],
        'seagate': [
            '파이어쿠다 520, 파이어쿠다 520', 'q5, q5', '파이어쿠다 530, 파이어쿠다 530',
            '파이어쿠다 510, 파이어쿠다 510',
        ],
        'essencore': [
            'c710, c710', 'c720, c720'
        ],
        'acer': [
            'gm7000, gm7000', 'fa200, fa200'
        ],
        'corsair': [
            'mp600, mp600', 'mp400, mp400'
        ],
        'colorful': [
            'cn600, cn600', 'cn700, cn700', 'sl500, sl500'
        ],
        'kioxia': [
            'exceria, exceria'
        ],
        'kingston': [
            'nv1, nv1', 'a400, a400', 'nv2, nv2'
        ],
        'timetec': [
            'timetec, timetec'
        ],
        'adata': [
            's70, s70', 'sx8200, sx8200', 's40g, s40g'
        ],
        'hiksemi': [
            'hiksemi, hiksemi'
        ],
        'hikvision': [
            'hhb1, hhb1'
        ],
        'leven': [
            'jps850, js850', 'js600, js600'
        ],
        'msi': [
            'm480, m480', 'm461, m461', 'm370, m370', 'm390, m390',
            'm450, m450', 'm470, m470'
        ],
        'pny': [
            'cs3040, cs3040', 'cs1030, cs1030', 'cs1031, cs1031',
            'cs2241, cs2241', 'cs2140, cs2140', 'cs900, cs900'
        ],
        'sabrent': [
            'sabrent, sabrent'
        ],
        'sk hynix': [
            'p41, p41', 'p31, p31', 'bc711, bc711'
        ],
        'western digital': [
            'sn850, sn850', 'sn530, sn530', 'sn550, sn550', 'sn850x, sn850x',
            'sn770, sn770', 'sn750, sn750', 'sn570, sn570', 'wd green, wd green',
            'sn740, sn740', 'wd blue, wd blue', 'wd 레드 플러스, wd 레드'
        ]
    }
    df = pd.DataFrame(columns=[
        'ssd_name', 'keyword'
    ])
    for company in company_products:
        for value in company_products[company]:
            words = value.split(',')
            ssd_name = f"{company} {words[0]}"
            keyword = words[-1]
            df.loc[len(df)] = [ssd_name, keyword]
    df.to_csv("posts/ssd/ssd_name_keywords.csv")

def get_posts_by_ssd_keywords(post_file, ssd_keywords_file):
    """
    ssd 제품별 키워드들을 제목에 담고 있는 게시글들을 필터링
    :param post_file: 2차 필터링된 ssd 관련 게시물들:
    :param ssd_keywords_file: ssd 제품별 이름 및 키워드 목록 csv 파일:
    :return 3차 필터링된 ssd 관련 게시글 목록 데이터프레임:
    """
    keywords_df = pd.read_csv(ssd_keywords_file)
    posts = pd.DataFrame(columns=[
        'post_title', 'product_name', 'price', 'shop_type',
        'votes', 'views', 'created_at', 'components_of_computer'
    ])
    for row in keywords_df.itertuples():
        ssd_name = row.ssd_name
        keyword = row.keyword
        preprocessor = Preprocessor(post_file)
        processed = preprocessor.extract_rows_by_keyword_contains(
            keyword=keyword, target_column='post_title',
            ignore_case_sensitive=True
        )
        for row in processed.itertuples():
            posts.loc[len(posts)] = [
                row.post_title, ssd_name, row.price, row.shop_type,
                row.votes, row.views, row.created_at, 'SSD'
            ]
        print(f"{keyword}")
    return posts

def set_ssd_volume_from_title(ssd_posts_df):
    """
    게시물 제목으로부터 ssd의 용량 키워드들을 추출하여 ssd 제품 제목에 붙여넣음
    :param ssd_posts_df: 3차 필터링된 ssd 관련 게시물 목록 데이터프레임:
    :return 제품 이름에 용량이 표시된 데이터 프레임:
    """
    new = pd.DataFrame(columns=[
        'post_title', 'product_name', 'price', 'shop_type',
        'votes', 'views', 'created_at', 'components_of_computer'
    ])
    for row in ssd_posts_df.itertuples():
        tb_pattern = r'\d{1}tb' # 1TB, 2tb, ...
        gb_pattern = r'\d+gb' # 4gb, 512GB, 1024GB, ...
        tb_volumes = re.findall(tb_pattern, row.post_title.lower())
        gb_volumes = re.findall(gb_pattern, row.post_title.lower())
        volume = " ".join(tb_volumes + gb_volumes)
        new_name = f"{row.product_name} {volume}"
        new.loc[len(new)] = [
            row.post_title, new_name, row.price, row.shop_type,
            row.votes, row.views, row.created_at, row.components_of_computer
        ]
    return new