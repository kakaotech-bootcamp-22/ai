from utils.filter.text_filtering import get_blog_id_by_text_filtering
import shutil
import pandas as pd
import os

# OCR_TARGET_KEYWORDS = ('광고아님', '광고 아님', '직접 구매', '직접 구매','직접 결제', '직접결제')  # '솔직 후기', '솔직하게 작성' -> 이 부분 문구만으로는 정확한 진짜 리뷰 필터링 불가 -> 소정의 원고를 받고도 솔직한 리뷰 작성 가능하기 때문에 ..
TEXT_TARGET_KEYWORDS = ('소정의 원고료', '일정액의 수수료', '소정의 적립금')

def filter_and_save_csv(file_path, blog_ids, output_path):
    # CSV 파일을 읽어옵니다.
    df = pd.read_csv(file_path)

    # blog_id가 final_fake_blog_id에 포함된 행만 필터링
    filtered_df = df[df['blog_id'].isin(blog_ids)]

    # 필터링된 데이터프레임을 새로운 CSV 파일로 저장합니다.
    filtered_df.to_csv(output_path, index=False)


import pandas as pd


def get_blog_ids():
    # CSV 파일 경로 설정
    csv_file_path = '/Users/admin/PycharmProjects/ai-jo_crawler/data/collected_real_data/csv/post_content_data.csv'

    try:
        # CSV 파일 읽기
        df = pd.read_csv(csv_file_path)

        # blog_id 열의 고유값을 문자열로 변환하여 set으로 만들기
        blog_ids = set(str(id_) for id_ in df['blog_id'].unique())
        return blog_ids

    except Exception as e:
        print(f"Error reading file: {e}")
        return set()

if __name__ == '__main__':
    total_set = get_blog_ids()

    # 광고성 블로그 ID 추출
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    txt_base_dir = os.path.join(project_root, 'data', 'collected_real_data', 'txt')
    set3 = get_blog_id_by_text_filtering(TEXT_TARGET_KEYWORDS, txt_base_dir)

    # 전체 블로그 id에서
    final_fake_blog_id =  total_set - set3
    # final_fake_blog_id = {223240310880, 223621078805, 223486790401, 223457867880, 223150438217}

    print(f"총 광고성 블로그 ID 수: {len(final_fake_blog_id)}")

    # 현재 파일의 경로에서 시작하여 프로젝트 루트 찾기
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(current_dir))  # utils 폴더를 벗어나 ai-jo_crawler 루트로

    # CSV 파일 경로 설정
    csv_folder = os.path.join(project_root, 'data', 'collected_real_data', 'csv')

    # 경로가 존재하는지 확인
    print(f"CSV 폴더 경로: {csv_folder}")
    if not os.path.exists(csv_folder):
        raise FileNotFoundError(f"CSV 폴더를 찾을 수 없습니다: {csv_folder}")

    blogger_meta_file = os.path.join(csv_folder, 'blogger_meta_data.csv')
    post_content_file = os.path.join(csv_folder, 'post_content_data.csv')
    post_meta_file = os.path.join(csv_folder, 'post_meta_data.csv')

    # 새로운 CSV 파일을 저장할 폴더 경로 설정
    new_csv_folder = os.path.join(project_root, 'data', 'real_data', 'csv')

    # 폴더가 존재하면 기존 파일을 삭제하고, 존재하지 않으면 폴더 생성
    if os.path.exists(new_csv_folder):
        shutil.rmtree(new_csv_folder)  # 폴더 내 모든 파일 삭제
    os.makedirs(new_csv_folder, exist_ok=True)  # 폴더 생성

    # 저장할 파일 경로 설정
    filtered_blogger_meta_file = os.path.join(new_csv_folder, 'real_blogger_meta_data.csv')
    filtered_post_content_file = os.path.join(new_csv_folder, 'real_post_content_data.csv')
    filtered_post_meta_file = os.path.join(new_csv_folder, 'real_post_meta_data.csv')

    # CSV 파일 필터링 및 저장
    filter_and_save_csv(blogger_meta_file, final_fake_blog_id, filtered_blogger_meta_file)
    filter_and_save_csv(post_content_file, final_fake_blog_id, filtered_post_content_file)
    filter_and_save_csv(post_meta_file, final_fake_blog_id, filtered_post_meta_file)

    print("필터링 완료! 새로운 CSV 파일들이 /fake_data/csv 폴더에 생성되었습니다.")