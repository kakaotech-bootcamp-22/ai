# .env 파일에서 API 인증 정보 로드
import os

import requests
from dotenv import load_dotenv

load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

# 블로그 링크 추출 : 일단 3개 -> 실제 크롤링 시 display 숫자 조정
def get_blog_links(keyword):
    # 검색어 설정 및 API 요청
    url = "https://openapi.naver.com/v1/search/blog.json"
    headers = {
        "X-Naver-Client-Id": client_id,
        "X-Naver-Client-Secret": client_secret
    }
    params = {
        "query": keyword,
        "display":20,
        "start": 1,
        "sort": "sim"
    }

    response = requests.get(url, headers=headers, params=params)
    blog_links = []

    # 블로그 글 링크 추출
    if response.status_code == 200:
        data = response.json()
        for item in data['items']:
            # title = item['title'].replace("<b>", "").replace("</b>", "")
            link = item['link']
            blog_links.append(link)
            print(f"링크 : {link}")
    else:
        print(f"Error Code: {response.status_code}")

    return blog_links