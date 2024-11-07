import pandas as pd
from utils.filter.img_OCR_multiprocessing_filtering import get_fake_blog_id_by_ocr_filtering
from utils.filter.img_url_filtering import get_fake_blog_id_by_img_url_filtering
from utils.filter.text_filtering import get_fake_blog_id_by_text_filtering
import os
import shutil


def filter_and_save_csv(file_path, blog_ids, output_path):
    # CSV 파일을 읽어옵니다.
    df = pd.read_csv(file_path)

    # blog_id가 final_fake_blog_id에 포함된 행만 필터링
    filtered_df = df[df['blog_id'].isin(blog_ids)]

    # 필터링된 데이터프레임을 새로운 CSV 파일로 저장합니다.
    filtered_df.to_csv(output_path, index=False)


if __name__ == '__main__':
    # 광고성 블로그 ID 추출
    set1 = get_fake_blog_id_by_img_url_filtering()
    set2 = get_fake_blog_id_by_ocr_filtering()
    set3 = get_fake_blog_id_by_text_filtering()
    final_fake_blog_id = set1 | set2 | set3
    #final_fake_blog_id = {223240310880, 223621078805, 223486790401, 223457867880, 223150438217}

    print(f"총 광고성 블로그 ID 수: {len(final_fake_blog_id)}")

    # 현재 파일의 경로에서 시작하여 프로젝트 루트 찾기
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(current_dir))  # utils 폴더를 벗어나 ai-jo_crawler 루트로

    # CSV 파일 경로 설정
    csv_folder = os.path.join(project_root, 'data', 'csv')

    # 경로가 존재하는지 확인
    print(f"CSV 폴더 경로: {csv_folder}")
    if not os.path.exists(csv_folder):
        raise FileNotFoundError(f"CSV 폴더를 찾을 수 없습니다: {csv_folder}")

    blogger_meta_file = os.path.join(csv_folder, 'blogger_meta_data.csv')
    post_content_file = os.path.join(csv_folder, 'post_content_data.csv')
    post_meta_file = os.path.join(csv_folder, 'post_meta_data.csv')

    # 새로운 CSV 파일을 저장할 폴더 경로 설정
    new_csv_folder = os.path.join(project_root, 'fake_data', 'csv')

    # 폴더가 존재하면 기존 파일을 삭제하고, 존재하지 않으면 폴더 생성
    if os.path.exists(new_csv_folder):
        shutil.rmtree(new_csv_folder)  # 폴더 내 모든 파일 삭제
    os.makedirs(new_csv_folder, exist_ok=True)  # 폴더 생성

    # 저장할 파일 경로 설정
    filtered_blogger_meta_file = os.path.join(new_csv_folder, 'filtered_blogger_meta_data.csv')
    filtered_post_content_file = os.path.join(new_csv_folder, 'filtered_post_content_data.csv')
    filtered_post_meta_file = os.path.join(new_csv_folder, 'filtered_post_meta_data.csv')

    # CSV 파일 필터링 및 저장
    filter_and_save_csv(blogger_meta_file, final_fake_blog_id, filtered_blogger_meta_file)
    filter_and_save_csv(post_content_file, final_fake_blog_id, filtered_post_content_file)
    filter_and_save_csv(post_meta_file, final_fake_blog_id, filtered_post_meta_file)

    print("필터링 완료! 새로운 CSV 파일들이 /fake_data/csv 폴더에 생성되었습니다.")