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
YEAR = datetime.today().year
MONTH = datetime.today().month

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
    핫딜 게시물 PC/하드웨어 태그에서 다음의 데이터를 추출
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
        hotdeal_info.loc[len(hotdeal_info)] = [
            hotdeal_summary['title'], hotdeal_summary['created_at'], hotdeal_summary['price'],
            hotdeal_summary['views'], hotdeal_summary['votes']
        ]
        print(hotdeal_info.tail(1))

def get_hotdeal_summary(hotdeal):
    votes_cell = hotdeal.select_one("td > span.num.num")
    if votes_cell:
        votes = votes_cell.text.strip()
        votes = correct(votes)
    else:
        votes = "명시되어있지않음"
    title_cell = hotdeal.select_one("td > div.market-info-list >"
                               "div.market-info-list-cont > p.tit >"
                               "a.subject-link > span.ellipsis-with-reply-cnt")
    if title_cell:
        title = title_cell.text
        title = correct(title)
    else:
        title = "명시되어있지않음"
    price_cell = hotdeal.select_one("td > div.market-info-list >"
                               "div.market-info-list-cont > div.market-info-sub >"
                               "p > span > span.text-orange")
    if price_cell:
        price = price_cell.text.replace(" ", "").strip()
        price = correct(price)
    else:
        price = "명시되어있지않음"
    views_cell = hotdeal.select_one("td > div.market-info-list >"
                               "div.market-info-list-cont > div.market-info-sub >"
                               "p > span.count")
    if views_cell:
        views = views_cell.text.strip()
        views = correct(views)
    else:
        views = "명시되어있지않음"

    created_at_cell = hotdeal.select_one("td > div.market-info-list >"
                                    "div.market-info-list-cont > div.market-info-sub >"
                                    "p > span.date")
    if created_at_cell:
        created_at = created_at_cell.text.strip()
        created_at = correct(created_at)
    else:
        created_at = "명시되어있지않음"
    return {
        "votes": votes, "title": title, "price": price,
        "views": parse_views(views), "created_at": parse_date(created_at)
    }

def correct(value):
    if value == '':
        return "명시되어있지않음"
    return value

def parse_date(created_at):
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
    if views.isdigit():
        return views
    unit_map = {'k': 1_000, 'm': 1_000_000, 'b': 1_000_000_000}
    unit = views[-1]
    views = float(views[:-1])
    return int(views * unit_map[unit])

def is_empty_page(soup):
    if soup.select_one(
            "div.list-board-wrap > "
            "div.market-type-list.market-info-type-list.relative >"
            "table > tbody > tr > "
            "td > p > a> i.fa.fa-exclamation-triangle"
    ):
        return True
    return False

def isBlocked(soup):
    if not soup.select_one("h2.title"):
        return False
    return True

def main():
    """
    1238 페이지까지 수집,
    98페이지 2024년 -> 2023년으로 넘어감

    :return:
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