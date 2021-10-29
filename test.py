

from selenium import webdriver as wd
import requests
from bs4 import BeautifulSoup
import time
import re
from datetime import datetime


class webofscience():

    def __init__(self):

        self.title = []
        self.abstract = []
        self.keywords = []
        self.keyword = input('검색어를 입력하세요 :')

    def get_post_info(self):

        driver = webdriver.Chrome('C:/Users/user/OneDrive/바탕 화면/조교/chromedriver.exe')  ## 크롬드라이버 경로 설정
        driver.implicitly_wait(3)
        ## web of science 사이트 접속
        driver.get(
            'https://apps.webofknowledge.com/WOS_GeneralSearch_input.do?product=WOS&search_mode=GeneralSearch&SID=D1aMr6lpeeF1QVJ4TC4&preferencesSaved=')

        ## forensic 검색어 입력
        search = driver.find_element_by_xpath('//*[@id="value(input1)"]')
        search.clear()
        search.send_keys(keyword)
        time.sleep(1)
        search.send_keys(Keys.ENTER)

        page = int(input("크롤링할 페이지 입력 :"))

        raw_data = []
        for i in range(1, 2377):
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
                raw_data.append([head[0].text + abstract[0].text + keywords[0].text])

            driver.back()
            time.sleep(1)

            ## 10개 크롤링하고 다음장으로 넘어가기
            if i % 10 == 0:
                driver.find_element_by_css_selector(
                    "#summary_navigation > nav > table > tbody > tr > td:nth-child(3) > a").click()
                time.sleep(2)

        return raw_data

if __name__=="__main__":
    webofscience()