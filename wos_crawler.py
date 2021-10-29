# -*- coding: utf-8 -*-
"""
Created on Mon Sep 21 11:23:10 2020

@author: user
"""

import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def get_paper_info():
    search_word = input("검색어를 입력해 주세요 : ")

    driver = webdriver.Chrome('C:/Users/user/OneDrive/바탕 화면/조교/chromedriver.exe')  ## 크롬드라이버 경로 설정
    driver.implicitly_wait(3)
    ## web of science 사이트 접속

    database = input("SCI or KCI ? \n => ")

    if database == 'Sci' or database == "SCI" or database == "sci":
        driver.get(
            'https://apps.webofknowledge.com/WOS_GeneralSearch_input.do?product=WOS&search_mode=GeneralSearch&SID=D1aMr6lpeeF1QVJ4TC4&preferencesSaved='
        )
    elif database == "KCI" or database == "Kci" or database == "kci":
        driver.get(
            'https://apps.webofknowledge.com/KJD_GeneralSearch_input.do?product=KJD&SID=D287K6bXXAwTmfno3PP&search_mode=GeneralSearch'
        )
    else:
        print("전체 데이터베이스를 선택하셨습니다.")
        driver.get(
            'https://apps.webofknowledge.com/UA_GeneralSearch_input.do?product=UA&SID=D287K6bXXAwTmfno3PP&search_mode=GeneralSearch'
        )

    search = driver.find_element_by_xpath('//*[@id="value(input1)"]')
    search.clear()
    search.send_keys(search_word)
    time.sleep(1)
    search.send_keys(Keys.ENTER)

    thr = driver.find_elements_by_css_selector('#pageCount\.top')
    max_page = thr[0].text
    print('이 검색어는 %s page 까지 존재합니다.(최대 10,000 page)' % max_page)

    user_want = int(input("몇 페이지 까지 크롤링 할까요? \n => "))

    total_concat = []
    raw_data = []
    for i in range(1, user_want*10 + 1):
        driver.find_element_by_css_selector(
            "#RECORD_%s > div.search-results-content > div > div:nth-child(1) > div > a > value" % i).click()
        head = driver.find_elements_by_css_selector(
            '#records_form > div > div > div > div.l-column-content > div > div.title > value')

        ex1 = driver.find_elements_by_css_selector(
            '#records_form > div > div > div > div.l-column-content > div > div:nth-child(9)')
        ex2 = driver.find_elements_by_css_selector(
            '#records_form > div > div > div > div.l-column-content > div > div:nth-child(10)')
        ex3 = driver.find_elements_by_css_selector(
            '#records_form > div > div > div > div.l-column-content > div > div:nth-child(11)')

        abstract = []
        keywords = []

        for ex in [ex1, ex2, ex3]:
            if len(ex) != 0:
                if '초록' in ex[0].text:
                    abstract = ex
                elif '키워드' in ex[0].text:
                    keywords = ex
                else:
                    None

        if len(head) == 0 or len(abstract) == 0 or len(keywords) == 0:
            for sel in [head, abstract, keywords]:
                if len(sel) != 0:
                    raw_data.append(sel[0].text)
                else:
                    raw_data.append("NaN")
        else:
            total_concat.append([head[0].text + abstract[0].text + keywords[0].text])
            raw_data.append(head[0].text)
            raw_data.append(abstract[0].text)
            raw_data.append(keywords[0].text)

        driver.back()
        time.sleep(1)

        ## 10개 크롤링하고 다음장으로 넘어가기
        if i % 10 == 0:
            print("%d / %d 크롤링 완료..." % (i//10, user_want))
            driver.find_element_by_css_selector(
                "#summary_navigation > nav > table > tbody > tr > td:nth-child(3) > a").click()
            time.sleep(2)



    return raw_data, total_concat


def make_df(a):
    df = pd.DataFrame(index=range(0, int(len(a) // 3 + 2)), columns=['title', 'abstract', 'keywords'])

    j = 0
    for i, num in enumerate(a):
        if i % 3 == 0:
            df['title'][j] = num
        elif i % 3 == 1:
            df['abstract'][j] = num
        else:
            df['keywords'][j] = num
            j += 1

    return df

def save_file(dir, name, df):
    ## 저장할 파일 이름 변경
    df.to_csv(dir+'/'+name+".csv", encoding='utf-8-sig')


if __name__ == '__main__':

    raw_data, lda_ = get_paper_info()
    df = make_df(raw_data)
    print(df.head)
    ## '' 사이에 저장할 경로 입력
    save_file('.','webofscience',df)