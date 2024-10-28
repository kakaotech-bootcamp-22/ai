import os

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# .env 파일에서 API 인증 정보 로드
load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def get_blog_links(query):
    # 검색어 설정 및 API 요청
    url = "https://openapi.naver.com/v1/search/blog.json"
    headers = {
        "X-Naver-Client-Id": client_id,
        "X-Naver-Client-Secret": client_secret
    }
    params = {
        "query": query,
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
            title = item['title'].replace("<b>", "").replace("</b>", "")
            link = item['link']
            blog_links.append(link)
            print(f"제목: {title}\n링크: {link}\n")
    else:
        print(f"Error Code: {response.status_code}")

    return blog_links

def scrape_blog_content(blog_links):
    # Selenium 설정
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    main_text = []
    # 각 블로그 링크로 접속해 본문 크롤링
    for blog_link in blog_links:
        mobile_blog_link = blog_link.replace("blog.naver.com", "m.blog.naver.com")
        driver.get(mobile_blog_link)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".se-main-container")))
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        try:
            post_content = soup.select_one('.se-main-container').get_text(strip=True)
            main_text.append(post_content)
        except Exception as e:
            print(f"본문을 가져올 수 없습니다. 에러: {str(e)}")

    driver.quit()
    return main_text

if __name__ == "__main__":
    bl = get_blog_links("맛집 리뷰")
    print(bl)
    m_text = scrape_blog_content(bl)
    for m in m_text:
        print(" 본문 텍스트 : ", m)