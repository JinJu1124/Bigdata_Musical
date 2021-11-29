from selenium import webdriver
import time
import re
from bs4 import BeautifulSoup
import pandas as pd


#chrome 드라이버 객체 실행시키기
driver = webdriver.Chrome("/Users/dindoo/Documents/Bigdata_Musical/chromedriver")
driver.maximize_window()

data = pd.read_csv(r"musical_url.csv")	#CSV 파일 불러오기 
urls = data['URL'].values.tolist() #리스트에 값

#url 리스트 돌며 페이지 열기(sample 10개)
i=0
URL =[]
title = []

for url in urls:
    i = i+1 #브레이크용도
    
    #해당 url 리스트에 저장하기
    URL.append(url)

    #url 열기
    driver.get('https://tickets.interpark.com/goods/21008252')
    
    #쉬기
    time.sleep(3)

    
    #제목


    print(driver.find_element_by_css_selector('#productSide > div > div.sideBtnWrap > a.sideBtn.is-primary > span').text)

    #장소

    #공연 시간

    #관람 연령

    #선호 성별

    #선호 연령

    

    #url sample을 위한 브레이크
    if i == 1:
        break




# #티켓 카테고리로 넘어가기
# driver.find_element_by_css_selector("#allContent > div.ticketContent > div.searchHeader > a").click()
# time.sleep(2)

# content= BeautifulSoup(driver.page_source, 'html.parser')

# titles = [] #
# genres = [] #
# musical_times = [] #
# ages = [] #
# actors = [] #
# tags = [] #
# areas = [] #
# places = [] #
# periods = [] #
# musical_poster = [] 


# page_bar = driver.find_elements_by_css_selector("span.pageNumber > *")


    
# musical_list = driver.find_element_by_xpath('//*[@class="categoryContent current"]/div[@class="ticketContent"]/div[@class="searchPanel"]')
# for p in musical_list.find_elements_by_tag_name('li'):
#     item_name = p.find_element_by_class_name('itemName') #itemName 요소     
    
#     #뮤지컬 제목
#     titles.append(item_name.text)
    
#     #장르
#     genre = p.find_element_by_css_selector('div.itemInfo > div > span.type').text
#     genres.append(genre)  

#     #지역 
#     try:
#         areas.append(p.find_element_by_class_name('area').text) 
#     except:
#         areas.append(None)
    
#     #기간
#     try:
#         periods.append(p.find_element_by_class_name('period').text) 
#     except:
#         periods.append(None) #기간  

#     #공연 시간
#     musical_time = p.find_element_by_css_selector('div.itemInfo > div > span.time').text
#     musical_times.append(musical_time)

#     #연령가
#     age = p.find_element_by_css_selector('div.itemInfo > div > span.visible').text
#     ages.append(age)

#     #출연진
#     try:
#         actor = p.find_element_by_css_selector('div.itemInfo > div.castWrap.castDate > span.content').text
#         actors.append(actor)
#     except:
#         actors.append(None)

#     #tag 판매중 or 종료
#     try:
#         tag = p.find_element_by_css_selector('div.tags').text
#         tags.append(tag)
#     except:
#         tag = "판매 종료"
#         tags.append(tag)

#     #장소
#     try:
#         place = p.find_element_by_css_selector('div.col.info > span.concertHall').text
#         places.append(place)
#     except:
#         places.append(None)



# df = pd.DataFrame({'Title':titles, 'Genre':genres, 'Time':musical_times, 'Age':ages, 'Actor':actors, 'Area': areas, 'Place':places, 'Period': periods, 'Tag':tags})
# df = df.replace('\n', ' ', regex=True)
# print(df)

# # #종료하기
# driver.close()
# driver.quit()