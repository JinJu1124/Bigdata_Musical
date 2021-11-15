from selenium import webdriver

#chrome 드라이버 객체 실행시키기
browser = webdriver.Chrome("/Users/dindoo/Documents/Bigdata_Musical/chromedriver")
browser.maximize_window()

#홈페이지 열기 interpark 뮤지컬 티켓 부분
url = "https://mobileticket.interpark.com/search/result?keyword=%EB%AE%A4%EC%A7%80%EC%BB%AC"
browser.get(url)

#전체->뮤지컬 탭으로 전환
browser.find_element_by_css_selector("button.filterBtn").click()
browser.find_element_by_css_selector("div.subDepth.addMovies > div > button:nth-child(2)").click()



#화면 가장 아래로 스크롤하기
# browser.execute_script("window.scrollTo(0,2800)")