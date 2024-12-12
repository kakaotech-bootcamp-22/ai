import os
import shutil

import pandas as pd

# 원본 CSV 파일 경로와 저장할 폴더 경로
input_folder = '/Users/admin/PycharmProjects/ai-jo_crawler/data/fake_data/csv'
output_folder = '/Users/admin/PycharmProjects/ai-jo_crawler/data/fake_data/csv2'

# output_folder가 있으면 제거하고 새로 생성
if os.path.exists(output_folder):
    shutil.rmtree(output_folder)
os.makedirs(output_folder)

# csv 폴더 내 모든 .csv 파일 처리
for filename in os.listdir(input_folder):
    if filename.endswith('.csv'):
        # 파일 경로 설정
        file_path = os.path.join(input_folder, filename)

        # CSV 파일 로드 및 blog_id 기준 중복 제거
        df = pd.read_csv(file_path)
        df_unique = df.drop_duplicates(subset=['blog_id'])

        # 중복이 제거된 CSV 파일을 csv2 폴더에 저장
        output_path = os.path.join(output_folder, filename)
        df_unique.to_csv(output_path, index=False)

        print(f"{filename} 처리 완료. 중복 제거 후 저장 위치: {output_path}")
