import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import datetime as dt
import time
import random


# WebDriver 설정
options = webdriver.ChromeOptions()
options.add_argument("window-size=1920x1080")
options.add_argument("--disable-blink-features=AutomationControlled")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# JSON 데이터 불러오기
with open("data/crawling/seodaemun_restaurant_200_D.json", "r", encoding="utf-8") as file:
    restaurant_data = json.load(file)

# 리뷰 데이터를 저장할 리스트
blog_results = []

# '더보기' 버튼을 클릭하여 모든 리뷰 로드
def load_all_reviews():
    c = 0
    while True:
        try:
            more_button = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="app-root"]/div/div/div/div[6]/div[3]/div/div[2]/div/a'))
            )
            # more_button = driver.find_element(By.XPATH, '//*[@id="app-root"]/div/div/div/div[6]/div[3]/div/div[2]/div/a')
            more_button.click()
            c = c + 1
            # time.sleep(1)  # 클릭 후 로딩 시간
        except Exception:
            print("더보기 완료", c)
            break  # 더보기 버튼이 없으면 종료

try:
    # 리뷰 데이터 크롤링
    for restaurant in restaurant_data:
        url = restaurant["URL"]
        print(f"크롤링 중: {restaurant['가게 이름']} - {url}")
        driver.get(url)
        
        #블로그 리뷰로 전환
        blog_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH,'//*[@id="_subtab_view"]/div/a[2]'))
            )
        blog_button.click()

        # 페이지 스크롤로 모든 리뷰 로드
        load_all_reviews()

        time.sleep(3)
        num = 0
        # 식당의 블로그리뷰 링크들 따로 저장
        while True:
            try:
                num = num + 1
                blog_link = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="app-root"]/div/div/div/div[6]/div[3]/div/div[1]/ul/li[{}]/a'.format(num)))
                )
                blog_link = blog_link.get_attribute("href")
                print(num, blog_link)
                blog_results.append({
                        "가게 이름": restaurant["가게 이름"],
                        "번호": num,
                        "리뷰 내용": blog_link
                    })
            except Exception:
                print(f"{restaurant['가게 이름']} - {num-1}개의 블로그리뷰 링크 수집 완료")
                break
            
except Exception as e:
            print(e)

#결과를 JSON 파일로 저장
timestamp = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
output_file = f"naver_blogs_link_D_{timestamp}.json"
with open(output_file, "w", encoding="utf-8") as file:
    json.dump(blog_results, file, ensure_ascii=False, indent=4)

print(f"리뷰 크롤링 완료. 결과는 {output_file}에 저장되었습니다.")
driver.quit()