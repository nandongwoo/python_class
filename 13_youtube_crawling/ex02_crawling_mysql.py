from konlpy.tag import Kkma
from konlpy.tag import Okt
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
import pymysql

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False
# 임포트를 하고 사용하지 않으면 흐리게 표시된다.

def scroll_fun():
    while True:
        h1 = driver.execute_script("return document.documentElement.scrollHeight")
        print("현재높이",h1)
        # 스크롤을 현재높이 만큼 내리기
        driver.execute_script("window.scrollTo(0,document.documentElement.scrollHeight)")
        #영상 로딩 시간
        time.sleep(2)

        h2= driver.execute_script("return document.documentElement.scrollHeight")
        print("두번 째 높이:", h2)
        if h1 == h2 :
            print("끝!")
            break

# 크롬 브라우저 실행
driver = webdriver.Chrome()
# 유튜브 인기급상승 페이지 접속
driver.get("https://www.youtube.com/feed/trending")
time.sleep(2)

# 무한스크롤 함수 호출
scroll_fun()

#제목 요소 가져오기
titles = driver.find_elements(By.XPATH, '//*[@id="video-title"]')

#제목 저장을 위한 리스트
title_list = []
#조회수 저장을 위한 리스트
hits_list= []

for title in titles:
    # short , 영화 , 제목데이터가 없는 컨텐츠 # shorts 영상을 걸러내기 위한 조건문
    if title.get_attribute("aria-label") and title.text and "YouTube 영화" not in title.get_attribute("aria-label"): 
        aria_label = title.get_attribute("aria-label")
        start_index= aria_label.rfind("조회수")+4
        end_index = aria_label.rfind("회")
        hits = aria_label[start_index:end_index]
        # 조회수 값 범위에 따라 분리
        # 조회수 없는 영상은 0으로, 조회수가 1000미만인 영상은 , 처리 생략
        # 조회수 1,000 이상인 영상
        hits = int(hits.replace(",",""))
        title_list.append(title.text)
        hits_list.append(hits)

conn = pymysql.connect(
    host='127.0.0.1',
    user='user_python',
    password='1234',
    db='db_python',
    charset='utf8mb4')

cur = conn.cursor()
sql = "insert into `table1`(title, hit) values(%s, %s);"
tuple_result = list(zip(title_list, hits_list))
cur.executemany(sql, tuple_result)

conn.commit()

crawling_result = {
    "title": title_list,
    "hits": hits_list
}

result = pd.DataFrame(crawling_result)
# dataframe을 csv로 저장
# result.to_csv("./result.csv", encoding="utf-8-sig")
# 조회수 내림차순으로 정렬 후 csv로 저장
result.sort_values(by=["hits"], ascending=False).to_csv("./result.csv", encoding="utf-8-sig")

okt = Okt()
kkma = Kkma()
word_list = []
# okt, kkma 로 추출할 때 에는 리스트 클라스에 담아서 바로 추출할 수 없기 때문에
# for문을 사용해서 걸러주는 작업이 필요함
# 명사, 형용사만 따로 출력
for title in title_list:
    for word, tag in okt.pos(title):
    # if tag in 'Noun': # 명사만
        if tag in ['Noun', 'Adjective']: # 명사만
        # print(word, tag)
            word_list.append(word)

#같은 단어 노출 빈도
word_list_count = Counter(word_list)

# 단어로 이루어진 리스트 생성
words = []
for word, count in word_list_count.most_common(5):
    words.append(word)

# words = [word for word, count in word_list_count.most_common(5)]
# 횟수로 이루어진 리스트 생성 
counts = [count for word, count in word_list_count.most_common(5)]
plt.bar(words, counts)
plt.show()

# 워드클라우드 객체 생성
wc = WordCloud(font_path='malgun', width=400, height=400)

#Counter 로 분석한 데이터를 wordcloud로 만들기
result = wc.generate_from_frequencies(word_list_count)

#matplotlib로 이미지 출력하기
plt.axis('off') # x, y 축은 필요없음으로 생략

#결과를 이미지로 출력할 준비
plt.imshow(result)
#이미지 출력
plt.show()
# wc.to_file('YouTube.png')
