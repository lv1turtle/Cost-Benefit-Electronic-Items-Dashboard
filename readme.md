# PC-Components-Price-fluctuation-Dashboard
We are developing PC Components Price fluctuation Patterns Analytics Dashboard by Quasarzone

## 프로젝트 소개

- 주제
  > 컴퓨터 부품 가격 변동 패턴 분석 by 퀘이사존 핫딜 게시판 
  
- 배경 및 목표
  > 컴퓨터 부품은 일반적인 다른 상품들에 비해 가격 변동이 큰 편이기에,
  > 적정선의 가격에 구매하기가 어려움.
  >
  > 퀘이사존의 핫딜 게시판의 컴퓨터 부품 핫딜 데이터를 통해, 
  > 대시보드를 구성하여 가격 변동의 패턴을 파악.
  >
  > 최종적으로 소비자의 현명한 소비를 돕는 것이 주 목적.

## 프로젝트 구현

### E-R Diagram
#### Production schema
![image](https://github.com/lv1turtle/PC-Components-Price-fluctuation-Dashboard/assets/32154881/3a0d0f70-a158-4f24-9317-e69bdd8f87d9)


#### Analytics schema (Datawarehouse)
![image](https://github.com/lv1turtle/PC-Components-Price-fluctuation-Dashboard/assets/32154881/7141c22f-2a80-487a-97c6-51f201aa4888)

### SW Architecture
![Untitled](https://github.com/lv1turtle/PC-Components-Price-fluctuation-Dashboard/assets/32154881/52f63acc-f70d-4c37-bb73-6eb6f93afdc1)

### 데이터 수집

#### BeautifulSoup4을 이용한 Web Crawling ( Quasarzone )
>https://quasarzone.com/bbs/qb_saleinfo

### 데이터 적재 및 전처리 ( ELT )

1. 수집한 데이터를 S3에 적재
![image](https://github.com/lv1turtle/PC-Components-Price-fluctuation-Dashboard/assets/32154881/1d69b99d-6494-4cf3-8e0f-bcf24534833b)

2. Python & SQL을 통해 전처리
![image](https://github.com/lv1turtle/PC-Components-Price-fluctuation-Dashboard/assets/32154881/af13fee4-33d7-4edd-a4dd-04cb883aecee)

3. 전처리한 데이터를 S3에 적재 후 COPY를 통해 Redshift에 적재
![image](https://github.com/lv1turtle/PC-Components-Price-fluctuation-Dashboard/assets/32154881/4aa665d7-65da-4348-a60c-8c11c566628d)

4. Redshift에서 추가 전처리 진행
     - Outlier 제거
     - NA 처리

### 데이터 시각화 - 대시보드 구성

#### Product Dashboard
![124](https://github.com/lv1turtle/PC-Components-Price-fluctuation-Dashboard/assets/32154881/3742feac-860b-4382-acfe-e21b2b45ecc4)

#### PC Components Dashboard
![시각화-필터링-시연3](https://github.com/lv1turtle/PC-Components-Price-fluctuation-Dashboard/assets/32154881/94ef2a8c-d0a2-4c01-a147-e295212f88bc)



## Crawling 실행 방법

- python 가상환경 생성
    ```
    py -m venv {venv_name}
    ```

- 가상환경 실행
    ```
    {venv_name}\Scripts\activate.bat
    ```

- 패키지 다운로드
    ```
    pip install -r requirements.txt
    ```

- crawling으로 이동
  - `cd crawling`

- Crawl Data 받기
  - `python hotdeal_crawler.py`

  - Preprocessing용 CPU 종류 추출
    - `python cpu_list_crawler.py`

