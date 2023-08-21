# 크롤링 결과 판다스로 저장하기 
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd

# 브라우저 실행
driver = webdriver.Chrome()
# 유튜브 인기급상승 페이지 접속
driver.get("https://www.youtube.com/feed/trending")
time.sleep(2)
# 제목 요소 가져오기 
titles = driver.find_elements(By.XPATH, '//*[@id="video-title"]')
# 제목 저장을 위한 리스트 
title_list = []
# 조회수 저장을 위한 리스트 
hits_list = []

for title in titles:
    if title.get_attribute("aria-label") and title.text: # shorts 영상을 걸러내기 위한 조건문 
        aria_label = title.get_attribute("aria-label")
        start_index = aria_label.rfind("조회수")+4
        end_index = aria_label.rfind("회")
        hits = aria_label[start_index:end_index]
        hits = int(hits.replace(",",""))        
        title_list.append(title.text)
        hits_list.append(hits)

# 제목, 조회수 리스트가 담긴 딕셔너리 
crawling_result = {
    "title": title_list,
    "hits": hits_list
}

result = pd.DataFrame(crawling_result)
# dataframe을 csv로 저장
# result.to_csv("./result.csv", encoding="utf-8-sig")
# 조회수 내림차순으로 정렬 후 csv로 저장 
result.sort_values(by=["hits"], ascending=False).to_csv("./result.csv", encoding="utf-8-sig")