import pandas as pd
import shutil
import os


def copy_txt_files():
    # CSV 파일에서 blog_id 읽기
    csv_path = '/data/real_data/csv/real_blogger_meta_data.csv'
    source_dir = '/data/collected_real_data/txt'
    target_dir = '/data/real_data/txt'

    # 타겟 디렉토리가 있으면 삭제하고 새로 생성
    if os.path.exists(target_dir):
        shutil.rmtree(target_dir)
    os.makedirs(target_dir)

    try:
        # CSV 파일 읽기
        df = pd.read_csv(csv_path)
        blog_ids = df['blog_id'].astype(str)  # blog_id를 문자열로 변환

        # 복사된 파일 수와 실패한 파일 수를 추적
        copied_count = 0
        failed_count = 0

        # 각 blog_id에 대해 파일 복사
        for blog_id in blog_ids:
            source_file = os.path.join(source_dir, f'{blog_id}.txt')
            target_file = os.path.join(target_dir, f'{blog_id}.txt')

            try:
                if os.path.exists(source_file):
                    shutil.copy2(source_file, target_file)
                    copied_count += 1
                else:
                    print(f'파일을 찾을 수 없습니다: {blog_id}.txt')
                    failed_count += 1
            except Exception as e:
                print(f'파일 복사 중 오류 발생 ({blog_id}.txt): {str(e)}')
                failed_count += 1

        print(f'\n작업 완료:')
        print(f'성공적으로 복사된 파일: {copied_count}')
        print(f'실패한 파일: {failed_count}')

    except Exception as e:
        print(f'오류 발생: {str(e)}')


if __name__ == '__main__':
    copy_txt_files()