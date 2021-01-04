import csv, io, time, os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium import webdriver

def tourReview():
    f = open("../review.csv", "w", encoding='UTF-8', newline ="")
    writer= csv.writer(f)

    delay = 30
    browser = webdriver.Chrome("chromedriver")
    browser.implicitly_wait(delay)
    base_url = "https://www.tripadvisor.com/"
    keywords = ["Cheonggyecheon","Myeongdong Shopping Street","Gyeongbokgung Palace","N Seoul Tower","Insadong","Namdaemun market","seoul city wall trail","Dongdaemon Design Plaza(DDP)","Hongik University"]

    for keyword in keywords:
        browser.get(base_url)
        time.sleep(3)
        # 화면 비율 설정 browser.execute_script("document.body.style.zoom='67%'")
        # 메인에서 검색 input 클릭
        search_btn = browser.find_element_by_css_selector("#lithium-root > main > div.U2O9sR7- > div > div > div._12nbOYJX > div._3-KjE8YR > div > form > input._3qLQ-U8m")
        search_btn.click()
        # browser.execute_script("arguments[0].click();", search_btn)
        search_btn.send_keys(keyword)
        search_btn.send_keys(Keys.RETURN)
        time.sleep(3)
        search_result = browser.find_element_by_css_selector("#BODY_BLOCK_JQUERY_REFLOW > div.page > div > div.ui_container.main_wrap > div > div > div > div > div.content_column.ui_column.is-9-desktop.is-12-tablet.is-12-mobile > div > div.ui_columns.sections_wrapper > div > div:nth-child(4) > div > div.main_content.ui_column.is-12 > div > div:nth-child(2) > div > div > div:nth-child(1) > div > div > div")
        search_result.click()
        browser.switch_to.window(browser.window_handles[1])
        # 브라우저 현재 위치 반환
        # print(browser.current_url)
        # 페이지 리뷰 중 좋은 리뷰들 선택 및 클릭
        excellent_label = browser.find_element_by_css_selector("div.Z78qJt1n > div:nth-child(1) > div.ui_column.is-5.is-12-mobile > ul > li:nth-child(1) > label")
        very_good_label = browser.find_element_by_css_selector("div.Z78qJt1n > div:nth-child(1) > div.ui_column.is-5.is-12-mobile > ul > li:nth-child(2) > label")
        Average_label = browser.find_element_by_css_selector("div.Z78qJt1n > div:nth-child(1) > div.ui_column.is-5.is-12-mobile > ul > li:nth-child(3) > label")
        excellent_label.click()
        time.sleep(1)
        very_good_label.click()
        time.sleep(1)
        Average_label.click()
        time.sleep(1)
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

                writer.writerow([keyword,_info_title, _info_text, _visit_content, _score])
                review += 1
                container += 1
            page += 1
            page_btn = browser.find_element_by_css_selector("._16gKMTFp > div > div > a:nth-child(%d)" % page)
            page_btn.click()
            time.sleep(1)
        
        browser.close()
        browser.switch_to.window(browser.window_handles[0])
        print(keyword,": 완료")
            
    f.close()
    browser.close()
    
tourReview()
