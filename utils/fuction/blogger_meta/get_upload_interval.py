from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from datetime import datetime
import time

# Selenium 드라이버 설정
chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)


def get_post_dates_from_page():
    """현재 페이지의 게시글 날짜를 수집하는 함수"""
    post_dates = []

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    date_tags = soup.find_all('span', class_='se_publishDate')  # 날짜 태그 클래스 확인 필요

    for date_tag in date_tags:
        date_text = date_tag.get_text().strip()
        post_date = datetime.strptime(date_text, "%Y.%m.%d")
        post_dates.append(post_date)

    return post_dates


def get_all_post_dates(blog_url):
    """모든 페이지에서 게시글 날짜를 수집하는 함수"""
    driver.get(blog_url)
    time.sleep(2)

    # mainFrame iframe으로 전환
    iframe = driver.find_element(By.ID, "mainFrame")
    driver.switch_to.frame(iframe)

    all_post_dates = set()  # 중복 방지를 위해 set 사용

    while True:
        # 현재 페이지에서 게시글 날짜 수집
        post_dates = get_post_dates_from_page()
        all_post_dates.update(post_dates)

        # "다음" 버튼을 찾아 클릭하여 다음 페이지로 이동
        try:
            next_button = driver.find_element(By.LINK_TEXT, "다음>")
            next_button.click()
            time.sleep(2)  # 페이지 로딩 대기
        except:
            print("마지막 페이지에 도달했습니다.")
            break  # "다음" 버튼이 없으면 마지막 페이지이므로 종료

    return sorted(all_post_dates)  # 날짜를 오름차순으로 정렬하여 반환


def calculate_average_upload_interval(post_dates):
    if len(post_dates) < 2:
        return None  # 게시글이 1개 이하일 경우, 주기 계산 불가

    intervals = [(post_dates[i] - post_dates[i - 1]).days for i in range(1, len(post_dates))]
    avg_interval = sum(intervals) / len(intervals)

    return avg_interval


# # 실행 예시
# blog_url = "https://blog.naver.com/sample_blog_id"
# try:
#     post_dates = get_all_post_dates(blog_url)
#     avg_interval = calculate_average_upload_interval(post_dates)
#
#     if avg_interval:
#         print(f"평균 업로드 주기: {avg_interval:.2f}일")
#     else:
#         print("게시글이 충분하지 않아 주기를 계산할 수 없습니다.")