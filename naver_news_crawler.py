# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import pandas as pd
import requests


def naver_news_search(keyword: str) -> pd.DataFrame:
    news_client_id = "asZxUXe8wjgWwbXgyn5l"
    news_client_secret = "TvDdDWqjmz"

    search_word = keyword  # 검색어
    encode_type = 'json'  # 출력 방식 json 또는 xml
    max_display = 100  # 출력 뉴스 수
    sort = 'date'  # 결과값의 정렬기준 시간순 date, 관련도 순 sim
    start = 1  # 출력 위치

    url = f"https://openapi.naver.com/v1/search/news.{encode_type}?query={search_word}&display={str(int(max_display))}&start={str(int(start))}&sort={sort}"

    # 헤더에 아이디와 키 정보 넣기
    headers = {'X-Naver-Client-Id': news_client_id,
               'X-Naver-Client-Secret': news_client_secret
               }

    # HTTP요청 보내기
    r = requests.get(url, headers=headers)
    # 요청 결과 보기 200 이면 정상적으로 요청 완료
    print(r)

    news_df = pd.DataFrame(r.json()['items'])
    news_df.to_csv("./result_save.csv", encoding = 'utf-8-sig')
    return news_df

if __name__ == '__main__':

    keyword = "한국"

    test_search = naver_news_search(keyword)
    print(test_search)