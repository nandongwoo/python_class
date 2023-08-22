## 유튜브 크롤링 
### 사용 라이브러리 
- selenium: 브라우저 제어, 웹페이지 요소 가져오기, 스크롤 제어를 위한 js 제어, 키보드 동작 등 
- konlpy: 영상 제목으로부터 명사, 형용사 추출 
- Counter: 명사, 형용사 노출 빈도 
- wordcloud: 워드클라우드 이미지 생성
- pandas: 크롤링 결과 저장 
- matplotlib: 이미지 출력 등 

### 유튜브 인기급상승 영상 분석 
1. 인기급상승 페이지 접속 
2. 무한스크롤로 모든 영상 로딩 
3. 모든 영상의 제목, 조회수 데이터 수집 및 각각 리스트로 저장 
4. 수집된 제목으로 부터 명사, 형용사 추출하여 결과를 별도 리스트로 저장
5. 추출한 명사, 형용사를 가지고 워드클라우드 이미지 생성 
6. 제목, 조회수 데이터는 pandas로 result.csv 라는 이름으로 저장(저장시 조회수 기준 내림차순) 


### db 저장시 한글 처리를 위한 쿼리 
```
create table table1(
	title varchar(500),
    hit int
    ) default charset=utf8;

alter database db_python character set = utf8mb4 collate = utf8mb4_unicode_ci;
alter table table1 convert to character set utf8mb4 collate utf8mb4_unicode_ci;
alter table table1 change title title varchar(500) character set utf8mb4 collate utf8mb4_unicode_ci;
```