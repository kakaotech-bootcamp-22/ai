"""
3. 블로거 메타 데이터

블로거 자기소개, 블로거 배너, 이웃 수, 블로그 메뉴 개수, 포스트가 속한 메뉴 게시글 개수, 글 업로드 주기, 하루 평균 업로드 개수
"""

from bs4 import BeautifulSoup
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
import time, os
from utils.fuctions.meta.img_emoji_urls import img_emoji_urls, download_images
from utils.fuctions.content.text import collect_text

def get_blogger_meta_data(url, driver): # 네이버 블로그 아티클 정보 크롤링하는 함수
    # 변수 기본값 초기화
    intro = ""
    banner = ""
    neighbor_cnt = 0
    menu_cnt = 0
    post_in_menu_cnt = 0

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

        # 블로거 자기소개
        '''
                자기소개 크롤링: .profile_desc와 같이 자기소개가 들어 있는 HTML 클래스 이름을 사용해 텍스트를 추출
                .itemfont.col 태그는 여러 개라 .caption.align로 자기소개 텍스트 접근
                '''
        intro = soup.select_one('.caption.align .itemfont.col')
        intro = intro.get_text(strip=True) if intro else None  # 텍스트만 추출하고 None 처리

        # 블로거 배너
        banner = soup.select_one('.itemtitlefont')
        banner = banner.get_text(strip=True) if banner else None

        # 이웃 수
        neighbor_cnt = soup.select_one('.widget .cm-col1 em')  # .widget   .info .cm-col1
        neighbor_cnt = neighbor_cnt.get_text(strip=True) if neighbor_cnt else None

        # 블로그 메뉴 개수
        menu_cnt = len(soup.find_all('.listimage'))  # albumimage
        menu_cnt = len(soup.find_all(class_='listimage'))  # class명 앞에 `class_` 사용

        # 포스트가 속한 메뉴 게시글 개수
        import re
        h4_text = soup.select_one('h4.category_title').get_text() if soup.select_one('h4.category_title') else None
        post_in_menu_cnt = re.search(r'\d{1,3}(?:,\d{3})*', h4_text).group() if h4_text else None  # 정규식 일치 결과 추출


        # 글 업로드 주기


        # 하루 평균 업로드 개수



    except NoSuchElementException as e:
        print(f"Element not found error: {e}")
    except TimeoutException as e:
        print(f"Page load timeout error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    # if intro:
    #     introduction = intro.get_text(strip=True)
    #     print(f"자기소개: {introduction}")
    # else:
    #     print("자기소개를 찾을 수 없습니다.")

    return intro, banner, neighbor_cnt, menu_cnt, post_in_menu_cnt

if __name__ == "__main__":
    url = "https://blog.naver.com/hj861031/223601136491"
    print("get_blogger_meta_data : ",  get_blogger_meta_data(url))