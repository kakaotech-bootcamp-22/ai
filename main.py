import os, time
import pandas as pd

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

from utils.crawler.blog_content_crawler import get_article_writer_id, get_blog_content_data
from utils.crawler.blog_meta_crawler import get_blog_meta_data
from utils.crawler.blogger_meta_crawler import get_blogger_meta_data
from utils.blog_links_loader import get_blog_links
from utils.html_parser import parse_html

# url: 네이버 블로그 링크
chrome_options = Options()
chrome_options.add_argument("--headless")  # 헤드리스 모드
chrome_options.add_argument("--no-sandbox")  # 샌드박스 모드 비활성화
chrome_options.add_argument("--disable-dev-shm-usage")  # /dev/shm 사용 안 함 (Docker에서 메모리 문제 해결)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

def get_next_index(file_path):
    """파일의 마지막 인덱스 가져와 다음 인덱스 계산"""
    if os.path.exists(file_path):
        existing_df = pd.read_csv(file_path)
        if not existing_df.empty:
            return existing_df.index[-1] + 1
    return 0  # 파일이 없거나 빈 경우 1부터 시작

# 지정된 경로의 파일들 삭제
def clear_directory(directory_path):
    if os.path.exists(directory_path):
        for file in os.listdir(directory_path):
            file_path = os.path.join(directory_path, file)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    print(f"Deleted file: {file_path}")
            except Exception as e:
                print(f"Error deleting file {file_path}: {e}")
    else:
        print("Directory does not exist:", directory_path)

try:
    # 파일 존재 시, 삭제 후 크롤링 시작
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
    save_dir = os.path.join(base_dir, 'data', 'txt')
    # 해당 경로의 파일 삭제
    clear_directory(save_dir)

    # CSV 파일 생성 경로
    os.makedirs('data/collected_data/csv', exist_ok=True)
    post_content_path = "data/collected_data/csv/post_content_data.csv"
    post_meta_path = "data/collected_data/csv/post_meta_data.csv"
    blogger_meta_path = "data/collected_data/csv/blogger_meta_data.csv"

    # 파일이 이미 존재하면 삭제
    if os.path.exists(post_content_path):
        os.remove(post_content_path)
    if os.path.exists(post_meta_path):
        os.remove(post_meta_path)
    if os.path.exists(blogger_meta_path):
        os.remove(blogger_meta_path)

    # <크롤링 시작>
    # 크롤링 시간 측정
    start_time = time.time()

    # area_list = ['판교', "강남", "성수", "군자", "제주도"]   # "북촌"

    area_list = [
        "강남", "교대", "홍대", "이태원", "성수", "압구정", "신사", "명동", "여의도", "건대", "군자",
        "판교", "가로수길", "종로", "삼청동", "광화문", "서래마을",
        "동대문", "합정", "상수", "대학로",
        "신촌", "서강대", "보문동", "신림동", "사당",
        "삼각지", "용산", "한남동", "서울대입구", "을지로", "연남동", "안국",
        "노량진", "청담동", "연남동", "마포", "잠실", "선릉",
        "남산", "서초", "정자역",
        "왕십리", "청량리", "미아리", "의정부", "광명",
        "여수", "순천", "전주 한옥마을", "이촌동", "대치동", "송파"
        "해운대", "광안리", "전포동", "서면", "송정", "구월동", "송도", "주안", "인사동", "목동",
        "양재", "일산", "수원", "동탄", "기흥", "용인", "안양", "평촌", "구리", "김포", "파주", "시흥", "하남 미사",
        "남포동", "남천동", "동래", "성남", "부평", "화정동", "장안동", "가양동", "홍제동", "문래동",
        "백석동", "대구 동성로", "대구", "대전", "청주 성안길", "천안 신부동", "군산 월명동", "익산 모현동", "포항 구룡포", "울산 삼산동",
        "강릉", "춘천", "평창", "속초", "양양", "철원",
        "동해", "원주", "정선", "인제",
        "제주 서귀포", "제주 애월", "한림"
    ]

    print(len(area_list))
    # print("Current working MAIN directory:", os.getcwd())

    is_first = True
    for area in area_list:
        keyword = area + " 맛집 리뷰"
        #keyword = "내돈내산 "+ area + " 맛집 리뷰" # 진짜 리뷰 키워드 서칭
        print('*** 현재 크롤링 중인 장소 키워드 *** : ', keyword)
        print()
        urls = get_blog_links(keyword)

        blogger_meta_data_lst = []
        post_content_data_lst = []
        post_meta_data_lst = []

        for url in urls:
            # url 별 html 파싱
            if not url.startswith("https://blog.naver.com"):
                pass
            soup = parse_html(driver, url)
            if not soup: # iframe 이 없을 때 - 제외
                continue

            # 추출한 블로그 링크로 3 종류 데이터 추출
            # 0. 블로그 사용자 id
            blog_id, writer_id = get_article_writer_id(url)
            print(f"블로그 사용자 id  -  *블로그 id : {blog_id}  *사용자 id : {writer_id}")

            # 1. blog_content : 포스트 컨텐츠 데이터 (포스트 내 이미지 개수, 포스트 내 이모지 개수는 여기서 크롤링함 !)
            title, text_save_path, img_save_dir, img_cnt, emoji_cnt, title_len, whole_text_len, img_urls = get_blog_content_data(soup, url)
            print(f"포스트 컨텐츠 데이터  -  *제목 : {title}  *본문 url : {text_save_path}   *이미지 url : {img_save_dir}    *이미지 개수 : {img_cnt}  *이모지 개수 : {emoji_cnt}")
            print(f"                    *제목 길이 : {title_len}     *본문 길이 : {whole_text_len}")

            # 2. blog_meta_data : 포스트 메타 데이터
            like_cnt, comment_cnt = get_blog_meta_data(soup)
            print(f"포스트 메타 데이터  -  *공감 수 : {like_cnt}  *댓글 수 : {comment_cnt}")

            # 3. blogger_meta : 블로거 메타 데이터
            intro, banner, neighbor_cnt, menu_cnt, post_in_menu_number = get_blogger_meta_data(soup)
            print(f"블로거 메타 데이터  -  *자기소개: {intro}  *배너 : {banner}   *이웃 수 : {neighbor_cnt}   *메뉴 개수 : {menu_cnt}  *메뉴에 속한 포스트 개수 : {post_in_menu_number}")
            print()

            # <크롤링한 데이터 저장>
            # 1. 포스트 컨텐츠 데이터 저장
            post_content_data_lst.append([blog_id,writer_id,title,text_save_path])
            # 2. 포스트 메타 데이터 저장
            post_meta_data_lst.append([blog_id,writer_id, title_len, whole_text_len,
                                       img_save_dir, img_cnt, emoji_cnt, like_cnt, comment_cnt, img_urls])
            # 3. 블로거 메타 데이터 저장
            blogger_meta_data_lst.append([blog_id, writer_id, intro, banner,
                                          neighbor_cnt, menu_cnt, post_in_menu_number])
        # 포스트 컨텐츠 데이터 csv 저장
        post_content_data_df = pd.DataFrame(post_content_data_lst , columns = ["blog_id", "writer_id","title", "text_save_path"])
        next_index = get_next_index(post_content_path)
        post_content_data_df.index = range(next_index, next_index + len(post_content_data_df))
        post_content_data_df.to_csv(post_content_path, mode='a', encoding="utf-8-sig",
                                    header= is_first, index_label="Index")
        # 포스트 메타 데이터 csv 저장
        post_meta_data_df = pd.DataFrame(post_meta_data_lst,
                                         columns = ["blog_id", "writer_id",
                                                    "title_len", "whole_text_len", "img_save_dir", "img_cnt",
                                                    "emoji_cnt","like_cnt", "comment_cnt", "img_urls"])
        next_index = get_next_index(post_meta_path)  # 다음 인덱스 설정
        post_meta_data_df.index = range(next_index, next_index + len(post_meta_data_df))
        post_meta_data_df.to_csv(post_meta_path, mode='a', encoding="utf-8-sig",
                                 header=is_first, index_label="Index")
        # 블로거 메타 데이터 csv 저장
        blogger_meta_data_df = pd.DataFrame(blogger_meta_data_lst,
                                            columns = ["blog_id", "writer_id", "intro", "banner",
                                                       "neighbor_cnt", "menu_cnt", "post_in_menu_number"] )
        next_index = get_next_index(blogger_meta_path)  # 다음 인덱스 설정
        blogger_meta_data_df.index = range(next_index, next_index + len(blogger_meta_data_df))
        blogger_meta_data_df.to_csv(blogger_meta_path, mode='a', encoding="utf-8-sig",
                                    header=is_first, index_label="Index")
        is_first = False  # 첫 번째 이후로는 헤더를 추가하지 않도록 설정

finally:
    driver.quit()
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"크롤링에 걸린 시간: {elapsed_time:.2f}초")