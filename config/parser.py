import requests
from selenium import webdriver
#from pyvirtualdisplay import Display
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

#display = Display(visible=0, size=(1920, 1080))
#display.start()

path = '/home/ubuntu/BOYAGE_SEOUL/config/chromedriver'


def savevideo():
    delay = 30
    browser = webdriver.Chrome(path)
    browser.implicitly_wait(delay)
    places = Place.objects.all()

    for place in places:
        if place.name == "Hongik University":
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
            print("완료")
            browser.close()
            break


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
    file = open('../review.csv', 'r')
    dataset = file.read()
    io_string = io.StringIO(dataset)

    # next(io_string)
    for column in csv.reader(io_string, delimiter=','):
        model = TourReview.objects.update_or_create(
            place = Place.objects.get(name=column[0]),
            info_title = column[1],
            info = column[2],
            score = column[4],
            visit_date =column[3],
        )
        print(column[1])


tourReview()



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
