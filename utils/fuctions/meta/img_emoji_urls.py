from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
import os
import requests
import re

def update_url_type_param(url, new_type_value): # url에서 type 파라미터 값을 변경
    # URL을 파싱
    parsed_url = urlparse(url)
    # 쿼리 파라미터를 딕셔너리로 변환
    query_params = parse_qs(parsed_url.query)
    # 'type' 파라미터를 새로운 값으로 변경
    query_params['type'] = new_type_value
    # 수정된 쿼리 문자열 만들기
    new_query = urlencode(query_params, doseq=True)
    # 수정된 URL 만들기
    updated_url = urlunparse(parsed_url._replace(query=new_query))
    return updated_url

def img_emoji_urls(soup): #bs4 객체가 들어오면, 이미지 개수, 이모지 개수, 이모지
    # 이미지 데이터 가져오기
    img_urls = []  # 이미지 링크
    emojis_url = []  # 이모지 URL 리스트
    num_emojis = 0  # 이모지 개수
    img_candidates = [img['src'] for img in soup.find_all('img') if img.get('src')]
    # for img_candidate in img_candidates:
    #     print(img_candidate + '\n')

    for url in img_candidates:
        match = re.match(r"^https://([^\.]+)\.pstatic\.net/", url)
        if match:
            if match.group(1) == "postfiles": # 이미지 유형
                url = update_url_type_param(url, "w580")  # 이미지 블러처리 해제
                img_urls.append(url)
            elif  match.group(1) == "storep-phinf": # 이모지 유형
                emojis_url.append(url)
        # 그 외 경우
        else:
            if url.startswith("https://"): # data: 로 시작하는
                img_urls.append(url)

    # print("num of imgs:", len(img_urls))
    # print(f"- 처음 이미지 URL:{img_urls[0]}, 마지막 이미지 URL: {img_urls[-1]}")
    # """for url in img_urls:
    #     print(f"{url}\n")"""
    # print("num of emojis", num_emojis)

    d = {"img_cnt": len(img_urls), "img_urls": img_urls, "emoji_cnt": num_emojis}
    return d # 딕셔너리

def download_images(img_urls, save_dir):
    # 디렉토리가 없으면 생성
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    for url in img_urls:
        # print("이미지 url:", url)
        # 파일명 추출 (기본적으로 URL에서 마지막 부분 사용)
        filename = url.split("/")[-1].split("?")[0].split('.')[0]
        img_format = '.jpg'
        file_path = os.path.join(save_dir, filename+img_format)
        # print(save_dir, filename, img_format)
        # print("file_path:", file_path)

        try:
            # 이미지 다운로드
            response = requests.get(url, stream=True)
            if response.status_code == 200:
                with open(file_path, 'wb') as file:
                    for chunk in response.iter_content(1024):
                        file.write(chunk)
                # print(f"Image downloaded and saved as {file_path}")
            else:
                print(f"Failed to download image from {url} (status code: {response.status_code})")
        except Exception as e:
            print(f"An error occurred while downloading {url}: {e}")

"""if __name__ == '__main__':
     img_emoji_urls(url='https://blog.naver.com/hj861031/223601136491')
    #a = update_url_type_param('https://postfiles.pstatic.net/MjAyNDA5MjlfMTE0/MDAxNzI3NTM2NDc2ODI5.LViUuL9TcYOry7VNHwVEqQ0A-eFZi3ZwMJ7wA0uFG2sg.jU5K2QXyCmPFllIcWbpU8qV5SxB7DaOwHz1LgP-9Ye8g.JPEG/IMG_2196.jpg?type=w80_blur' , 'w580')
     # 태그 이미지 - https://xn--939au0g4vj8sq.net/_sp/wg.php?ctf=MTcwOTI0fDE1MDQ4NjZ8YWRtXzI2OTEyOHw2NjYxMHwyMDI0MTAwMg==

if __name__ == "__main__":

    # 사용 예시
    img_urls = [
        "https://postfiles.pstatic.net/MjAyNDA5MjlfMTgx/MDAxNzI3NTM2NDc0OTM2.p031lLK2gHsYiZvhFQdKGe-5sOsVXrJ6Z0CNZyEE7fog.18FIL6uMT0CQ8F3EWu3Ib0hlMJau-E7ODBU_LNVTzQog.JPEG/IMG_2172.jpg?type=w80_blur",
        "https://postfiles.pstatic.net/MjAyNDA5MjlfMjk5/MDAxNzI3NTM2NDc3OTI1.xNEylSPGacrEKjvAIAMbNU3ZKnVKBGBPwFqH6G1uD-8g.PW3u9d4UDHhI4KCPbCB_7OrvXQkpaDd1L3zCnMiv2vEg.JPEG/IMG_2212.jpg?type=w580"
    ]
    save_dir = "./images/"  # 원하는 디렉토리 경로
    download_images(img_urls, save_dir)"""