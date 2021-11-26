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
time.sleep(3)

content= BeautifulSoup(driver.page_source, 'html.parser')

titles = []
tags = []
areas = []
periods= [] 
item_urls = []

#뮤지컬 리스트 뽑기 눈물난다..
musical_list = driver.find_element_by_xpath('//*[@class="categoryContent current"]/div[@class="ticketContent"]/div[@class="searchPanel"]')
for p in musical_list.find_elements_by_tag_name('li'):
    item_name = p.find_element_by_class_name('itemName') #itemName 요소
    titles.append(item_name.text) #뮤지컬 제목
    areas.append(p.find_element_by_class_name('area').text) #지역
    periods.append(p.find_element_by_class_name('period').text) #기간
    item_urls.append(item_name.find_element_by_css_selector('a').get_attribute('href')) #url

last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(0.5)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

#종료하기
driver.close()

df = pd.DataFrame({'title':titles, 'Area': areas, 'Period': periods, 'URL':item_urls})
df = df.replace('\n', ' ', regex=True)

df.to_csv('musical_url.csv')