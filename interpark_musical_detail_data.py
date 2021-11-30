from selenium import webdriver
import time
import re
from bs4 import BeautifulSoup
import pandas as pd


# chrome 드라이버 객체 실행시키기
driver = webdriver.Chrome(
    "/Users/dindoo/Documents/Bigdata_Musical/chromedriver")
driver.maximize_window()

data = pd.read_csv(r"musical_data.csv")  # CSV 파일 불러오기
urls = data['URL'].values.tolist()  # 리스트에 값

titles = []
musical_times = []
ages = []
places = []
periods = []
URLs = []
genre = []
like_sex_m = []
like_sex_w = []
like_age_1 = []
like_age_2 = []
like_age_3 = []
like_age_4 = []
like_age_5 = []
ticketCast = []
musical_status = []
error_page = []


# url 리스트 돌며 페이지 열기(sample 10개)
# i = 0
for url in urls:
    # i = i+1  # 브레이크용도
    # url 열기
    try:
        driver.get(url)
    
    # 쉬기
        driver.implicitly_wait(10)

    # 판매취소 작품 거르기
        try:
            status = driver.find_element_by_css_selector(
                '#productSide > div > div.sideMain > div > div > div > div > strong').text
            if status == '판매취소':
                title = driver.find_element_by_css_selector(
                    'div.productMainTop > div > div.summaryTop > h2').text
                musical_status.append(status) 
                genre.append(driver.find_element_by_css_selector('#container > div.contents > div.productWrapper > div.productMain > div.productMainTop > div > div.summaryTop > div.tag > div.tagText > span').text)
                musical_times.append("NA")
                ages.append("NA")
                places.append("NA")
                periods.append("NA")
                like_sex_m.append("NA")
                like_sex_w.append("NA")
                like_age_1.append("NA")
                like_age_2.append("NA")
                like_age_3.append("NA")
                like_age_4.append("NA")
                like_age_5.append("NA")
                ticketCast.append("NA")
                URLs.append(url)
                titles.append(title)
                print('판매 취소 : ', title)
            
            else:
                title = driver.find_element_by_css_selector(
                    'div.productMainTop > div > div.summaryTop > h2').text
                titles.append(title)
                genre.append(driver.find_element_by_css_selector('#container > div.contents > div.productWrapper > div.productMain > div.productMainTop > div > div.summaryTop > div.tag > div.tagText > span').text)
                URLs.append(url)

                # status
                musical_status.append('판매종료')

                # 장소
                try:
                    places.append(driver.find_element_by_css_selector(
                    'div.summaryBody > ul > li:nth-child(1) > div > a').text)
                except:
                    places.append("NA")

                # 공연 시간
                try:
                    musical_times.append(driver.find_element_by_css_selector(
                        'div.summaryBody > ul > li:nth-child(2) > div > p').text)
                except:
                    musical_times.append("NA")

                # 공연 기간
                try:
                    periods.append(driver.find_element_by_css_selector(
                        'div.summaryBody > ul > li:nth-child(2) > div > p').text)
                except:
                    periods.append("NA")

                # 관람 연령
                try:
                    ages.append(driver.find_element_by_css_selector(
                        'div.summaryBody > ul > li:nth-child(4) > div > p').text)
                except:
                    ages.append("NA")

                # 선호 성별
                try:
                    like_sex_m.append(driver.find_element_by_css_selector(
                        'div.statGenderType.is-male > div.statGenderValue').text)  # 남
                except:
                    like_sex_m.append("NA")
                try:
                    like_sex_w.append(driver.find_element_by_css_selector(
                        'div.statGenderType.is-female > div.statGenderValue').text)  # 녀
                except:
                    like_sex_w.append("NA")

                # 선호 연령
                try:
                    like_age_1.append(driver.find_element_by_css_selector(
                        'div.statAge > div > div:nth-child(1) > div.statAgePercent').text)  # 10대
                except:
                    like_age_1.append("NA")
                try:
                    like_age_2.append(driver.find_element_by_css_selector(
                        'div.statAge > div > div:nth-child(2) > div.statAgePercent').text)  # 20대
                except:
                    like_age_2.append("NA")
                try:
                    like_age_3.append(driver.find_element_by_css_selector(
                        'div.statAge > div > div:nth-child(3) > div.statAgePercent').text)  # 30대
                except:
                    like_age_3.append("NA")
                try:
                    like_age_4.append(driver.find_element_by_css_selector(
                        'div.statAge > div > div:nth-child(4) > div.statAgePercent').text)  # 40대
                except:
                    like_age_4.append("NA")
                try:
                    like_age_5.append(driver.find_element_by_css_selector(
                        'div.statAge > div > div:nth-child(5) > div.statAgePercent').text)  # 50대
                except:
                    like_age_5.append("NA")

                # 티켓캐스트
                try:
                    ticketCast.append(driver.find_element_by_css_selector(
                        'div.summaryBody > div > div.posterBoxBottom > div.prdCast > p').text)
                except:
                    ticketCast.append("NA")
        
        except:
            print("성공")
            title = driver.find_element_by_css_selector(
                'div.productMainTop > div > div.summaryTop > h2').text
            titles.append(title)
            genre.append(driver.find_element_by_css_selector('#container > div.contents > div.productWrapper > div.productMain > div.productMainTop > div > div.summaryTop > div.tag > div.tagText > span').text)
            URLs.append(url)

            # status
            musical_status.append('판매예정/판매중')

            # 장소
            try:
                places.append(driver.find_element_by_css_selector(
                'div.summaryBody > ul > li:nth-child(1) > div > a').text)
            except:
                places.append("NA")

            # 공연 시간
            try:
                musical_times.append(driver.find_element_by_css_selector(
                    'div.summaryBody > ul > li:nth-child(2) > div > p').text)
            except:
                musical_times.append("NA")

            # 공연 기간
            try:
                periods.append(driver.find_element_by_css_selector(
                    'div.summaryBody > ul > li:nth-child(2) > div > p').text)
            except:
                periods.append("NA")

            # 관람 연령
            try:
                ages.append(driver.find_element_by_css_selector(
                    'div.summaryBody > ul > li:nth-child(4) > div > p').text)
            except:
                ages.append("NA")

            # 선호 성별
            try:
                like_sex_m.append(driver.find_element_by_css_selector(
                    'div.statGenderType.is-male > div.statGenderValue').text)  # 남
            except:
                like_sex_m.append("NA")
            try:
                like_sex_w.append(driver.find_element_by_css_selector(
                    'div.statGenderType.is-female > div.statGenderValue').text)  # 녀
            except:
                like_sex_w.append("NA")

            # 선호 연령
            try:
                like_age_1.append(driver.find_element_by_css_selector(
                    'div.statAge > div > div:nth-child(1) > div.statAgePercent').text)  # 10대
            except:
                like_age_1.append("NA")
            try:
                like_age_2.append(driver.find_element_by_css_selector(
                    'div.statAge > div > div:nth-child(2) > div.statAgePercent').text)  # 20대
            except:
                like_age_2.append("NA")
            try:
                like_age_3.append(driver.find_element_by_css_selector(
                    'div.statAge > div > div:nth-child(3) > div.statAgePercent').text)  # 30대
            except:
                like_age_3.append("NA")
            try:
                like_age_4.append(driver.find_element_by_css_selector(
                    'div.statAge > div > div:nth-child(4) > div.statAgePercent').text)  # 40대
            except:
                like_age_4.append("NA")
            try:
                like_age_5.append(driver.find_element_by_css_selector(
                    'div.statAge > div > div:nth-child(5) > div.statAgePercent').text)  # 50대
            except:
                like_age_5.append("NA")

            # 티켓캐스트
            try:
                ticketCast.append(driver.find_element_by_css_selector(
                    'div.summaryBody > div > div.posterBoxBottom > div.prdCast > p').text)
            except:
                ticketCast.append("NA")
        
    except:
        print("유효하지 않는 페이지 : ",url)
        print('주의! 페이지가 유효하지 않습니다.')
        error_page.append(url)
        continue
        # # url sample을 위한 브레이크
    # if i == 10:
    #     break

df = pd.DataFrame({'Title': titles, 'Genre' : genre, 'Place': places, 'Time': musical_times, 'Age': ages, 'Period': periods,
                   'TicketCast': ticketCast, 'Like_man': like_sex_m, 'Like_woman': like_sex_w,
                   'Like_age_10': like_age_1, 'Like_age_20': like_age_2, 'Like_age_30': like_age_3, 'Like_age_40': like_age_4, 'Like_age_50': like_age_5, 'URL': URLs,
                   'Status': musical_status})

df = df.replace('\n', ' ', regex=True)
df.to_csv('musical_detailed_data.csv')
print(df)
print(error_page)

# 종료하기
driver.close()
