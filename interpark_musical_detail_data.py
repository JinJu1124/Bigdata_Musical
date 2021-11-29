from selenium import webdriver
import time
import re
from bs4 import BeautifulSoup
import pandas as pd


# chrome 드라이버 객체 실행시키기
driver = webdriver.Chrome(
    "/Users/dindoo/Documents/Bigdata_Musical/chromedriver")
driver.maximize_window()

data = pd.read_csv(r"musical_url.csv")  # CSV 파일 불러오기
urls = data['URL'].values.tolist()  # 리스트에 값

titles = []
musical_times = []
ages = []
places = []
periods = []
URLs = []
like_sex_m = []
like_sex_w = []
like_age_1 = []
like_age_2 = []
like_age_3 = []
like_age_4 = []
like_age_5 = []
ticketCast = []
musical_status = []


# url 리스트 돌며 페이지 열기(sample 10개)
# i = 0
for url in urls:
    # i = i+1  # 브레이크용도
    try:
        # url 열기
        driver.get(url)

        # 쉬기
        driver.implicitly_wait(10)
    
        # 제목
        titles.append(driver.find_element_by_css_selector('div.productMainTop > div > div.summaryTop > h2').text)
        
        #판매취소 작품 거르기
        try:
            status = driver.find_element_by_css_selector('#productSide > div > div.sideMain > div > div > div > div > strong').text
            if status == '판매취소':
                URLs.append(None)
                musical_status.append(status)
                musical_times.append(None)
                ages.append(None)
                places.append(None)
                periods.append(None)
                like_sex_m.append(None)
                like_sex_w.append(None)
                like_age_1.append(None)
                like_age_2.append(None)
                like_age_3.append(None)
                like_age_4.append(None)
                like_age_5.append(None)
                ticketCast.append(None)
                print('판매 취소')

        except:
            musical_status.append('판매예정/판매중/판매종료')
            # 해당 url 리스트에 저장하기
            URLs.append(url)

            # 장소
            try:
                places.append(driver.find_element_by_css_selector(
                'div.summaryBody > ul > li:nth-child(1) > div > a').text)
            except:
                places.append(None)

            # 공연 시간
            try:
                musical_times.append(driver.find_element_by_css_selector(
                    'div.summaryBody > ul > li:nth-child(2) > div > p').text)
            except:
                musical_times.append(None)

            # 공연 기간
            try:
                periods.append(driver.find_element_by_css_selector(
                    'div.summaryBody > ul > li:nth-child(2) > div > p').text)
            except:
                periods.append(None)

            # 관람 연령
            try:
                ages.append(driver.find_element_by_css_selector(
                    'div.summaryBody > ul > li:nth-child(4) > div > p').text)
            except:
                ages.append(None)
            
            # 선호 성별
            try:
                like_sex_m.append(driver.find_element_by_css_selector(
                    'div.statGenderType.is-male > div.statGenderValue').text)  # 남
            except:
                like_sex_m.append(None)
            try:
                like_sex_w.append(driver.find_element_by_css_selector(
                    'div.statGenderType.is-female > div.statGenderValue').text)  # 녀
            except:
                like_sex_w.append(None)

            # 선호 연령
            try:
                like_age_1.append(driver.find_element_by_css_selector(
                    'div.statAge > div > div:nth-child(1) > div.statAgePercent').text)  # 10대
            except:
                like_age_1.append(None)
            try:
                like_age_2.append(driver.find_element_by_css_selector(
                    'div.statAge > div > div:nth-child(2) > div.statAgePercent').text)  # 20대
            except:
                like_age_2.append(None)
            try:
                like_age_3.append(driver.find_element_by_css_selector(
                    'div.statAge > div > div:nth-child(3) > div.statAgePercent').text)  # 30대
            except:
                like_age_3.append(None)
            try:
                like_age_4.append(driver.find_element_by_css_selector(
                    'div.statAge > div > div:nth-child(4) > div.statAgePercent').text)  # 40대
            except:
                like_age_4.append(None)
            try:
                like_age_5.append(driver.find_element_by_css_selector(
                    'div.statAge > div > div:nth-child(5) > div.statAgePercent').text)  # 50대
            except:
                like_age_5.append(None)

            # 티켓캐스트
            try:
                ticketCast.append(driver.find_element_by_css_selector(
                    'div.summaryBody > div > div.posterBoxBottom > div.prdCast > p').text)
            except:
                ticketCast.append(None)
            

            
    except: #페이지가 더이상 유효하지 않을때
        titles.append(None)
        print('주의! 페이지가 유효하지 않습니다.')
    
    # url sample을 위한 브레이크
    # if i == 10:
    #     break
# print(titles, places, musical_times, ages, periods, ticketCast, like_sex_m, like_sex_w, like_age_1, like_age_2, like_age_3, like_age_4, like_age_5, URLs)
df = pd.DataFrame({'Title': titles, 'Place': places, 'Time': musical_times, 'Age': ages, 'Period': periods,
                   'TicketCast': ticketCast, 'Like_man': like_sex_m, 'Like_woman': like_sex_w,
                   'Like_age_10': like_age_1, 'Like_age_20': like_age_2, 'Like_age_30': like_age_3, 'Like_age_40': like_age_4, 'Like_age_50': like_age_5, 'URL': URLs,
                   'Status': musical_status})

df = df.replace('\n', ' ', regex=True)
print(df)
df.to_csv('musical_detailed_data.csv')

# 종료하기
driver.close()
