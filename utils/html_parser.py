import time

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

def parse_html(driver, url):
    # URL에 접속
    driver.get(url)
    time.sleep(2)  # 페이지 로딩 대기 (필요에 따라 조정 가능)

    # 페이지의 HTML 소스 가져오기
    try:
        iframe = driver.find_element(By.ID, "mainFrame")  # id가 mainFrame이라는 요소를 찾아내고 -> iframe임
        driver.switch_to.frame(iframe)  # 이 iframe이 내가 찾고자하는 html을 포함하고 있는 내용
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        # print(page_source)
    except Exception:
        print("No iframe ")
        return False






    # print('page_source:', page_source)

    # BeautifulSoup으로 HTML 파싱



    return soup

if __name__=="__main__":
    # url: 네이버 블로그 링크
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # 헤드리스 모드
    chrome_options.add_argument("--no-sandbox")  # 샌드박스 모드 비활성화
    chrome_options.add_argument("--disable-dev-shm-usage")  # /dev/shm 사용 안 함 (Docker에서 메모리 문제 해결)

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    url = "https://blog.naver.com/soyeon931018/223034765619"
    parse_html(driver, url)

