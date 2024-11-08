import os
import multiprocessing
from pathlib import Path
from functools import partial
from tqdm import tqdm

# 나중에 제거 !
#

def process_text_file(file_path, TEXT_TARGET_KEYWORDS):
    """
    개별 텍스트 파일을 처리하여 광고성 문구 포함 여부를 확인합니다.

    Args:
        file_path (Path): 처리할 텍스트 파일 경로

    Returns:
        tuple: (블로그 ID, 광고성 문구 포함 여부, 발견된 문구 목록)
    """
    try:
        # 파일 읽기
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        if not content.strip():  # 빈 파일 체크
            return file_path.stem, False, []

        # 광고성 문구 검사
        found_keywords = []
        for keyword in TEXT_TARGET_KEYWORDS:
            if keyword in content:
                found_keywords.append(keyword)

        blog_id = file_path.stem  # .txt 확장자를 제외한 파일명
        has_sponsored_text = bool(found_keywords)

        return blog_id, has_sponsored_text, found_keywords

    except Exception as e:
        print(f"Error reading file {file_path}: {str(e)}")
        return file_path.stem, False, []


def get_blog_id_by_text_filtering(TEXT_TARGET_KEYWORDS, txt_base_dir):
    """
    txt 폴더 내의 파일들을 멀티프로세싱으로 순회하며
    광고성 문구가 포함된 블로그 ID를 찾아 반환합니다.

    Args:
        txt_folder_path (str): txt 파일들이 있는 폴더 경로

    Returns:
        tuple: (광고성 문구가 포함된 블로그 ID들의 집합,
               {블로그ID: [발견된 문구 목록]} 형태의 상세 정보 딕셔너리)
    """

    # Path 객체로 변환
    base_path = Path(txt_base_dir)

    # txt 파일 목록 수집
    text_files = [f for f in base_path.iterdir() if f.is_file() and f.suffix == '.txt']

    print(f"총 {len(text_files)}개의 텍스트 파일 처리 시작...")
    print(f"검색할 광고성 문구 수: {len(TEXT_TARGET_KEYWORDS)}개")

    # CPU 코어 수 확인
    num_cores = multiprocessing.cpu_count()
    print(f"사용 가능한 CPU 코어 수: {num_cores}")

    # 멀티프로세싱 풀 생성
    with multiprocessing.Pool(processes=num_cores) as pool:
        process_func = partial(process_text_file, TEXT_TARGET_KEYWORDS=TEXT_TARGET_KEYWORDS)

        # tqdm으로 진행률 표시하면서 병렬 처리
        results = list(tqdm(
            pool.imap(process_func, text_files),
            total=len(text_files),
            desc="파일 처리 중"
        ))

    # 광고성 문구가 포함된 블로그 ID 필터링
    fake_review_blog_ids = set()
    # detailed_results = {}

    for blog_id, has_sponsored, found_keywords in results:
        if has_sponsored:
            fake_review_blog_ids.add(blog_id)
            # detailed_results[blog_id] = found_keywords

    return fake_review_blog_ids   #detailed_results


if __name__ == "__main__":
    # 현재 파일의 상위 폴더의 상위 폴더의 상위 폴더에 있는 data 폴더의 txt 폴더 경로 지정

    # current_dir = os.path.dirname(os.path.abspath(__file__))
    # parent_dir = os.path.dirname(current_dir)
    # grandparent_dir = os.path.dirname(parent_dir)
    # txt_folder_path = os.path.join(grandparent_dir, "data", "txt")

    # 함수 실행
    # sponsored_ids, detailed_info = find_sponsored_blog_ids(txt_folder_path)

    project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    txt_base_dir = os.path.join(project_root, 'data', 'collected_fake_data', 'txt')

    #sponsored_ids = get_blog_id_by_text_filtering(TEXT_TARGET_KEYWORDS, txt_base_dir)

    # 결과 출력
    print(f"\n광고성 문구가 포함된 블로그 수: {len(sponsored_ids)}")


    # 상세 정보 출력
    # print("\n=== 상세 분석 결과 ===")
    # for blog_id, keywords in detailed_info.items():
    #     print(f"\n블로그 ID: {blog_id}")
    #     print(f"발견된 광고성 문구: {', '.join(keywords)}")