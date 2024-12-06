import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import requests
import re
import random


# WebDriver 설정
options = webdriver.ChromeOptions()
options.add_argument("window-size=1920x1080")
options.add_argument("--disable-blink-features=AutomationControlled")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

input_file = "naver_blogs_link.csv"
output_file = "naver_blogs_detail_0.csv"

# csv 데이터 불러오기
with open(input_file, "r", encoding="utf-8") as file:
    blog_link_data = list(csv.reader(file))

blog_results = []

def no_space(text):
    text = re.sub(r'(&nbsp;|\n|\t|\r)+', '', text)
    return text

try:
    # 리뷰 데이터 크롤링
    for blog_link in blog_link_data:
        url = blog_link[2]
        # 카페 데이터 필터링(안들어가짐 이슈)
        if url not in "cafe.naver.com":
            if "://" in url:
                m_url =url.replace("://","://m.")
            else :
                print("??",url)
            # blog.naver 의 경우 크롤링을 막아놔서 모바일 경로인 m.으로 우회
            
            print(f"크롤링 중: {blog_link[0]} - {m_url}")

            res = requests.get(m_url)
            res.raise_for_status()
            soup = BeautifulSoup(res.text, "lxml")

            try:
                blog_main = soup.find("div", attrs={'class':'se-main-container'}).text
                blog_main = no_space(blog_main)
                print(blog_main)
                # blog_results.append({
                #         "가게 이름": blog_link["가게 이름"],
                #         "리뷰 내용": blog_main
                #     })
                with open(output_file, "a", encoding="utf-8", newline="") as file:
                    csv_writer = csv.writer(file)
                    csv_writer.writerow([blog_link[0], blog_main])
            except:
                continue
        else :
            print("카페 링크 넘어감")
            continue
            
except Exception as e:
            print(e)

print(f"리뷰 크롤링 완료. 결과는 {output_file}에 저장되었습니다.")
driver.quit()