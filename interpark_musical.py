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
    titles.append(p.find_element_by_class_name('itemName').text) #뮤지컬 제목
    areas.append(p.find_element_by_class_name('area').text)
    periods.append(p.find_element_by_class_name('period').text)
    item_urls.append(p.get_attribute('href'))


#종료하기
driver.close()

df = pd.DataFrame({'title':titles, 'Area': areas, 'Period': periods, 'URL': item_urls})
# df = pd.DataFrame({'title':titles})
print(df)


#ticketContent > div > div.searchPanel > ul > li:nth-child(1)


# for item in items : 
#     titles.append(item.find("div", attrs={"class":"itemName"}).get_text())

# items = content.select(re.compile("categoryContent current$"))
# items = content.select('div.categoryContent current > div.ticketContent > div.searchPanel > ul.itemList')




# # for item in items:
# #     titles.append(item.find("div", attrs={"class":"itemName"}).get_text()) #뮤지컬 타이틀
# #     tags.append(item.find("div", attrs={"class":"tags"}).get_text())#태그
# #     areas.append(item.find("span", attrs={"class":"area"}).get_text())#지역
# #     periods.append(item.find("span", attrs={"class":"period"}).get_text())#기간
# #     item_urls.append(item.find("a").attrs['href']) # url




# dataframe = pd.DataFrame({'Title': titles, 'Tag': tags, 'Area': areas, 'Period': periods, 'URL': item_urls})

# # clean DataFrame
# dataframe = dataframe.replace('\n', ' ', regex=True)
# print(len(titles))
# print(dataframe)