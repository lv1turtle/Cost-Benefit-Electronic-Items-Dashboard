import time

import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

def get_soup_from_page_with(url):
    """
    :param url:
    :return soup object of web page:
    """
    response = requests.get(url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
    })
    return bs(response.text, 'lxml')

def scrap_cpu_names():
    """
    Scrap cpu names from passmark web page
    :return None, just save cpu name:
    """
    urls = [
        'https://www.cpubenchmark.net/socketType.html#i48'
    ]

    for idx, url in enumerate(urls, start=1):
        df = pd.DataFrame(columns=['cpu_name'])
        soup = get_soup_from_page_with(url)
        chart_list = soup.select("div.chart_body > ul.chartlist > li")
        for chart in chart_list:
            cpu_name = chart.select_one("a > span.prdname").text.strip()
            print(cpu_name)
            df.loc[len(df)] = [cpu_name]
        print(f"{idx}th page has been scraped")
        time.sleep(5)
        df.to_csv(f"cpu_names_{url[url.find('#'):]}.csv")


if __name__ == "__main__":
    scrap_cpu_names()