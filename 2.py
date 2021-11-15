import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import pymysql
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('mysql+pymysql://root:qlqjs99!@localhost/prac')
engine.connect()
Base = declarative_base()
Session = sessionmaker(bind=engine) 

driver = webdriver.Chrome("C:/Users/82107/Desktop/chromedriver.exe") # webdirver.Chrome("경로(한글X)")

driver.get('https://www.agoda.com/ko-kr/pages/agoda/default/DestinationSearchResult.aspx?asq=rp7c5epycLthZ0hHoORGnpufa9Vwpz6XltTHq4n%2B9gN3dKLJ2CSXy2MFQ4mXIPMkG8mkPiCChFumqFZwERSiKVCFcPsjdKRWeTMp2t6jQpMNYJ%2FcCWv%2F24SObsMFxXBeq%2F%2BbkS51iQs%2FzvQsTUxKZQ%2Foa8qaSyQrg61mdIzB86KPzSkK9fKrnjwxW6q6lPcIzPx3p8UWZS2iN1I3SW%2BqojVI1hfLTktOcN3QfCrx%2FY0%3D&city=16901&cid=1732639&tag=a85f57f6-f4b0-5117-39ff-f69b8b36db1a&gclid=Cj0KCQjwkIzlBRDzARIsABgXqV9474e-pU1st8ZdlFWySlL168eYxXpRblOaoy9bxbsHGkWD5Xwh6eUaAtLFEALw_wcB&tick=636898847383&isdym=true&searchterm=%EC%A0%9C%EC%A3%BC%EB%8F%84%EB%8F%84&txtuuid=62401b76-c320-499e-81f9-ce04e8f77881&languageId=9&userId=d668e3a1-5c83-493c-9b69-118608c89cab&sessionId=4fjgaxujjqkkm4i0l24hq2g2&pageTypeId=1&origin=KR&locale=ko-KR&aid=81837&currencyCode=KRW&htmlLanguage=ko-kr&cultureInfoName=ko-KR&ckuid=d668e3a1-5c83-493c-9b69-118608c89cab&prid=0&checkIn=2019-04-12&checkOut=2019-04-13&rooms=1&adults=2&children=0&priceCur=KRW&los=1&textToSearch=%EC%A0%9C%EC%A3%BC%EB%8F%84%EB%8F%84&productType=-1&travellerType=1&familyMode=off')
sleep(5) # sleep은 코드를 중지시키는 거임-> 코드가 실행되는 속도가 웹이 실행되는 속도보다 빠르니까!

driver.find_element_by_class_name('CalendarAlertMessage__close').click()  #'날짜를 선택하세요'창을 닫아주는 것-> 나중에하기 자동으로 눌러주게 코드 작성
sleep(1)

driver.find_element_by_css_selector("a[data-element-name='search-sort-price']").click() #낮은 요금으로 정렬
sleep(5)
 
actions = ActionChains(driver) #ActionChains import한 것을 내 drive에 엮어줌
last_height = driver.execute_script("return document.body.scrollHeight") #처음에 로딩됐을때 길이를 string으로 받아옴 -> driver을 통해 받아옴

while True:
    for _ in range(15):
        actions.send_keys(Keys.SPACE).perform() # keys라는 모듈로 space찾아 눌러줌(15번 반복)
        sleep(1)
    new_height = driver.execute_script("return document.body.scrollHeight") # 스크롤 길이를 다시 받아옴
    if new_height == last_height:  # 끝까지 다 로딩이 되면 멈춤
        break
    last_height = new_height

print("loading complete") 
driver.execute_script("window.scrollTo(0, 0);")
sleep(1)

content= BeautifulSoup(driver.page_source, 'html.parser')
list_items = content.findAll('li', {'class':["PropertyCardItem", "ssr-search-result"]})

class Hotel(Base):

    __tablename__ = 'newhotels'

    #id = Column(Integer, Sequence('hotel_id_seq'), primary_key=True)
    name = Column(String(30), primary_key=True)
    price = Column(String(10))

    def __init__(self,name,price):
        self.name = name
        self.price = price


    def __repr__(self):
        # id = ""
        # if self.id is not None:
        #     id = str(self.id)
        # else:
        #     id = "None"
        return str(self)

hotels = []
for item in list_items:
    hotel_name = item.find('h3', class_="InfoBox__HotelTitle")
    price = item.find('span', class_='price-box__price__amount')
   
    if hotel_name is not None and price is not None:
        new_hotel_data = Hotel(hotel_name.text, price.text)
        hotels.append(new_hotel_data)

print(hotels)
sleep(5)
driver.quit()


session = Session()

for i in range(len(hotels)):
    session.add(hotels[i])

Base.metadata.create_all(engine)
session.commit()

temp = session.query(Hotel).all()
print(temp)

# for item in temp:
#     session.delete(item)

# temp = session.query(Hotel).all()
# print(temp)
