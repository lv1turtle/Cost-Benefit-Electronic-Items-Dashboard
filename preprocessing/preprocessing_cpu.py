import time

from preprocessor import Preprocessor
import pandas as pd


def get_intel_core_cpu_names(file, target_column):
    """
    get intel core cpu name from all cpu name csv file
    :param all cpu name csv file from "passmark" web page:
    :param core, intel core shch as "i3, i5, i7, i9":
    :return intel core cpu names:
    """
    processed = get_i3_to_i9_intel_cpu(file, target_column)
    new = pd.DataFrame(columns=['cpu_name'])
    for idx, row in processed.iterrows():
        cpu_name = row[target_column]
        parsed_name = parse_intel_cpu_name(cpu_name)
        new.loc[len(new)] = parsed_name
    return new

def get_i3_to_i9_intel_cpu(file, target_column):
    preprocessor = Preprocessor(file)
    processed = pd.DataFrame()
    for core in ['i3', 'i5', 'i7', 'i9']:
        processed = pd.concat(
            [
                processed,
                preprocessor.extract_rows_by_keyword_contains(keyword=core, target_column=target_column)
            ],
            ignore_index=True
        )
    return processed
def parse_intel_cpu_name(cpu_name):
    repeated = 'Intel Core'
    start_idx = cpu_name.find(repeated) + len(repeated)
    end_idx = cpu_name.find('@')
    if end_idx != -1:
        return cpu_name[start_idx:end_idx].strip()
    return cpu_name[start_idx:].strip()


def get_ryzen_cpu_names(file, target_column):
    """
    get ryzen cpu name from all cpu name csv file
    :param all cpu name csv file from "passmark" web page:
    :param core, intel core shch as "3, 5, 7, 9":
    :return ryzen core cpu names:
    """
    processed = get_ryzen3_to_9_amd_cpu(file, target_column)
    new = pd.DataFrame(columns=['cpu_name'])
    for idx, row in processed.iterrows():
        cpu_name = row[target_column]
        parsed_name = parse_ryzen_cpu_name(cpu_name)
        print(parsed_name)
        new.loc[len(new)] = parsed_name
    return new


def get_ryzen3_to_9_amd_cpu(file, target_column):
    preprocessor = Preprocessor(file)
    processed = pd.DataFrame()
    for core in ['3', '5', '7', '9']:
        processed = pd.concat(
            [
                processed,
                preprocessor.extract_rows_by_keyword_contains(keyword=f"Ryzen {core}", target_column=target_column)
            ],
            ignore_index=True
        )
    return processed


def parse_ryzen_cpu_name(cpu_name):
    repeated = 'AMD'
    start_idx = cpu_name.find(repeated) + len(repeated)
    return cpu_name[start_idx:].strip()


def add_keyword_with_cpu_name(cpu_names, company):
    """
    :param cpu_nams: intel, ryzen cpu names:
    :param company: cpu manufacturing company(Intel, AMD):
    :return datafrmae including cpu name and keyword such as: (Ryzen 5 3600, 3600):
    """
    new = pd.DataFrame(columns=['cpu_name', 'keyword'])
    delimiter = ' '
    if company == 'AMD':
        delimiter = ' '
    elif company == 'Intel':
        delimiter = '-'

    for row in cpu_names.itertuples():
        name_words = row.cpu_name.split(delimiter)
        target_keyword = name_words[-1]
        if target_keyword == "Edition":
            target_keyword = name_words[2] if name_words[2] != "PRO" else name_words[3]
        new.loc[len(new)] = [row.cpu_name, target_keyword]
    new = new.sort_values(by=['keyword'], ignore_index=True)
    return new


def get_posts_by_cpu_keyword(post_file, cpu_keywords_file):
    """
    cpu 키워드가 post의 title에 포함되어 있을 경우에만 post의 행을 가져옴
    또한, post의 행에 내용을 추가하여 다음의 컬럼들로 dataframe을 구성하고 csv로 저장
    post_title, product_name, price, shop_type, votes, views, created_at
    """
    cpu_keywords = pd.read_csv(cpu_keywords_file)
    posts = pd.DataFrame(columns=[
        'post_title', 'product_name', 'price', 'shop_type',
        'votes', 'views', 'created_at'
    ])
    for row in cpu_keywords.itertuples():
        cpu_name = row.cpu_name
        cpu_keyword = row.keyword
        preprocessor = Preprocessor(post_file)
        processed = preprocessor.extract_rows_by_keyword_exactly(keyword=cpu_keyword, target_column='title',
                                                                 ignore_case_sensitive=True)
        for row in processed.itertuples():
            posts.loc[len(posts)] = [
                row.title, cpu_name, row.price, row.shop_type,
                row.votes, row.views, row.created_at
            ]
        print(f"{cpu_name}: {cpu_keyword}")
    return posts


def delete_rows_except_cpu(cpu_post_file):
    """
    제외해야할 키워드를 통해 원치않는 행들을 제거하고,
    실제로는 판매 게시글이 없는 상품을 포함한 행들도 제거한 후 반환
    :param cpu_post_file:
    :return dataframe filtered:
    """
    keywords = [
        '마이크로닉스', '브라보텍', '기가', 'peerless', 'asus', '아수스',
        '노트북', '중고', 'rtx', '본체', '메모리', '케이스', '1660super',
        '앱코', '시소닉', '키크론', '장패드', '커세어', 'ddr', 'trident', 'Corsair',
        '8*2', 'rx570', '그래픽', '조립', 'B550', '1660ti', '에이서', 'beelink',
        '파빌리온', '데스크탑', '3060ti', '6600xt', '6700xt', '3070', '6600',
        '세트', '3060', 'msi', '3050', '6800 xt', '3080ti', '마이크론',
        'gigabyte', '빅터스', '4070', '4060', 'asrock', 'b650m', 'microsoft',
        'zotac', '3080', '7900xt', 'x670', 'asrock', 'z690', '샌디스크', 'x670e',
        '파이어쿠다', '마그네틱 케이블', 'evga', '6700 xt', '헤드폰', '마우스', '키보드',
        '태블릿', 'fsp', '1tb', 'gold', '골드', 'wd', '에너맥스', '870evo', '970 evo',
        '38gn 950', 'nvme', '980 pro', '980 프로', 'ssd', '870 evo', '삼성 980',
        '갤럭시', '클레브 CRAS X RGB 3600'
    ]
    keywords += [
        'RTX4090', 'RTX4080SUPER', 'RTX4070Ti', 'RTX4070SUPER', 'RTX4070',
        'RTX4060Ti', 'RTX4080', 'RTX4060', 'RTX3090', 'RTX3080Ti', 'RTX3080', 'RTX3070Ti',
        'RTX3070', 'RTX3060Ti', 'RTX3060', 'RTX3050', 'RTX2080Ti', 'RTX2080SUPER', 'RTX2060SUPER',
        'RTX2060', 'GTX1660Ti', 'GTX1660SUPER', 'GTX1660', 'GTX1650SUPER', 'GTX1650', 'GTX1630', 'GT1030',
        'GT730', 'GT710', 'GTX1050Ti', 'T1000', 'T600', 'T400', 'H100', 'L40S', 'A40', 'A30',
        'RTXA6000', 'RTXA5500', 'RTXA5000', 'RTXA4500', 'RTXA4000', 'RTXA2000', 'GTX760',
        'GTX750Ti', 'RTX6000', 'RTX5000', 'RTX4500', 'RTX4000', 'P400', 'P620', 'G210',
        'TeslaA100', 'P2000', '지포스GTX550Ti', 'GT610', 'RX7900XTX', 'RX7900XT',
        'RX7900GRE', 'RX7800XT', 'RX7700XT', 'RX7600XT', 'RX7600', 'RX6900XT',
        'RX6800XT', 'RX6800', 'RX6750XT', 'RX6700XT', 'RX6700', 'RX6650XT', 'RX6600XT',
        'RX6600', 'RX6500XT', 'RX6400', 'RX580', 'RX570', 'RX560', 'RX550', 'RX480',
        'W7900', 'W7800', 'W7700', 'W7600', 'W7500', 'W6900X', 'W6800X', 'W6800',
        'W6600', 'W5700', 'W5500', 'WX3200', 'WX3100', 'ARCA770', 'ARCA750',
        'ARCA580', 'ARCA380', 'ARCA310'
    ]
    keywords += [
        'RTX 4090', 'RTX 4080', 'RTX 4070',
        'RTX 4060', 'RTX 3090', 'RTX 3080',
        'RTX 3070', 'RTX 3060', 'RTX 3050', 'RTX 2080', 'RTX 2060',
        'GTX 1660', 'GTX 1650', 'GTX 1630', 'GT 1030',
        'GT 730', 'GT 710', 'GTX 1050', 'T 1000', 'T 600', 'T 400', 'H 100', 'L 40S', 'A 40', 'A 30',
        'RTX A6000', 'RTX A5500', 'RTX A5000', 'RTX A4500', 'RTX A4000', 'RTX A2000', 'GTX 760',
        'GTX 750', 'RTX 6000', 'RTX 5000', 'RTX 4500', 'RTX 4000', 'P 400', 'P 620', 'G 210',
        'Tesla A100', 'P 2000', 'GTX 550', 'GT 610', 'RX 7900',
        'RX 7800', 'RX 7700', 'RX 7600', 'RX 6900',
        'RX 6800', 'RX 6750', 'RX 6700', 'RX 6650', 'RX 6600',
        'RX 6500', 'RX 6400', 'RX 580', 'RX 570', 'RX 560', 'RX 550', 'RX 480',
        'W 7900', 'W 7800', 'W 7700', 'W 7600', 'W 7500', 'W 6900', 'W 6800',
        'W 6600', 'W 5700', 'W 5500', 'WX 3200', 'WX 3100', 'ARCA770', 'ARCA750',
        'ARCA580', 'ARCA380', 'ARCA310'
    ]
    df = pd.read_csv(cpu_post_file)
    for keyword in keywords:
        idx = df[df['post_title'].str.lower().str.contains(keyword.lower())].index
        df = df.drop(idx)
    products = [
        'i5-7600', 'i7-7700', 'i7-7800X', 'i7-7900X', 'i9-7900X', 'Ryzen 3 3300X',
        'Ryzen 3 PRO 1300', 'Ryzen 5 1400', 'Ryzen 5 Microsoft Surface Edition',
        'Ryzen 7 Extreme Edition', 'Ryzen 7 PRO 7840HS'
    ]
    for product in products:
        idx = df[df['product_name'] == product].index
        df = df.drop(idx)
    df = df.sort_values(by=['product_name'], ignore_index=True)
    return df

def preprocess_cpu():
    cpu_names_file = "../crawling/cpu_names/cpu_names_#i48.csv"
    intel_cpu_names = get_intel_core_cpu_names(cpu_names_file, 'cpu_name')
    ryzen_cpu_names = get_ryzen_cpu_names(cpu_names_file, 'cpu_name')
    intel_cpu_name_with_keyword = add_keyword_with_cpu_name(intel_cpu_names, 'Intel')
    ryzen_cpu_name_with_keyword = add_keyword_with_cpu_name(ryzen_cpu_names, 'AMD')
    all_cpu_name_with_keyword = pd.concat(
        [intel_cpu_name_with_keyword, ryzen_cpu_name_with_keyword],
        ignore_index=True
    )
    # 팀원들과 키워드 공유를 위해 저장
    all_cpu_name_with_keyword.to_csv("../crawling/cpu_names/cpu_names_with_keyword.csv")
    time.sleep(5)
    print("Waiting for saving cpu name with keyword file")
    all_cpu_name_with_keyword_file = pd.read_csv("../crawling/cpu_names/cpu_names_with_keyword.csv")
    post_file = pd.read_csv("../crawling/2021-2023.csv")
    # 1차 전처리
    cpu_posts = get_posts_by_cpu_keyword(post_file, all_cpu_name_with_keyword_file)
    # 1차 전처리 후, 백업을 위해 저장
    cpu_posts.to_csv("../crawling/cpu_posts.csv")
    time.sleep(5)
    print("Waiting for saving cpu posts file")
    cpu_post_file = pd.read_csv("../crawling/cpu_posts.csv")
    # cpu와 관련 없는 게시물에 들어가는 키워드들로 필터링
    filtered = delete_rows_except_cpu(cpu_post_file)
    filtered.to_csv("../crawling/filtered.csv")

if __name__ == "__main__":
    preprocess_cpu()


