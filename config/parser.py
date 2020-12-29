import requests
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
import os
import csv, io
import re
# Python이 실행될 때 DJANGO_SETTINGS_MODULE이라는 환경 변수에 현재 프로젝트의 settings.py파일 경로를 등록합니다.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
# 이제 장고를 가져와 장고 프로젝트를 사용할 수 있도록 환경을 만듭니다.
# import pandas as pd
import django
django.setup()

from map.models import YoutubeData, Place, Seoul_detail, detail_route, TourReview




def savevideo():
    delay = 30
    browser = Chrome("C:\\Users\\User\\Desktop\\boyage  seoul\\config\\chromedriver.exe")
    browser.implicitly_wait(delay)
    places = Place.objects.all()
    for place in places:
        base_url = 'https://www.youtube.com/results?search_query=' + place.name  + '&sp=CAMSAggF'
        browser.get(base_url)
        browser.execute_script("window.scrollTo(0,312)")

        for j in range(1, 6):

            img_xpath = '/html/body/ytd-app/div/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-video-renderer['+ str(j) +']/div[1]/ytd-thumbnail/a/yt-img-shadow/img'
            title_xpath = '/html/body/ytd-app/div/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-video-renderer['+ str(j) +']/div[1]/div/div[1]/div/h3/a/yt-formatted-string'
            link_xpath = '/html/body/ytd-app/div/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-video-renderer[' + str(j) + ']/div[1]/ytd-thumbnail/a'

            # 썸네일 주소를 리스트에 저장
            image = browser.find_element_by_xpath(img_xpath)
            img_url = image.get_attribute('src')
            # if img_url == '' :
            #     body = browser.find_element_by_xpath('/html/body')
            #     body.Keys()

            # 타이틀을 리스트에 저장
            title = browser.find_element_by_xpath(title_xpath)

            # 링크
            link = browser.find_element_by_xpath(link_xpath)
            link_url = link.get_attribute('href')

            YoutubeData.objects.update_or_create(place=(Place(pk=place.id)),
                        title=title.text,
                        link=link_url,
                        thumb=img_url)



def seoul_data():
    # 각 지역 명소 정보 저장
    file = open('placeinfo.csv', 'r', encoding='UTF8')
    dataset = file.read()
    io_string = io.StringIO(dataset)

    _read = csv.reader(io_string, delimiter=',')
    next(_read)
    for column in _read:
        print(column)
        _, created = Seoul_detail.objects.update_or_create(
            place=Place.objects.get(name=column[0]),
            name=column[1],
            url=column[2],
            photo=column[3],
            marker_thum=column[4],
            lat=column[5],
            lng=column[6],
        )


def seoul_route():
    file = open('1Place.csv', 'r', encoding='UTF8')
    dataset = file.read()
    io_string = io.StringIO(dataset)

    # next(io_string)
    for column in csv.reader(io_string, delimiter=','):
        _, created = detail_route.objects.update_or_create(
            place=column[0],
            lat=column[1],
            lng=column[2],
        )

def tourReview():
    delay = 30
    browser = Chrome("C:\\Users\\User\\Desktop\\boyage  seoul\\config\\chromedriver.exe")
    browser.implicitly_wait(delay)
    base_url = "https://www.tripadvisor.com/"
    places = Place.objects.all()

    for place in places:
        # 검색 용어 설정 및 base_Url 이동
        keyword = "Myeongdong Shopping Street"
        # keyword = place.name
        browser.get(base_url)
        time.sleep(1)
        # 화면 비율 설정 browser.execute_script("document.body.style.zoom='67%'")
        # 메인에서 검색 input 클릭
        search_btn = browser.find_element_by_css_selector("#lithium-root > main > div.U2O9sR7- > div > div > div._12nbOYJX > div._3-KjE8YR > div > form > input._3qLQ-U8m")
        search_btn.click()
        # browser.execute_script("arguments[0].click();", search_btn)
        search_btn.send_keys(keyword)
        search_btn.send_keys(Keys.RETURN)
        time.sleep(4)
        search_result = browser.find_element_by_css_selector("#BODY_BLOCK_JQUERY_REFLOW > div.page > div > div.ui_container.main_wrap > div > div > div > div > div.content_column.ui_column.is-9-desktop.is-12-tablet.is-12-mobile > div > div.ui_columns.sections_wrapper > div > div:nth-child(4) > div > div.main_content.ui_column.is-12 > div > div:nth-child(2) > div > div > div:nth-child(1) > div > div > div")
        search_result.click()
        browser.switch_to.window(browser.window_handles[1])

        # 브라우저 현재 위치 반환
        # print(browser.current_url)
        P = Place.objects.get(name=keyword)
        P.trip_url = browser.current_url
        P.save()
        # 페이지 리뷰 중 좋은 리뷰들 선택 및 클릭
        excellent_label = browser.find_element_by_css_selector("div.Z78qJt1n > div:nth-child(1) > div.ui_column.is-5.is-12-mobile > ul > li:nth-child(1) > label")
        very_good_label = browser.find_element_by_css_selector("div.Z78qJt1n > div:nth-child(1) > div.ui_column.is-5.is-12-mobile > ul > li:nth-child(2) > label")
        Average_label = browser.find_element_by_css_selector("div.Z78qJt1n > div:nth-child(1) > div.ui_column.is-5.is-12-mobile > ul > li:nth-child(3) > label")
        excellent_label.click()
        very_good_label.click()
        Average_label.click()
        time.sleep(3)
        # 리뷰 긁기
        page = 1
        review = 0
        while(page<4):
            container = 0
            review_container = browser.find_elements_by_class_name("Dq9MAugU")
            while(container <5):
                # 리뷰 점수
                review_code = review_container[container].find_element_by_css_selector(".ui_bubble_rating")
                cls_data = str(review_code.get_attribute("class")).split("ui_bubble_rating bubble_")

                #리뷰 내용 긁기
                try:
                    visit_text = str(review_container[container].find_element_by_class_name("_34Xs-BQm").text).split("Date of experience: ")
                except:
                    pass
                read_more = review_container[container].find_element_by_css_selector("div.XUVJZtom")

                browser.execute_script("arguments[0].click();", read_more)

                _info_title = review_container[container].find_element_by_css_selector("div.oETBfkHU > div.glasR4aX > a").text
                _info_text = review_container[container].find_element_by_css_selector("q.IRsGHoPm > span").text
                _visit_content = visit_text[1]
                _score = int(cls_data[1])

                model = TourReview.objects.update_or_create(
                    place = Place.objects.get(name=keyword),
                    info_title = _info_title,
                    info = _info_text,
                    score = _score ,
                    visit_date = _visit_content
                )

                review += 1
                container += 1

            page += 1
            page_btn = browser.find_element_by_css_selector("._16gKMTFp > div > div > a:nth-child(%d)" % page)
            page_btn.click()
            time.sleep(1)


        browser.close()
        browser.switch_to.window(browser.window_handles[0])


seoul_data()



# img = WebDriverWait(browser, 20).until(EC.presence_of_all_elements_located((By.XPATH, img_xpath)))

# if img is None:
#     print(idx, 'img is not loaded.')

# if idx % 8 == 0 :
#     browser.execute_script('window.scrollBy(0, 1080);')
#     time.sleep(2)
#     browser.execute_script('window.scrollBy(0, 1080);')
#     time.sleep(2)
#     browser.execute_script('window.scrollBy(0, 1080);')
#     time.sleep(2)
