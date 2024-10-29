from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time, os
import re

def save_blog_text(file_name, content):
    save_dir = '../data/txt'
    if not os.path.exists(save_dir): # 저장 패스 없으면 여기서 체크
        os.makedirs(save_dir)
    save_path = os.path.join(save_dir, file_name)

    with open(save_path+'.txt', "w", encoding="utf-8") as file:
        file.write(content)
    # print(f"text saved as {save_path}")

    return save_path+'.txt'

def collect_text(soup, article_id): # 네이버 블로그 아티클 정보 크롤링하는 함수
    # 텍스트 데이터 수집
    content = soup.find_all('p', class_=re.compile('se-text-paragraph'))
    # 본문 내용만 리스트로 저장
    article_content = []
    for item in content:
        paragraphs = item.find_all('span')  # 본문 텍스트는 span 태그 안에 있을 가능성이 높음
        for paragraph in paragraphs:
            chunk = paragraph.get_text(strip=True)
            chunk = chunk.replace(u"\u200b", u"\n")
            article_content.append(chunk)

    whole_text = ' '.join(article_content)
    whole_text_len = len(whole_text)
    # print("whole_text:", whole_text)

    # 텍스트 파일 저장
    file_name = article_id
    save_path = save_blog_text(file_name, whole_text)
    return save_path, whole_text_len

#if __name__ == "__main__":
    #article(url = "https://blog.naver.com/hj861031/223601136491")
