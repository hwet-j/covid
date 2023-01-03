from selenium import webdriver
import pandas as pd
import time
from datetime import datetime, timedelta
from twit_crawl.Clean import clean_str

def twitter_search(title):
    try:
        end = datetime.today().strftime("%Y-%m-%d")
        text_all = []
        for i in range(1):  # range 날짜 범위 -> 오늘 부터 시작되게 만들어놓음
            
            headers = {
                "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36",
                "Accept-Language":"ko-KR,ko"
                }
            
            browser = webdriver.Chrome('C:/work/chromedriver')  # 각자 컴퓨터에 파일이 존재하는 경로로
            browser.implicitly_wait(time_to_wait=5)
            
            # end의 시작은 오늘 start는 end의 전날로 설정하여 하루의 데이터를 가져오기위해 설정  
            start = (datetime.today() - timedelta(i+1)).strftime("%Y-%m-%d")
            end = (datetime.today() - timedelta(i)).strftime("%Y-%m-%d")
            url = "https://twitter.com/search?q={0}%20until%3A{2}%20since%3A{1}&src=typed_query"
            
            # 아스트라제네카(AZ), 화이자
            # (아스트라제네카 OR AZ백신) 으로 검색어 하면 둘중하나 언급해도 나옴
            # 검색어 변경은 여기서 -> 코드로 입력 말고 input 사용해도됨. 현재로써 필요성을 느끼지 못함
            search = url.format(title, start ,end)
            
            browser.get(search)
            
            prev_height = browser.execute_script("return document.body.scrollHeight")
            
            text = []   # 작성글 하나씩 분류 저장하기 위함 - for문 돌때마다 초기화
            
            # 웹페이지 맨 아래까지 무한 스크롤
            while True:
                # 데이터 추출
                element = browser.find_elements_by_class_name("css-901oao.r-18jsvk2.r-1qd0xha.r-a023e6.r-16dba41.r-rjixqe.r-bcqeeo.r-bnwqim.r-qvutc0")
                
                for n in element:
                    # name1 = n.text.split("\n")    # 올바른 데이터가 나오는지 확인
                    text.append(clean_str(n.text, title))  # 변수 저장
                    # text.append(n.text.split("\n")) # 변수 저장
                    # text_all.append(n.text.split("\n"))
                # print(text) # 확인
                
                # 스크롤을 화면 가장 아래로 내린다
                browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            
                # 페이지 로딩 대기 (스크롤 내리고 데이터 로딩을 기다림)
                time.sleep(2)
                
                # 현재 문서 높이를 가져와서 저장 (if문 사용하기 위해)
                curr_height = browser.execute_script("return document.body.scrollHeight")
        
                if(curr_height == prev_height):
                    break   
                else:  
                    prev_height = browser.execute_script("return document.body.scrollHeight")
            
            print(text)
            df = pd.DataFrame(text)
            
            #file_name = "./data/Twitter_{}.txt".format(end)
            # 하루 데이터 저장
            #df.to_csv(file_name, mode='w', index = False, header = False)
            
            # 이어쓰기 - 이름 수동 수정
            df.to_csv("./data/Twitter_all_data(" +title +").txt", mode='a', index = False, header = False)
            
            time.sleep(2)   # 저장이 완성되고 넘어갈수있는 방법을찾아보기
            browser.quit()  # 브라우저 종료 - 완성되면
            print(i)
            print('성공')
        
        # 전체를 저장(지정해준 범위만큼) - 이어쓰기해서 필요없음
        #df2 = pd.DataFrame(text_all) 
        #df2.to_csv("./data/Twitter_all_data.txt", mode='w', index = False, header = False)
        print('끝')
    except Exception as e:
        print(e)
        print('에러')    





