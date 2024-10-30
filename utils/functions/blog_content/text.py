import os
import re

def save_blog_text(file_name, content):
    # 프로젝트 최상위 폴더의 절대 경로를 기준으로 data/txt 경로 설정
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
    save_dir = os.path.join(base_dir, 'data', 'txt')

    if not os.path.exists(save_dir): # 저장 패스 없으면 여기서 체크
        os.makedirs(save_dir)
        print("no directory!")

    save_path = os.path.join(save_dir, file_name)
    print(save_path)

    try:
        with open(save_path + '.txt', "w", encoding="utf-8") as file:
            file.write(content)
        print("File created successfully:", save_path + '.txt')
        print("Current working directory:", os.getcwd())
    except Exception as e:
        print(f"An error occurred: {e}")

    return save_path + '.txt'

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

    # 텍스트 파일 저장
    file_name = article_id
    save_path = save_blog_text(file_name, whole_text)

    return save_path, whole_text_len