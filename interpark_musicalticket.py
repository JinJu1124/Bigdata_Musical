from selenium import webdriver
from bs4 import BeautifulSoup
import time
import re
import pandas as pd

#chrome 드라이버 객체 실행시키기
driver = webdriver.Chrome("/Users/dindoo/Documents/Bigdata_Musical/chromedriver")
driver.maximize_window()

#홈페이지 열기 interpark 뮤지컬 티켓 부분
url = "https://tickets.interpark.com/search?keyword=%EB%AE%A4%EC%A7%80%EC%BB%AC"
driver.get(url)

#뮤지컬 장르 탭 선택하기
driver.find_element_by_css_selector("#container > div.contents > div > div.searchResultWrap > div.resultContents > div.categoryTabWrap > div > ul > li:nth-child(2)").click()
driver.find_element_by_css_selector("#ticketContent > div > div.subCatecory > ul > li:nth-child(2)").click()
time.sleep(5)


#해당 url beautifulsoup에 가져오기
content= BeautifulSoup(driver.page_source, 'html.parser')


titles = []
tags = []
areas = []
periods= [] 
item_urls = []

for n in range(1,3):
    time.sleep(1)

    items = content.find_all("li", attrs={"data-sale": re.compile("1")})
    for item in items:
        titles.append(item.find("div", attrs={"class":"itemName"}).get_text()) #뮤지컬 타이틀
        tags.append(item.find("div", attrs={"class":"tags"}).get_text())#태그
        areas.append(item.find("span", attrs={"class":"area"}).get_text())#지역
        periods.append(item.find("span", attrs={"class":"period"}).get_text())#기간
        item_urls.append(item.find("a").attrs['href']) # url
    
    page_bar = driver.find_elements_by_css_selector("div.pagination > span > *")

    page_bar[2].click()
    # if n%10 != 0:
    #     page_bar[n%10+1].click()
    # else:
    #     page_bar[11].click()

driver.close()

dataframe = pd.DataFrame({'Title': titles, 'Tag': tags, 'Area': areas, 'Period': periods, 'URL': item_urls})

# clean DataFrame
dataframe = dataframe.replace('\n', ' ', regex=True)

print(dataframe[10:])
# # # export to excel
# # df.to_csv('jekyll.csv')

