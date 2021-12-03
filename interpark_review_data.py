from selenium import webdriver
import time
import re
from bs4 import BeautifulSoup
import pandas as pd


data = pd.read_csv(r"musical_detailed_data.csv") # CSV 파일 불러오기(유효하지 않는 페이지는 걸러진 상태)
urls = data['URL'].values.tolist() # 리스트에 값


for url in urls[2:3]:
    # chrome 드라이버 객체 실행시키기
    driver = webdriver.Chrome(
        "/Users/dindoo/Documents/Bigdata_Musical/chromedriver")
    driver.maximize_window()
    driver.implicitly_wait(3)
    
    #url 열기
    driver.get(url)

    #팝업창 관리
    try:
        driver.find_element_by_css_selector('#popup-prdGuide > div > div.popupFooter > div > a').click()
    except:
        pass

    #title 얻기
    try:
        musical_title = driver.find_element_by_css_selector('div.productMainTop > div > div.summaryTop > h2').text
        try:  # \ / : * ? " < > | 파일 명 저장할때 조심해야하니까
            musical_title = musical_title.replace(":", " ")
            musical_title = musical_title.replace("<", " ")
            musical_title = musical_title.replace(">", " ")
            musical_title = musical_title.replace(""" " """, " ")
            musical_title = musical_title.replace("/", " ")
            musical_title = musical_title.replace("|", " ")
        except:
            continue
            
    except:
        musical_title = "NA"


    #관람 후기로 넘어가기
    driver.find_element_by_partial_link_text("관람후기").click()

    try:
        #리뷰가 있는 페이지인지 확인 역할, 없으면 리뷰가 없는 페이지 하고 종료
        driver.find_element_by_css_selector("#prdReview > div > div.bbsListWrap.reviewAll > div.pagination > ol > li").click()

        #총 페이지 수
        n=0
        while(True):
            try:
                #옆으로 이동해서 최종 페이지 확인하기
                n=n+1
                driver.find_element_by_css_selector('a.pageNextBtn.pageArrow').click()
                time.sleep(1)
                print(n)

            except:
                page_bar = driver.find_elements_by_css_selector("#prdReview > div > div.bbsListWrap.reviewAll > div.pagination > ol > li")
                last_pageNum = page_bar[-1].text
                print("최종", last_pageNum)
                break
            
        
        #이전으로 돌아가기
        driver.refresh()
        driver.find_element_by_partial_link_text("관람후기").click()

                            
        #최종 총 페이지 str -> int
        last_pageNum = int(last_pageNum)
        print(type(last_pageNum))

        #휴식
        time.sleep(3)

        
        #정보 가져오기
        review_title = []
        review_text = []
        star_rating = []
        review_id = []
        post_date = []


        # 페이지 넘기기
        for i in range(1, 2):
            #beautifulSoup
            content = BeautifulSoup(driver.page_source, 'html.parser')
            contents = content.select('li.bbsItem')
            
            for review in contents:
                time.sleep(0.5)
                #리뷰 타이틀
                try:
                    reviewTitle = review.select_one('div > div.bbsItemBody > div.bbsBodyMain > div > strong').text
                    review_title.append(reviewTitle)
                    
                    # print(reviewTitle)
                except:
                    review_title.append("NA")

                #리뷰 본문
                try:
                    time.sleep(0.5) #prdReview > div > div.bbsListWrap.reviewAll > ul > li:nth-child(5) > div > div.bbsItemBody > div.bbsBodyMain > p
                    reviewText = review.find('p', {'class':'bbsText'})
                    review_text.append(reviewText)
                except:
                    review_text.append("NA")

                #별점
                try:
                    starRating = review.select_one('div.bbsItemHead > div.leftSide > div > div.prdStarScore > span').text
                    if starRating == '평점: 실망':
                        starRating = 1
                    elif starRating == '평점: 아쉬움':
                        starRating = 2
                    elif starRating == '평점: 보통':
                        starRating = 3
                    elif starRating == '평점: 추천':
                        starRating = 4
                    elif starRating == '평점: 강력 추천':
                        starRating = 5
                    star_rating.append(starRating)

                except:
                    star_rating.append("NA")

                
                #리뷰아이디    
                try:
                    reviewId = review.select_one('div > div.bbsItemHead > div.rightSide > ul > li:nth-child(1) > span').text
                    review_id.append(reviewId)
                except:
                    review_id.append("NA")
                
                #게시 날짜
                try:
                    postDate = review.select_one('div.bbsItemHead > div.rightSide > ul > li:nth-child(2)').text
                    post_date.append(postDate)
                except:
                    post_date.append("NA")


            page_bar = driver.find_elements_by_css_selector("#prdReview > div > div.bbsListWrap.reviewAll > div.pagination > ol > li")
            i = i + 1
            try:
                if i % 10 == 0:
                    print(i)
                    driver.find_element_by_css_selector('a.pageNextBtn.pageArrow').click()
                    time.sleep(1)

                else:
                    page_bar[i % 10].click()
                    time.sleep(1)
            except:
                print("the end")
        
        #파일 저장하기(review 있는 것만)
        df = pd.DataFrame({'Review Title': review_title, 'Review Text': review_text, 'Rating Star': star_rating, 'Review Id': review_id, 'Post Date': post_date})
        df = df.replace('\n', ' ', regex=True)
        df.to_csv('/Users/dindoo/Documents/Bigdata_Musical/review_data' + '/' + musical_title +'.csv')

    except:
        print("해당 뮤지컬에는 리뷰가 없습니다.")
    


    #드라이버 종료하기
    driver.close()


