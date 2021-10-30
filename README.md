# research_crawler

본 크롤러는 [2020-2nd Semester] RA 업무 중에 진행했던 Web of Science 홈페이지(https://www.webofscience.com/wos/woscc/basic-search)에서 정보를 크롤링해오는 코드입니다.

#### Requirement

- pandas
- selenium
- Chrome Driver
- nltk
- sklearn

Selenium 라이브러리를 이용한 크롤링 코드 입니다. 셀레니움은 파이어폭스, 인터넷 익스플로어, 크롬등과 같은 브라우저를 컨트롤 할 수 있게 해줍니다. 현재 파이썬 3.5 이상부터 지원되며 3.6 이상 버전 부터 pip 로 표준 라이브러리로 사용할 수 있습니다.

- 드라이버 : https://sites.google.com/a/chromium.org/chromedriver/downloads


### LDA 결과

- 추가적으로 "Digital Forensic" 키워드로 검색한 결과를 LDA한 과정까지 함께 첨부합니다.
- 
- 크롤링 한 논문 : 2377개(제목, 요약문, 키워드) *요약문이나 키워드가 없는 경우에는 제목만 크롤링
- 상위 1000개 단어를 보존하여 분석 진행
- 10개 토픽, 각 토픽 별 10개의 단어 추출

```python
from sklearn.decomposition import LatentDirichletAllocation
lda_model=LatentDirichletAllocation(n_components=10,learning_method='online',random_state=777,max_iter=1)

lda_top=lda_model.fit_transform(X)
```

1. Stemming 하지 않은 결과
![image](https://user-images.githubusercontent.com/46701548/139521292-ac6d09a0-89ac-4092-965a-e6d8d7406fc2.png)

2. Stemming 한 결과
![image](https://user-images.githubusercontent.com/46701548/139521305-2aadf072-3317-4bc8-bfeb-bb82b6c52f33.png)
