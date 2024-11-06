import os
import pytesseract
from PIL import Image
from pathlib import Path
import re
from tqdm import tqdm
import multiprocessing
from functools import partial

# pytesseract 경로 변경
pytesseract.pytesseract.tesseract_cmd = "/opt/homebrew/bin/tesseract"

TARGET_KEYWORDS = ('소정의 원고료', '일정액의 수수료', '소정의 적립금', '제공받아', '지원받아', '체험단')  # '광고' -> 광고/지원이 전혀 없는, '원고료', '수수료', '제품'

def get_image_number(filename):
    """이미지 파일명에서 숫자를 추출합니다."""
    match = re.search(r'(\d+)', filename)
    return int(match.group(1)) if match else 0


def check_text_in_image(image_path, scale_percent=50):
    """
    이미지에서 특정 텍스트를 찾습니다.

    Args:
        image_path (str): 이미지 파일 경로
        target_text (str): 찾을 텍스트
        scale_percent (int): 이미지 크기 축소 비율 (%)
    Returns:
        bool: 텍스트 포함 여부
    """
    try:
        # 이미지 로드 및 크기 축소
        with Image.open(image_path) as img:
            # 이미지가 너무 작지 않은 경우에만 크기 축소
            if img.width > 1000 or img.height > 1000:
                new_width = int(img.width * scale_percent / 100)
                new_height = int(img.height * scale_percent / 100)
                img = img.resize((new_width, new_height))

            # OCR 설정 (빠른 처리를 위한 옵션 추가)
            custom_config = '--psm 3 -l kor --dpi 300 --oem 1'

            # 텍스트 추출
            text = pytesseract.image_to_string(img, config=custom_config, lang='kor')

            # 추출한 텍스트에 target_text 있는지 확인
            for keyword in TARGET_KEYWORDS:
                if keyword in text:
                    return True

            return False

    except FileNotFoundError:
        print(f"이미지 파일을 찾을 수 없습니다: {image_path}")
    except pytesseract.TesseractNotFoundError:
        print("Tesseract OCR이 설치되지 않았거나 경로가 올바르지 않습니다.")
    except IOError:
        print(f"이미지 파일을 열 수 없습니다 (파일이 손상되었거나 지원되지 않는 형식일 수 있음): {image_path}")
    except pytesseract.pytesseract.TesseractError as e:
        print(f"OCR 처리 중 오류 발생: {str(e)}")
    except Exception as e:
        print(f"알 수 없는 오류 발생: {image_path}")
        print(f"에러: {str(e)}")

    return False


def process_blog_folder(blog_folder, max_images=7):
    """
    한 블로그 폴더의 이미지들을 처리합니다.

    Args:
        blog_folder (Path): 블로그 폴더 경로
        max_images (int): 확인할 최대 이미지 수
    Returns:
        tuple: (블로그 ID, 광고 포함 여부)
    """
    blog_id = blog_folder.name

    # 이미지 파일 가져오기
    image_files = list(blog_folder.glob("*.jpg"))

    if not image_files:
        return (blog_id, False)

    # 번호 기준 내림차순 정렬
    image_files.sort(key=lambda x: get_image_number(x.name), reverse=True)


    # 뒤에서부터 지정된 수의 이미지만 확인
    for img_path in image_files[:max_images]:
        if check_text_in_image(img_path):
            return (blog_id, True)

    return (blog_id, False)


def find_sponsored_posts(base_dir, max_images=7):
    """
    저장된 이미지에서 '소정의 원고료' 문구가 포함된 블로그 ID를 찾습니다.

    Args:
        base_dir (str): 블로그 ID 폴더들이 있는 기본 디렉토리 경로
        max_images (int): 각 폴더에서 확인할 최대 이미지 수
    Returns:
        set: 광고성 게시물이 있는 블로그 ID 집합
    """

    base_path = Path(base_dir)
    blog_folders = [f for f in base_path.iterdir() if f.is_dir()]

    print(f"총 {len(blog_folders)}개의 블로그 폴더 처리 시작...")

    # CPU 코어 수 확인
    num_cores = multiprocessing.cpu_count()
    print(f"사용 가능한 CPU 코어 수: {num_cores}")

    # 멀티프로세싱 풀 생성
    with multiprocessing.Pool(processes=num_cores) as pool:
        # 부분 함수를 생성하여 max_images 파라미터 고정
        process_func = partial(process_blog_folder, max_images=max_images)

        # tqdm으로 진행률 표시하면서 병렬 처리
        results = list(tqdm(
            pool.imap(process_func, blog_folders),
            total=len(blog_folders),
            desc="폴더 처리 중"
        ))

    # 광고가 포함된 블로그 ID만 필터링
    fake_review_blog_ids = {blog_id for blog_id, has_ad in results if has_ad}

    return fake_review_blog_ids


# 사용 예시
if __name__ == "__main__":
    img_base_dir = "../data/img"
    # 시작 시간 기록
    import time

    start_time = time.time()

    # 뒤에서 5개 이미지만 확인
    fake_review_blog_ids = find_sponsored_posts(img_base_dir, max_images=5)

    # 종료 시간 기록 및 출력
    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"\n처리 완료!")
    print(f"소요 시간: {elapsed_time / 3600:.2f}시간")
    print("광소성 블로그 id:", fake_review_blog_ids)
    print(f"발견된 광고성 블로그 수: {len(fake_review_blog_ids)}")