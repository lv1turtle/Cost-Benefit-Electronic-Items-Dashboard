import requests
from bs4 import BeautifulSoup as bs
import time
from datetime import datetime
import pandas as pd
import re
"""
need to install "lxml"
-> "pip install lxml" 
"""
YEAR = datetime.today().year # 크롤링 시작시 연도
MONTH = datetime.today().month # 크롤링 시작시 월

def get_soup_from_page_with(url):
    """
    :param url:
    :return soup object of web page:
    """
    response = requests.get(url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
    })
    return bs(response.text, 'lxml')

def scrap_hotdeal_info(soup, hotdeal_info):
    """
    핫딜 게시판 PC/하드웨어 태그 게시물들로부터 다음의 데이터를 추출하여 데이터 프레임에 추가
    1. 제목, 2. 업로드 날짜, 3. 가격, 4. 조회수, 5. 추천수
    :param url:
    :return:
    """
    hotdeal_list = soup.select(
        "div.list-board-wrap > "
        "div.market-type-list.market-info-type-list.relative >"
        "table > tbody > tr"
    )
    for idx, hotdeal in enumerate(hotdeal_list, start=1):
        hotdeal_summary = get_hotdeal_summary(hotdeal)
        if not hotdeal_summary:
            continue
        hotdeal_info.loc[len(hotdeal_info)] = [
            hotdeal_summary['title'], hotdeal_summary['created_at'], hotdeal_summary['price'],
            hotdeal_summary['views'], hotdeal_summary['votes']
        ]
        print(hotdeal_info.tail(1))

def get_hotdeal_summary(hotdeal):
    """
    핫딜 게시물 하나로부터
    추천수, 제목, 가격, 조회수, 게시일 데이터를 스크랩하여 딕셔너리로 반환
    값이 없는 요소는 "명시되어있지않음"으로 표시
    :param hotdeal 핫딜 게시물 하나에 대한 soup :
    :return 추천수, 제목, 가격, 조회수, 게시일을 담고있는 딕셔너리:
    """
    votes_cell = hotdeal.select_one("td > span.num.num")
    if not votes_cell or len(votes_cell.text) == 0:
        return
    votes = votes_cell.text.strip()

    title_cell = hotdeal.select_one("td > div.market-info-list >"
                               "div.market-info-list-cont > p.tit >"
                               "a.subject-link > span.ellipsis-with-reply-cnt")
    if not title_cell or len(title_cell.text) == 0:
        return
    title = title_cell.text.strip()

    price_cell = hotdeal.select_one("td > div.market-info-list >"
                               "div.market-info-list-cont > div.market-info-sub >"
                               "p > span > span.text-orange")
    if not price_cell or len(price_cell.text) == 0:
        return
    price = price_cell.text.replace(" ", "").strip()

    views_cell = hotdeal.select_one("td > div.market-info-list >"
                               "div.market-info-list-cont > div.market-info-sub >"
                               "p > span.count")
    if not views_cell or len(views_cell.text) == 0:
        return
    views = views_cell.text.strip()

    created_at_cell = hotdeal.select_one("td > div.market-info-list >"
                                    "div.market-info-list-cont > div.market-info-sub >"
                                    "p > span.date")
    if not created_at_cell or len(created_at_cell.text) == 0:
        return
    created_at = created_at_cell.text.strip()
    return {
        "votes": votes, "title": title, "price": price,
        "views": parse_views(views), "created_at": parse_date(created_at)
    }

def parse_date(created_at):
    """
    게시물에 표시된 날짜 정보("HH:MM", "mm-dd")를 원하는 형태("YYYY-mm-dd")로 파싱
    시간은 오늘 날짜로, mm-dd는 맞는 연도를 붙여서 반환
    1월에서 12월로 넘어갈 때마다 연도 값을 하나씩 빼주어 게시글의 연도를 계산
    날짜가 작성한 패턴과 다른 게 들어올시 ValueError에러를 발생시킴,
    발생된 에러는 main()에서 처리
    :param created_at: 게시물에 표시된 날짜 문자열("HH:MM", "mm-dd"):
    :return 원하는 날짜 형태("YYYY-mm-dd") 문자열:
    """
    global YEAR, MONTH
    time_pattern = r'\d{2}:\d{2}'
    date_pattern = r'\d{2}-\d{2}'
    if re.match(time_pattern, created_at):
        today_month_day = datetime.today().strftime("%m-%d")
        return f'{YEAR}-{today_month_day}'
    elif re.match(date_pattern, created_at):
        visiting_month = int(created_at[:2])
        if MONTH == 1 and visiting_month == 12:
            YEAR -= 1
        if MONTH != visiting_month:
            MONTH = visiting_month
        return f"{YEAR}-{created_at}"
    raise ValueError("잘못된 형식")

def parse_views(views):
    """
    "2.2k" 와 같은 형식의 조회수를 정수형으로 변환하여 반환
    :param views: 조회수 데이터:
    :return: 정수 자료형의 조회수:
    """
    if views.isdigit():
        return views
    unit_map = {'k': 1_000, 'm': 1_000_000, 'b': 1_000_000_000}
    unit = views[-1]
    views = float(views[:-1])
    return int(views * unit_map[unit])

def is_empty_page(soup):
    """
    더 이상 크롤링할 핫딜 게시물이 있는지 검사
    :param soup 핫딜 게시판 페이지의 soup 객체:
    :return 핫딜 게시물 여부:
    """
    if soup.select_one(
            "div.list-board-wrap > "
            "div.market-type-list.market-info-type-list.relative >"
            "table > tbody > tr > "
            "td > p > a> i.fa.fa-exclamation-triangle"
    ):
        return True
    return False

def isBlocked(soup):
    """
    서버에서 크롤러를 차단했는지 여부를 검사
    :param soup:
    :return:
    """
    if not soup.select_one("h2.title"):
        return False
    return True

def main():
    """
    퀘이사존 핫딜 "PC/하드웨어" 카테고리에 해당하는 게시물 웹페이지를 더 이상 게시물이 없을 떄 까지 방문하여
    게시글 제목, 게시일, 가격, 조회수, 추천수들을 수집하여 csv파일로 저장.
    모든 과정은 자동이며, 서버로부터 차단시 15초 기다린 후 재요청하여 이어서 수집,
    사용자가 keyboard interrupt로 크롤링 종료시 크롤링한 지점까지 자동 저장,
    잘못된 날짜 데이터 등 ValueError 발생시에도 크롤링한 지점까지 자동 저장
    """
    hotdeal_info = pd.DataFrame(columns=[
        'title', 'created_at', 'price',
        'views', 'votes'
    ])
    page_no = 1
    while True:
        try:
            target_url = f"https://quasarzone.com/bbs/qb_saleinfo?_method=post&_token=WFvgK7Uo3vRnLEmg2qUVskvNlgih0KNrTrGKiRaV&category=PC%2F%ED%95%98%EB%93%9C%EC%9B%A8%EC%96%B4&kind=subject&sort=num%2C%20reply&direction=DESC&page={page_no}"
            soup = get_soup_from_page_with(target_url)
            if is_empty_page(soup):
                print("Scraping is completed")
                break
            if isBlocked(soup):
                print("Blocked by server, wait for unblocking")
                time.sleep(15)
                continue
            scrap_hotdeal_info(soup, hotdeal_info)
            print(f"page #{page_no} has been scraped")
            page_no += 1
            time.sleep(3)
        except KeyboardInterrupt:
            print("Scraping has been stopped bt KeyboardInterrupt")
            break
        except ValueError:
            print("값이 잘못된 형식으로 들어옴")
            break
    hotdeal_info.to_csv(f"hotdeal-info_utf-8-encoded_{datetime.now()}.csv", index=False, encoding='utf-8')


if __name__ == "__main__":
    main()