from selenium import webdriver
import time

#chrome 드라이버 객체 실행시키기
driver = webdriver.Chrome("/Users/dindoo/Documents/Bigdata_Musical/chromedriver")
driver.maximize_window()

#홈페이지 열기 interpark 뮤지컬 티켓 부분
url = "https://tickets.interpark.com/search?keyword=%EB%AE%A4%EC%A7%80%EC%BB%AC"
driver.get(url)

print("+"*100)
print("interpark 뮤지컬 크롤링")
print("+"*100)

#티켓 카테고리로 넘어가기
driver.find_element_by_css_selector("#allContent > div.ticketContent > div.searchHeader > a").click()
time.sleep(3)

#종료하기
driver.close()
