from selenium import webdriver
import time
import re
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urlparse,urlunparse
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


# chrome 드라이버 객체 실행시키기
driver = webdriver.Chrome(
    "/Users/dindoo/Documents/Bigdata_Musical/chromedriver")
driver.maximize_window()
driver.implicitly_wait(3)


data = pd.read_csv(r"musical_detailed_data.csv") # CSV 파일 불러오기(유효하지 않는 페이지는 걸러진 상태)
urls = data['URL'].values.tolist() # 리스트에 값

#url 열기
driver.get(urls[100])

#팝업창 관리
try:
    driver.find_element_by_css_selector('#popup-prdGuide > div > div.popupFooter > button').click()
except:
    pass

#관람 후기로 넘어가기
driver.find_element_by_partial_link_text("관람후기").click()

try:
    #위치 잡아주기 역할 및 리뷰가 있는 페이지인지 확인 역할
    driver.find_element_by_css_selector("#prdReview > div > div.bbsListWrap.reviewAll > div.pagination > ol > li").click()

    #총 페이지 수
    n=0
    while(True):
        try:
            #옆으로 이동해서 최종 페이지 확인하기
            n=n+1
            driver.find_element_by_css_selector('a.pageNextBtn.pageArrow').click()
            time.sleep(1)
            print(n)

        except:
            page_bar = driver.find_elements_by_css_selector("#prdReview > div > div.bbsListWrap.reviewAll > div.pagination > ol > li")
            last_pageNum = page_bar[-1].text
            print("최종", last_pageNum)
            break
        
    
    #이전으로 돌아가기
    for u in range(1, n):
        driver.find_element_by_css_selector('a.pagePrevBtn.pageArrow').click()
        time.sleep(1)
        print('확인', u)

    #제1 페이지로 확실히 넘어가기
    try:
        driver.find_element_by_xpath('//*[@id="prdReview"]/div/div[3]/div[2]/ol/li[1]/a').click()
    except:
        pass
                
    #최종 총 페이지 str -> int
    last_pageNum = int(last_pageNum)
    print(type(last_pageNum))

    #휴식
    time.sleep(1)

        
    # 페이지 넘기기
    for i in range(1,last_pageNum):
        page_bar = driver.find_elements_by_css_selector("#prdReview > div > div.bbsListWrap.reviewAll > div.pagination > ol > li")
        i = i + 1
        try:
            if i % 10 == 0:
                print(i)
                driver.find_element_by_css_selector('a.pageNextBtn.pageArrow').click()
                time.sleep(1)

            else:
                page_bar[i % 10].click()
                time.sleep(1)
        except:
            print("the end")
except:
    print("해당 뮤지컬에는 리뷰가 없습니다.")

driver.close()