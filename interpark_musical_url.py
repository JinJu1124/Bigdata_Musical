from selenium import webdriver
import time
import re
from bs4 import BeautifulSoup
import pandas as pd

#chrome 드라이버 객체 실행시키기
driver = webdriver.Chrome("/Users/dindoo/Documents/Bigdata_Musical/chromedriver")
driver.maximize_window()

#홈페이지 열기 interpark 뮤지컬 티켓 부분
url = "https://tickets.interpark.com/search?keyword=%EB%AE%A4%EC%A7%80%EC%BB%AC"
driver.get(url)
time.sleep(3)


#티켓 카테고리로 넘어가기
driver.find_element_by_css_selector("#allContent > div.ticketContent > div.searchHeader > a").click()
time.sleep(2)

content= BeautifulSoup(driver.page_source, 'html.parser')

titles = []
areas = []
periods= [] 
item_urls = []

page_bar = driver.find_elements_by_css_selector("span.pageNumber > *")

for n in range(1, 500):
    #뮤지컬 리스트 뽑기 눈물난다..
    
    musical_list = driver.find_element_by_xpath('//*[@class="categoryContent current"]/div[@class="ticketContent"]/div[@class="searchPanel"]')
    for p in musical_list.find_elements_by_tag_name('li'):
        item_name = p.find_element_by_class_name('itemName') #itemName 요소     
        titles.append(item_name.text) #뮤지컬 제목
        try:
            areas.append(p.find_element_by_class_name('area').text) #지역
        except:
            areas.append(None)
        try:
            periods.append(p.find_element_by_class_name('period').text) #기간
        except:
            periods.append(None) #기간
        item_urls.append(item_name.find_element_by_css_selector('a').get_attribute('href')) #url
            


#페이지 넘기기
    n = n + 1
    if n%10 == 0:
        print(n)
        driver.find_element_by_css_selector('#ticketContent > div > div.pagination > a.next').click()
        
    else:
        page_bar[n%10].click()


df = pd.DataFrame({'title':titles, 'Area': areas, 'Period': periods, 'URL':item_urls})
df = df.replace('\n', ' ', regex=True)

df.to_csv('musical_url.csv')

#종료하기
driver.close()