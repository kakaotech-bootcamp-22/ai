"""
3. 블로거 메타 데이터

블로거 자기소개, 블로거 배너, 이웃 수, 블로그 메뉴 개수, 포스트가 속한 메뉴 게시글 개수, 글 업로드 주기, 하루 평균 업로드 개수
"""

from selenium.common import NoSuchElementException, TimeoutException
import re
def get_blogger_meta_data(soup): # 네이버 블로그 아티클 정보 크롤링하는 함수
    # 변수 기본값 초기화
    intro = ""
    banner = ""
    neighbor_cnt = 0
    menu_cnt = 0
    post_in_menu_cnt = 0

    try:
        # 블로거 자기소개
        '''
        자기소개 크롤링: .profile_desc와 같이 자기소개가 들어 있는 HTML 클래스 이름을 사용해 텍스트를 추출
        .itemfont.col 태그는 여러 개라 .caption.align로 자기소개 텍스트 접근
        '''
        intro = soup.select_one('.caption.align .itemfont.col')
        intro = intro.get_text(strip=True) if intro else None  # 텍스트만 추출하고 None 처리
        # intro = re.sub(r'&nbsp;', ' ', intro)
        intro = re.sub(r"\xa0", ' ', intro)


        # 블로거 배너
        banner = soup.select_one('.itemtitlefont')
        banner = banner.get_text(strip=True) if banner else None

        # 이웃 수
        neighbor_cnt = soup.select_one('.widget .cm-col1 em')  # .widget   .info .cm-col1
        neighbor_cnt = neighbor_cnt.get_text(strip=True) if neighbor_cnt else None

        # 블로그 메뉴 개수
        menu_cnt1 = len(soup.find_all(class_='listimage'))  # class명 앞에 `class_` 사용
        menu_cnt2 = len(soup.find_all(class_='albumimage'))  # albumimage
        menu_cnt = menu_cnt1 + menu_cnt2 - 1

        # 포스트가 속한 메뉴 게시글 개수

        h4_text = soup.select_one('h4.category_title').get_text() if soup.select_one('h4.category_title') else None
        post_in_menu_cnt = re.search(r'\d{1,3}(?:,\d{3})*', h4_text).group() if h4_text else None  # 정규식 일치 결과 추출


        # 글 업로드 주기


        # 하루 평균 업로드 개수



    except NoSuchElementException as e:
        print(f"Element not found error: {e}")
    except TimeoutException as e:
        print(f"Page load timeout error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    return intro, banner, neighbor_cnt, menu_cnt, post_in_menu_cnt

if __name__ == "__main__":
    url = "https://blog.naver.com/hj861031/223601136491"
    print("get_blogger_meta_data : ",  get_blogger_meta_data(url))