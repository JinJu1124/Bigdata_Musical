from selenium import webdriver
from bs4 import BeautifulSoup
import time
import re
import pandas as pd

#chrome 드라이버 객체 실행시키기
driver = webdriver.Chrome("/Users/dindoo/Documents/Bigdata_Musical/chromedriver")
driver.maximize_window()

#홈페이지 열기 interpark 뮤지컬 티켓 부분
url = "https://mobileticket.interpark.com/search/result?keyword=%EB%AE%A4%EC%A7%80%EC%BB%AC"
driver.get(url)

#전체->뮤지컬 탭으로 전환
driver.find_element_by_css_selector("button.filterBtn").click()
driver.find_element_by_css_selector("div.subDepth.addMovies > div > button:nth-child(2)").click()
time.sleep(3)

# musical_title = driver.find_elements_by_css_selector("#root > main > section.resultZone > article.searchResultBox > div.tabContents > div.perform.active > div.active > ul > li:nth-child(1) > a > div:nth-child(2) > p.label")
# print(musical_title)


#화면 가장 아래로 스크롤하기
# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")


# while True:
#     # Scroll down to bottom
#     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

#     # Wait to load page
#     time.sleep(0.5)

#     # Calculate new scroll height and compare with last scroll height
#     new_height = driver.execute_script("return document.body.scrollHeight")
#     if new_height == last_height:
#         break
#     last_height = new_height

titles = []
tags = []
areas = []
periods= [] 
item_urls = []


content= BeautifulSoup(driver.page_source, 'html.parser')


musical_title = content.find_all("p", attrs={"class": "label"})
musical_title = content.find_all("div", attrs={"class": "active"} )

for i in range(len(musical_title)):
    titles.append(musical_title[i].get_text())

print(titles)
print(len(titles))


# for item in musical:
#     titles.append(item.find("p", attrs={"class":"label"}).get_text()) #뮤지컬 타이틀
#     # tags.append(item.find("strong", attrs={"class":"bdgeIng"}).get_text())#태그
#     # areas.append(item.find("p", attrs={"class":"place"}).get_text())#지역
#     # periods.append(item.find("p", attrs={"class":"timeContents"}).get_text())#기간
#     # item_urls.append(item.find("a").attrs['href']) # url

# print(titles)

dataframe = pd.DataFrame({'Title': titles})

# clean DataFrame
dataframe = dataframe.replace('\n', ' ', regex=True)

print(dataframe)