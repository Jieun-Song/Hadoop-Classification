import json
import csv

with open("naver_blogs_detail_A_20241202_120729.json", "r", encoding="utf-8") as a, \
    open("naver_blogs_detail_B_20241202_121126.json", "r", encoding="utf-8") as b, \
    open("naver_blogs_detail_C_20241202_121313.json", "r", encoding="utf-8") as c, \
    open("naver_blogs_detail_D_20241202_121541.json", "r", encoding="utf-8") as d, \
    open("naver_blogs_detail_E_20241202_121830.json", "r", encoding="utf-8") as e, \
    open('./data/crawling/서대문_navermap_blog_review.csv', 'w', newline = '',encoding = 'utf-8') as output_file:
    data_A = json.load(a)
    data_B = json.load(b)
    data_C = json.load(c)
    data_D = json.load(d)
    data_E = json.load(e)

    data = data_A+data_B+data_C+data_D+data_E

    f = csv.writer(output_file)
    f.writerow(["Title","Content"])

    for line in data:
        f.writerow([line["가게 이름"], line["리뷰 내용"]])

print("done")