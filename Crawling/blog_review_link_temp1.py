import csv
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

# CSV 데이터 불러오기
with open('data/crawling/Seoul-all_restaurants1.csv', 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    restaurant_data = list(reader)[1:]

# 리뷰 데이터를 저장할 리스트
blog_results = []

# '더보기' 버튼을 클릭하여 모든 리뷰 로드
def load_all_reviews():
    c = 0
    while True:
        try:
            more_button = WebDriverWait(driver, 5).until(
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
    output_file = f"naver_blogs_link_2.csv"
    # 리뷰 데이터 크롤링
    for restaurant in restaurant_data:
        name, url = restaurant[0], restaurant[3]
        driver.get(url)
        print(f"크롤링 중: {restaurant[0]} - {url}")
        
        #블로그 리뷰로 전환
        blog_button = WebDriverWait(driver, 5).until(
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
                num += 1
                blog_link = WebDriverWait(driver, 3).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="app-root"]/div/div/div/div[6]/div[3]/div/div[1]/ul/li[{}]/a'.format(num)))
                )
                blog_link = blog_link.get_attribute("href")
                
                print(num, blog_link)
                with open(output_file, "a", encoding="utf-8", newline="") as file:
                    csv_writer = csv.writer(file)
                    csv_writer.writerow([restaurant[0], num, blog_link])
            except Exception:
                print(f"{restaurant[0]} - {num-1}개의 블로그 리뷰 링크 수집 완료")
                break
            
except Exception as e:
            print(e)

print(f"리뷰 크롤링 완료. 결과는 {output_file}에 저장되었습니다.")
driver.quit()