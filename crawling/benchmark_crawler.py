import time

import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
"""
Passmark 웹 사이트로부터 CPU, GPU 벤치마크 정보를 크롤링,
기존 프로젝트에 벤치마크 내용 추가함에 따라 크롤러도 추가함.
전체적인 스크랩핑 구조는 passmark로부터 cpu 이름들을 추출하는 cpu_list_crawler와 동일
"""
def get_soup_from_page_with(url):
    """
    :param url:
    :return soup object of web page:
    """
    response = requests.get(url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
    })
    return bs(response.text, 'lxml')

def scrap_benchmark_info():
    """
    Scrap cpu, gpu names and benchmark score from passmark web page
    :return None, just save cpu name:
    """
    urls = [
        ('https://www.cpubenchmark.net/socketType.html#i48', 'CPU'), # cpu benchmark
        ('https://www.videocardbenchmark.net/high_end_gpus.html', 'gpu') # gpu benchmark
    ]
    df = pd.DataFrame(columns=['product_name', 'product_performance', 'components_of_computer'])
    for idx, url_tuple in enumerate(urls, start=1):
        url = url_tuple[0]
        components_of_computer = url_tuple[1]
        soup = get_soup_from_page_with(url)
        chart_list = soup.select("div.chart_body > ul.chartlist > li")
        for chart in chart_list:
            product_name = chart.select_one("a > span.prdname").text.strip()
            product_performance = chart.select_one("a > span.count").text.replace(',', '').strip()
            if not product_performance.isdigit():
                continue
            print(f"{product_name} {product_performance}")
            df.loc[len(df)] = [product_name, product_performance, components_of_computer]
        print(f"{idx}th page has been scraped")
        time.sleep(5)
    df.to_csv(f"cpu_gpu_bench_marks.csv")


if __name__ == "__main__":
    scrap_benchmark_info()
