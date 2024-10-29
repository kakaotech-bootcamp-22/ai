# api로 url 가져오는 부분

"""
검색 키워드 기반으로 블로그 링크 모음을 가져오는 코드
# 참고자료 : https://developer-woo.tistory.com/60
"""

from bs4 import BeautifulSoup

import requests
import re
import time
import urllib.request
import json
import os
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv
from selenium.webdriver.chrome.service import Service
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

#
def update_url_type_param(url, new_type_value):
    # URL을 파싱
    parsed_url = urlparse(url)
    # 쿼리 파라미터를 딕셔너리로 변환
    query_params = parse_qs(parsed_url.query)
    # 'type' 파라미터를 새로운 값으로 변경
    query_params['type'] = new_type_value
    # 수정된 쿼리 문자열 만들기
    new_query = urlencode(query_params, doseq=True)
    # 수정된 URL 만들기
    updated_url = urlunparse(parsed_url._replace(query=new_query))
    return updated_url

"""# 사용 예시
url = "https://postfiles.pstatic.net/MjAyNDA5MjlfMTgx/MDAxNzI3NTM2NDc0OTM2.p031lLK2gHsYiZvhFQdKGe-5sOsVXrJ6Z0CNZyEE7fog.18FIL6uMT0CQ8F3EWu3Ib0hlMJau-E7ODBU_LNVTzQog.JPEG/IMG_2172.jpg?type=w80_blur"
new_type_value = "w100"  # 원하는 값으로 변경
updated_url = update_url_type_param(url, new_type_value)
print(updated_url)"""


def search_urls(keyword):
    load_dotenv()
    # Naver API key 입력
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")

    # 웹드라이버 설정
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    driver = webdriver.Chrome(service= Service(ChromeDriverManager().install())) # 버전에 상관 없이 os에 설치된 크롬 브라우저 사용
    driver.implicitly_wait(3)


    # 검색어 입력
    #keyword = input("검색할 키워드를 입력해주세요:") # 추후 수정 - 함수 인자로 받아오도록
    encText = urllib.parse.quote(keyword)

    end = 1 # 페이지 수 설정
    display = 10 # 한번에 가져올 페이지 입력

    """# 검색을 끝낼 페이지 입력
    end = input("\n크롤링을 끝낼 위치를 입력해주세요. (기본값:1, 최대값:100):")
    if end == "":
        end = 1
    else:
        end = int(end)
    print("\n 1 ~ ", end, "페이지 까지 크롤링을 진행 합니다")"""

    """# 한번에 가져올 페이지 입력
    display = input("\n한번에 가져올 페이지 개수를 입력해주세요.(기본값:10, 최대값: 100):")
    if display == "":
        display = 10
    else:
        display = int(display)
    print("\n한번에 가져올 페이지 : ", display, "페이지")"""

    # selenium으로 검색 페이지 불러오기 #
    naver_urls = []  # 블로그 URL
    postdates = []    # 블로그글 포스트된 날짜
    titles = []      # 블로그 글 타이틀
    article_ids = [] # 블로그 글 번호
    user_id = [] # 블로그 유저 아이디

    for start in range(end):
        url = "https://openapi.naver.com/v1/search/blog?query=" + encText + "&start=" + str(
            start + 1) + "&display=" + str(display + 1)  # JSON 결과
        request = urllib.request.Request(url)
        request.add_header("X-Naver-Client-Id", client_id)
        request.add_header("X-Naver-Client-Secret", client_secret)
        response = urllib.request.urlopen(request)
        rescode = response.getcode()
        if (rescode == 200):
            response_body = response.read()
            data = json.loads(response_body.decode('utf-8'))['items']
            for row in data:
                if ('blog.naver' in row['link']): # 네이버 블로그 글만 읽어오기
                    naver_urls.append(row['link'])
                    postdates.append(row['postdate'])

                    # 타이틀
                    title = re.sub(pattern='<[^>]*>', repl='', string=row['title']) # html 태그 제거
                    titles.append(title)
            time.sleep(2)
        else:
            print("Error Code:" + rescode)
    """# 이미지 데이터 수집
    for i in range(len(naver_urls)):
        print(f'{titles[i]}\n({postdates[i]}): {naver_urls[i]}\n\n')"""

    return naver_urls

if __name__ == "__main__":
    search_urls(keyword = "판교 맛집")
