from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
# 자기소개, 배너 텍스트,
def get_info(blog_url):
    # Selenium 설정
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        driver.get(blog_url)

        # 페이지가 로드될 때까지 기다림
        time.sleep(2)

        # 블로거의 자기소개 부분이 포함된 iframe으로 전환
        iframe = driver.find_element(By.ID, "mainFrame")
        driver.switch_to.frame(iframe)

        # 페이지의 HTML 소스를 BeautifulSoup으로 파싱
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # 자기소개가 포함된 HTML 요소 선택
        # 1. 블로거 자기소개
        '''
        자기소개 크롤링: .profile_desc와 같이 자기소개가 들어 있는 HTML 클래스 이름을 사용해 텍스트를 추출
        .itemfont.col 태그는 여러 개라 .caption.align로 자기소개 텍스트 접근
        '''
        intro_element = soup.select_one('.caption.align .itemfont.col')

        # 2. 블로거 배너
        banner_element = soup.select_one('.itemtitlefont')

        # 3. 이웃 수
        neighbor_element = soup.select_one('.widget .cm-col1 em')  # .widget   .info .cm-col1

        # 4. 블로거 메뉴 개수 -> 수정
        menu_count_element = len(soup.find_all('.listimage')) #albumimage

        # 5. 포스트가 속한 메뉴 게시글 개수
        # <h4> 태그에서 텍스트 추출
        h4_text = soup.select_one('h4.category_title').get_text()
        # 정규 표현식을 사용하여 숫자만 추출
        import re
        post_in_menu_number = re.search(r'\d{1,3}(?:,\d{3})*', h4_text)  # 1,000 이상의 숫자도 포함


        if intro_element:
            introduction = intro_element.get_text(strip=True)
            print(f"자기소개: {introduction}")
        else:
            print("자기소개를 찾을 수 없습니다.")

        if banner_element:
            banner_text = banner_element.get_text(strip=True)
            print(f"블로그 배너: {banner_text}")
        else:
            print("블로그 배너 텍스트를 찾을 수 없습니다.")

        if neighbor_element:
            neighbor_num = neighbor_element.get_text(strip=True)
            print(f"이웃 수: {neighbor_num}")
        else:
            print("이웃 수를 찾을 수 없습니다.")

        if menu_count_element:
            print(f"메뉴 수: {menu_count_element}")
        else:
            print("메뉴 수를 찾을 수 없습니다.")

        if post_in_menu_number:
            clean_number = post_in_menu_number.group().replace(",", "")  # 쉼표 제거
            print("포스트가 속한 메뉴 게시글 개수:", clean_number)
        else:
            print("포스트가 속한 메뉴 게시글 개수를 찾을 수 없습니다.")

    except Exception as e:
        print(f"오류 발생: {str(e)}")

    finally:
        # 드라이버 종료
        driver.quit()

if __name__ == '__main__':

    # # 예시 블로그 URL
    # blog_url = "https://blog.naver.com/hj861031"
    # get_blogger_introduction(blog_url)

    search_query = "리뷰"
    blog_links = get_blog_links(search_query)
    for b in blog_links:
        get_info(b)
        print()
