# -*- coding: utf-8 -*-
"""
Created on Mon Sep 21 11:23:10 2020

@author: user
"""
import re
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

#%%
driver = webdriver.Chrome('C:/Users/user/OneDrive/바탕 화면/RA/chromedriver.exe') ## 크롬드라이버 경로 설정
driver.implicitly_wait(3)
## web of science 사이트 접속
driver.get('https://apps.webofknowledge.com/WOS_GeneralSearch_input.do?product=WOS&search_mode=GeneralSearch&SID=D1aMr6lpeeF1QVJ4TC4&preferencesSaved=')

## forensic 검색어 입력
search = driver.find_element_by_xpath('//*[@id="value(input1)"]')
search.clear()
search.send_keys('digital forensic')
time.sleep(1)
search.send_keys(Keys.ENTER)

## 페이지 이동
#search = driver.find_element_by_xpath('//*[@id="summary_navigation"]/nav/table/tbody/tr/td[2]/input')
#search.clear()
#search.send_keys('58')
#time.sleep(1)
#search.send_keys(Keys.ENTER)

## 제목, 요약문, 키워드 순으로 크롤링후 리스트 생성 
raw_data = []
for i in range(1,2301):
    driver.find_element_by_css_selector("#RECORD_%s > div.search-results-content > div > div:nth-child(1) > div > a > value"%i).click()
    head = driver.find_elements_by_css_selector('#records_form > div > div > div > div.l-column-content > div > div.title > value')

    ex1 = driver.find_elements_by_css_selector('#records_form > div > div > div > div.l-column-content > div > div:nth-child(9)')
    ex2 = driver.find_elements_by_css_selector('#records_form > div > div > div > div.l-column-content > div > div:nth-child(10)')
    ex3 = driver.find_elements_by_css_selector('#records_form > div > div > div > div.l-column-content > div > div:nth-child(11)')
    
    abstract = []
    keywords = []

    for ex in [ex1, ex2, ex3]:
        if len(ex) != 0:
            if '초록' in ex[0].text:
                abstract = ex
            elif '키워드' in ex[0].text:
                keywords = ex
            else :
                None
            
    if len(head)==0 or len(abstract)==0 or len(keywords)==0:
        for sel in [head,abstract,keywords]:
            if len(sel) != 0:
                raw_data.append(sel[0].text)
    else:
        raw_data.append([head[0].text+abstract[0].text+keywords[0].text])
    
    driver.back()
    time.sleep(1)
    
    ## 10개 크롤링하고 다음장으로 넘어가기
    if i%10 == 0:
        driver.find_element_by_css_selector("#summary_navigation > nav > table > tbody > tr > td:nth-child(3) > a").click()
        time.sleep(2)
        

#%%
## 파일 추출
file = open('C:/Users/user/OneDrive/바탕 화면/RA/raw_data.txt', 'w', encoding='utf8')
for a in raw_data:
  file.write(a[0])
file.close()
#%%
## 토큰화, 전처리(영문, 불용어제거, 소문자, stemming)
import nltk
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
from nltk.stem.snowball import SnowballStemmer
nltk.download('punkt')
nltk.download('stopwords')

## 영문이 아닌 문자 제외 및 소문자화
normalized_text = []
for string in raw_data:  
  tokens = re.sub(r"[^a-z0-9]+", " ", string[0])
  normalized_text.append(tokens.lower())

## 토큰화
result = [word_tokenize(sentence) for sentence in normalized_text]

## 불용어 제거
stop_words = set(stopwords.words('english')) 

tokenized_doc = []
for st in result:
  temp = []
  for tk in st:
    if tk not in stop_words: 
        temp.append(tk)
  tokenized_doc.append(temp)

## stemming
snowball = SnowballStemmer('english')
st_tokenized_doc = []
for text in tokenized_doc:
    tmp = []
    for t in text:
        tmp.append(snowball.stem(t))
    st_tokenized_doc.append(tmp)

#%%
## TFIDF 행렬 만들기

# 역토큰화 (토큰화 작업을 되돌림)
detokenized_doc = []
for i in range(len(st_tokenized_doc)):
    t = ' '.join(st_tokenized_doc[i])
    detokenized_doc.append(t)
    
from sklearn.feature_extraction.text import TfidfVectorizer
vectorizer = TfidfVectorizer(stop_words='english', 
max_features= 1000) # 상위 1000개의 단어를 보존 
X = vectorizer.fit_transform(detokenized_doc)
print(X.shape) # TF-IDF 행렬의 크기 확인

#%%
# LDA

from sklearn.decomposition import LatentDirichletAllocation
lda_model=LatentDirichletAllocation(n_components=10,learning_method='online',random_state=777,max_iter=1)

lda_top=lda_model.fit_transform(X)

print(lda_model.components_)
print(lda_model.components_.shape)

#%%

terms = vectorizer.get_feature_names() # 단어 집합. 1000개의 단어가 저장됨.

def get_topics(components, feature_names, n=10):
    for idx, topic in enumerate(components):
        print("Topic %d:" % (idx+1), [(feature_names[i], topic[i].round(2)) for i in topic.argsort()[:-n - 1:-1]])
get_topics(lda_model.components_,terms)