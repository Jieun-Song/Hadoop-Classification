import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import requests
import re
import chardet

# WebDriver 설정
options = webdriver.ChromeOptions()
options.add_argument("window-size=1920x1080")
options.add_argument("--disable-blink-features=AutomationControlled")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

input_file = "naver_blogs_link_2.csv"
output_file = "naver_blogs_detail_2.csv"  # 확장자 추가

# 불필요한 공백이나 특수문자 제거하는 함수 정의
def no_space(text):
    text = re.sub(r'(&nbsp;|\n|\t|\r)+', '', text)
    return text

# 인코딩 탐지 및 파일 읽기
with open(input_file, "rb") as raw_file:
    result = chardet.detect(raw_file.read())
    detected_encoding = result['encoding']
    print(f"Detected encoding: {detected_encoding}")

with open(input_file, "r", encoding=detected_encoding, errors="replace") as file:
    blog_link_data = list(csv.reader(file))

try:
    # 리뷰 데이터 크롤링
    for blog_link in blog_link_data:
        url = blog_link[2]
        # 카페 데이터 필터링(안들어가짐 이슈)
        if "cafe.naver.com" not in url:
            if "://" in url:
                m_url = url.replace("://", "://m.")
            else:
                print("??", url)
            # blog.naver 의 경우 크롤링을 막아놔서 모바일 경로인 m.으로 우회
            
            print(f"크롤링 중: {blog_link[0]} - {m_url}")

            res = requests.get(m_url)
            res.raise_for_status()
            soup = BeautifulSoup(res.text, "lxml")

            try:
                blog_main = soup.find("div", attrs={'class': 'se-main-container'}).text
                blog_main = no_space(blog_main)
                print(blog_main)

                # 파일에 데이터 작성
                with open(output_file, "a", encoding="utf-8", newline="") as file:
                    csv_writer = csv.writer(file)
                    csv_writer.writerow([blog_link[0], blog_main])

            except Exception as e:
                print(f"Error extracting blog content: {e}")
                continue
        else:
            print("카페 링크 넘어감")
            continue
            
except Exception as e:
    print(f"전체 크롤링 중 오류: {e}")

print(f"리뷰 크롤링 완료. 결과는 {output_file}에 저장되었습니다.")
driver.quit()
