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

titles = [] #
genres = [] #
musical_times = [] #
ages = [] #
actors = [] #
tags = [] #
areas = [] #
places = [] #
periods = [] #
# musical_poster = [] 


for n in range(1, 500):
    #뮤지컬 리스트 뽑기 눈물난다..
    
    musical_list = driver.find_element_by_xpath('//*[@class="categoryContent current"]/div[@class="ticketContent"]/div[@class="searchPanel"]')
    for p in musical_list.find_elements_by_tag_name('li'):
        item_name = p.find_element_by_class_name('itemName') #itemName 요소     
        
        #뮤지컬 제목
        titles.append(item_name.text)
        
        #장르
        genre = p.find_element_by_css_selector('div.itemInfo > div > span.type').text
        genres.append(genre)  

        #지역 
        try:
            areas.append(p.find_element_by_class_name('area').text) 
        except:
            areas.append(None)
        
        #기간
        try:
            periods.append(p.find_element_by_class_name('period').text) 
        except:
            periods.append(None) #기간  

        #공연 시간
        try:
            musical_time = p.find_element_by_css_selector('div.itemInfo > div > span.time').text
            musical_times.append(musical_time)
        except:
            musical_times.append(None)

        #연령가
        try:
            age = p.find_element_by_css_selector('div.itemInfo > div > span.visible').text
            ages.append(age)
        except:
            ages.append(None)

        #출연진
        try:
            actor = p.find_element_by_css_selector('div.itemInfo > div.castWrap.castDate > span.content').text
            actors.append(actor)
        except:
            actors.append(None)

        #tag 판매중 or 종료
        try:
            tag = p.find_element_by_css_selector('div.tags').text
            tags.append(tag)
            print(tag)
        except:
            print('error')
            # tag = "판매 종료"
            # tags.append(tag)

        #장소
        try:
            place = p.find_element_by_css_selector('div.col.info > span.concertHall').text
            places.append(place)
        except:
            places.append(None)

#페이지 넘기기
    page_bar = driver.find_elements_by_css_selector("span.pageNumber > *")
    n = n + 1
    if n%10 == 0:
        print(n)
        driver.find_element_by_css_selector('#ticketContent > div > div.pagination > a.next').click()
        
    else:
        page_bar[n%10].click()


df = pd.DataFrame({'Title':titles, 'Genre':genres, 'Time':musical_times, 'Age':ages, 'Actor':actors, 'Area': areas, 'Place':places, 'Period': periods, 'Tag':tags})
df = df.replace('\n', ' ', regex=True)

df.to_csv('musical_data.csv')

#종료하기
driver.close()