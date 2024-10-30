import requests
from dotenv import load_dotenv

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import os

from utils.crawler.blog_content_crawler import get_article_writer_id, get_blog_content_data
from utils.crawler.blog_meta_crawler import get_blog_meta_data
from utils.crawler.blogger_meta_crawler import get_blogger_meta_data

from utils.blog_links_loader import get_blog_links
from utils.html_parser import parse_html

import pandas as pd

# url: 네이버 블로그 링크
chrome_options = Options()
chrome_options.add_argument("--headless")  # 헤드리스 모드
chrome_options.add_argument("--no-sandbox")  # 샌드박스 모드 비활성화
chrome_options.add_argument("--disable-dev-shm-usage")  # /dev/shm 사용 안 함 (Docker에서 메모리 문제 해결)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)


def get_next_index(file_path):
    """파일의 마지막 인덱스 가져와 다음 인덱스 계산"""
    if os.path.exists(file_path):
        existing_df = pd.read_csv(file_path)
        if not existing_df.empty:
            return existing_df.index[-1] + 1
    return 0  # 파일이 없거나 빈 경우 1부터 시작

try:
    area_list = ['판교', "성수", "강남"]
    print("Current working MAIN directory:", os.getcwd())

    is_first = True
    for area in area_list:
        keyword = area + " 맛집 리뷰"
        print(keyword)
        print()
        urls = get_blog_links(keyword)

        for url in urls:

            # ulr 별 html 파싱
            soup = parse_html(driver, url)

            # 추출한 블로그 링크로 3 종류 데이터 추출

            # 0. 블로그 사용자 id
            blog_id, writer_id = get_article_writer_id(url)
            print(f"블로그 사용자 id  -  *블로그 id : {blog_id}  *사용자 id : {writer_id}")

            # 1. blog_content : 포스트 컨텐츠 데이터 (포스트 내 이미지 개수, 포스트 내 이모지 개수는 여기서 크롤링함 !)
            title, text_save_path, img_save_dir, img_cnt, emoji_cnt, title_len, whole_text_len = get_blog_content_data(soup, url)
            print(f"포스트 컨텐츠 데이터  -  *제목 : {title}  *본문 url : {text_save_path}   *이미지 url : {img_save_dir}    *이미지 개수 : {img_cnt}  *이모지 개수 : {emoji_cnt}")
            print(f"                    *제목 길이 : {title_len}     *본문 길이 : {whole_text_len}")

            # 2. blog_meta_data : 포스트 메타 데이터
            like_cnt, comment_cnt = get_blog_meta_data(soup)
            print(f"포스트 메타 데이터  -  *공감 수 : {like_cnt}  *댓글 수 : {comment_cnt}")

            # 3. blogger_meta : 블로거 메타 데이터
            intro, banner, neighbor_cnt, menu_cnt, post_in_menu_number = get_blogger_meta_data(soup)
            print(f"블로거 메타 데이터  -  *자기소개: {intro}  *배너 : {banner}   *이웃 수 : {neighbor_cnt}   *메뉴 개수 : {menu_cnt}  *메뉴에 속한 포스트 개수 : {post_in_menu_number}")
            print()

            # CSV 파일 생성 경로
            post_content_path = "csv_data/post_content_data.csv"
            post_meta_path = "csv_data/post_meta_data.csv"
            blogger_meta_path = "csv_data/blogger_meta_data.csv"

            # 1. 포스트 컨텐츠 데이터 저장
            post_content_data = {
                "blog_id": blog_id,
                "writer_id": writer_id,
                "title": title,
                "text_save_path": text_save_path
            }
            post_content_data_df = pd.DataFrame([post_content_data])
            post_content_data_df.index = [get_next_index(post_content_path)]  # 다음 인덱스 설정
            post_content_data_df.to_csv(post_content_path, mode='a', encoding="utf-8-sig",
                                        header=is_first, index_label="Index")

            # 2. 포스트 메타 데이터 저장
            post_meta_data = {
                "blog_id": blog_id,
                "writer_id": writer_id,
                "title_len": title_len,
                "whole_text_len": whole_text_len,
                "img_save_dir": img_save_dir,
                "img_cnt": img_cnt,
                "emoji_cnt": emoji_cnt,
                "like_cnt": like_cnt,
                "comment_cnt": comment_cnt
            }
            post_meta_data_df = pd.DataFrame([post_meta_data])
            post_meta_data_df.index = [get_next_index(post_meta_path)]  # 다음 인덱스 설정
            post_meta_data_df.to_csv(post_meta_path, mode='a', encoding="utf-8-sig",
                                     header=is_first, index_label="Index")

            # 3. 블로거 메타 데이터 저장
            blogger_meta_data = {
                "blog_id": blog_id,
                "writer_id": writer_id,
                "intro": intro,
                "banner": banner,
                "neighbor_cnt": neighbor_cnt,
                "menu_cnt": menu_cnt,
                "post_in_menu_number": post_in_menu_number
            }
            blogger_meta_data_df = pd.DataFrame([blogger_meta_data])
            blogger_meta_data_df.index = [get_next_index(blogger_meta_path)]  # 다음 인덱스 설정
            blogger_meta_data_df.to_csv(blogger_meta_path, mode='a', encoding="utf-8-sig",
                                        header=is_first, index_label="Index")

            is_first = False  # 첫 번째 이후로는 헤더를 추가하지 않도록 설정
finally:
    driver.quit()