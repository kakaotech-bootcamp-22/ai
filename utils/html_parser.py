import time

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By


def parse_html(driver, url):
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

    return soup
