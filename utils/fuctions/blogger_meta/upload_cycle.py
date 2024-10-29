from selenium import webdriver
from bs4 import BeautifulSoup
from datetime import datetime
import time

def get_upload_cycle():
    # Selenium WebDriver 설정
    driver = webdriver.Chrome('path_to_chromedriver')  # ChromeDriver 경로 설정

    # 블로그 URL
    blog_url = "https://blog.naver.com/example_blog_id"
    driver.get(blog_url)
    time.sleep(3)  # 페이지 로딩 시간 대기

    # 게시글 날짜 수집 리스트 초기화
    post_dates = []

    # 여러 페이지에서 게시글 수집
    for page in range(1, 6):  # 필요한 만큼 페이지를 탐색 (예: 5페이지)
        page_url = f"{blog_url}?Page={page}"
        driver.get(page_url)
        time.sleep(2)  # 페이지 로딩 시간 대기

        # 페이지 소스 가져오기
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # 게시글 날짜 찾기
        dates = soup.find_all('span', {'class': 'post_date'})  # 정확한 클래스 이름 확인 필요
        for date in dates:
            post_date_text = date.get_text().strip()
            post_date = datetime.strptime(post_date_text, "%Y.%m.%d")  # 네이버 블로그 날짜 형식에 맞게 파싱
            post_dates.append(post_date)

    driver.quit()

    # 날짜 데이터 분석
    if post_dates:
        post_dates.sort()  # 날짜 순으로 정렬
        total_days = (post_dates[-1] - post_dates[0]).days + 1  # 블로그 기간 (최초 ~ 마지막 게시글 날짜 차이)
        total_posts = len(post_dates)  # 총 게시글 수

        # 하루 평균 업로드 개수 계산
        avg_posts_per_day = total_posts / total_days

        # 업로드 주기 계산 (각 게시글 간의 날짜 차이의 평균)
        intervals = [(post_dates[i] - post_dates[i - 1]).days for i in range(1, len(post_dates))]
        avg_upload_interval = sum(intervals) / len(intervals) if intervals else 0

        # 결과 출력
        print(f"총 게시글 수: {total_posts}")
        print(f"블로그 기간 (일): {total_days}")
        print(f"하루 평균 업로드 개수: {avg_posts_per_day:.2f}")
        print(f"평균 업로드 주기 (일): {avg_upload_interval:.2f}")
    else:
        print("게시글 날짜를 찾을 수 없음")