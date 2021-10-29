import re
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


driver = webdriver.Chrome('C:/Users/user/OneDrive/바탕 화면/조교/chromedriver.exe') ## 크롬드라이버 경로 설정
driver.implicitly_wait(3)
## web of science 사이트 접속
driver.get('https://apps.webofknowledge.com/WOS_GeneralSearch_input.do?product=WOS&search_mode=GeneralSearch&SID=D1aMr6lpeeF1QVJ4TC4&preferencesSaved=')

