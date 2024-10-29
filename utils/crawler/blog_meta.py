"""
2. 블로그 메타 데이터 수집 하는 크롤러

포스트 메타 데이터 : 포스트 제목 길이, 포스트 길이, 포스트 업로드 날짜, , 공감 개수, 댓글 개수
"""

from bs4 import BeautifulSoup
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
import time, os
from utils.fuctions.meta.img_emoji_urls import img_emoji_urls, download_images
from utils.fuctions.content.text import collect_text
from utils.fuctions.meta.like_comment import get_like_comment_count


def get_blog_meta_data(url, driver): # 네이버 블로그 아티클 정보 크롤링하는 함수
    # 변수 기본값 초기화
    like_cnt = 0
    comment_cnt = 0

    try:
        # URL에 접속
        driver.get(url)
        time.sleep(2)  # 페이지 로딩 대기 (필요에 따라 조정 가능)

        # 페이지의 HTML 소스 가져오기
        iframe = driver.find_element(By.ID, "mainFrame")  # id가 mainFrame이라는 요소를 찾아내고 -> iframe임
        driver.switch_to.frame(iframe)  # 이 iframe이 내가 찾고자하는 html을 포함하고 있는 내용
        page_source = driver.page_source
        # print('page_source:', page_source)

        # BeautifulSoup으로 HTML 파싱
        soup = BeautifulSoup(page_source, 'html.parser')

        # 포스트 제목 길이, 포스트 길이 -> blog_content에서 ???

        # 포스트 업로드 날짜

        # 공감 + 댓글 개수
        like_cnt, comment_cnt = get_like_comment_count(soup)


    except NoSuchElementException as e:
        print(f"Element not found error: {e}")
    except TimeoutException as e:
        print(f"Page load timeout error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    return like_cnt, comment_cnt

if __name__ == "__main__":
    url = "https://blog.naver.com/hj861031/223601136491"
    print(" : ",  get_blog_meta_data(url))