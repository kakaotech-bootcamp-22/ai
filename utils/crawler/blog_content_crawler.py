"""
1. 블로그 컨텐츠 데이터 수집 하는 크롤러

블로그 내의 글을 긁어오는 코드
긁어올 데이터 항목 - 이미지 좋아요 수, 댓글 수
"""

from selenium.common import NoSuchElementException, TimeoutException
import time, os
from utils.fuction.blog_content_meta.img_emoji_urls import img_emoji_urls, download_images
from utils.fuction.blog_content.text import collect_text

# 블로그 및 사용자 id
def get_article_writer_id(url):
    url_list = url.split('/')

    article_id = url_list[-1]
    writer_id = url_list[-2]

    return article_id, writer_id

def get_blog_content_data(soup, url): # 네이버 블로그 아티클 정보 크롤링하는 함수
    # 변수 기본값 초기화
    title =""
    text_save_path = None
    img_save_dir = None
    img_cnt = 0
    emoji_cnt = 0

    title_len = 0
    whole_text_len = 0

    try:
        # 블로그 및 사용자 id
        a_id, w_id = get_article_writer_id(url)

        # 블로그 제목 ( 제목 길이, 본문 길이 수집 -> 일단 나중에 .. .. ..)
        title_tag = soup.find('div', class_='se-module se-module-text se-title-text')
        if title_tag:
            # 'title_tag' 내부의 'span' 태그 텍스트 추출
            title = title_tag.find('span').get_text().strip()
            # 블로그 제목 길이
            title_len = len(title)
        else:
            title = "제목 없음"


        # 텍스트 데이터(경로) 수집 및 디렉토리에 저장
        text_save_path, whole_text_len = collect_text(soup, a_id)

        # 이미지 & 이모지 데이터 수집
        d = img_emoji_urls(soup)
        img_cnt, emoji_cnt = d["img_cnt"], d["emoji_cnt"]

        # 이미지 데이터(경로) 수집
        img_save_dir = os.path.join('../data/imgs', a_id)
        img_urls = d['img_urls']
        # print("이미지 저장 path:", img_save_dir)
        download_images(img_urls, img_save_dir)

    except NoSuchElementException as e:
        print(f"Element not found error: {e}")
    except TimeoutException as e:
        print(f"Page load timeout error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    return title, text_save_path, img_save_dir, img_cnt, emoji_cnt, title_len, whole_text_len

if __name__ == "__main__":
    url = "https://blog.naver.com/hj861031/223601136491"
    print("title, text_save_path, img_save_dir, img_cnt, emoji_cnt : ",  get_blog_content_data(url))