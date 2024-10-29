import os

import requests
from dotenv import load_dotenv

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time, os

import utils.crawler.blog_content
from utils.crawler.blog_content import get_blog_content_data, get_article_writer_id
from utils.crawler.blog_meta import get_blog_meta_data
from utils.crawler.blogger_meta import get_blogger_meta_data
from utils.search import search_urls

# url: 네이버 블로그 링크
chrome_options = Options()
chrome_options.add_argument("--headless")  # 헤드리스 모드
chrome_options.add_argument("--no-sandbox")  # 샌드박스 모드 비활성화
chrome_options.add_argument("--disable-dev-shm-usage")  # /dev/shm 사용 안 함 (Docker에서 메모리 문제 해결)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)


# .env 파일에서 API 인증 정보 로드
load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

# 블로그 링크 추출 : 일단 3개 -> 실제 크롤링 시 display 숫자 조정
def get_blog_links(keyword):
    # 검색어 설정 및 API 요청
    url = "https://openapi.naver.com/v1/search/blog.json"
    headers = {
        "X-Naver-Client-Id": client_id,
        "X-Naver-Client-Secret": client_secret
    }
    params = {
        "query": keyword,
        "display":3,
        "start": 1,
        "sort": "sim"
    }

    response = requests.get(url, headers=headers, params=params)
    blog_links = []

    # 블로그 글 링크 추출
    if response.status_code == 200:
        data = response.json()
        for item in data['items']:
            # title = item['title'].replace("<b>", "").replace("</b>", "")
            link = item['link']
            blog_links.append(link)
            print(f"링크 : {link}")
    else:
        print(f"Error Code: {response.status_code}")

    return blog_links

try:
    keyword = "맛집 리뷰"
    urls = get_blog_links(keyword)
    for url in urls:
        # 추출한 블로그 링크로 3 종류 데이터 추출

        # 0. 블로그 사용자 id
        blog_id, writer_id = get_article_writer_id(url)

        # 1. blog_content : 포스트 컨텐츠 데이터 (포스트 내 이미지 개수, 포스트 내 이모지 개수는 여기서 크롤링함 !)
        title, text_save_path, img_save_dir, img_cnt, emoji_cnt = get_blog_content_data(url, driver)
        print("******* title, text_save_path, img_save_dir, img_cnt, emoji_cnt : ", title, text_save_path, img_save_dir, img_cnt, emoji_cnt)

        # 2. blog_meta_data : 포스트 메타 데이터
        like_cnt, comment_cnt = get_blog_meta_data(url, driver)
        print("******* like_cnt, comment_cnt : ", like_cnt, comment_cnt)

        # 3. blogger_meta : 블로거 메타 데이터
        intro, banner, neighbor_cnt, menu_cnt, post_in_menu_number = get_blogger_meta_data(url, driver)
        print("******* intro, banner, neighbor_cnt, menu_cnt, post_in_menu_number : ", like_cnt, comment_cnt)

        # 크롤링한 데이터들 모아서 csv 파일로 생성

finally:
    driver.quit()


























