import pandas as pd
import ast

df = pd.read_csv('../data/csv/post_meta_data.csv', header=0, usecols=["blog_id", "img_urls"])

# print(df)

# 광고성 후원성 키워드 : 추후 추가 가능
ad_keywords = ["xn--939au0g4vj8sq", "revu", "reviewnote", "d3i7y4ugnppb9p.cloudfront", "reviewplace", # 강남 맛집, 레뷰, 리뷰노트, 슈퍼멤버스, 리뷰플레이스
               "cometoplay", "mrble1", "storyn", "assaview", "seoulouba", # 놀러와체험단, 미블, 스토리앤미디어, 아싸뷰, 서울오빠
               "4blog", "ringble", "popomon", "modublog", "dailyview", # 모두함께이겨내요,제가..협찬~, 링블, popomon, 업체로부터상품만, 데일리뷰
               "gabom", "hello-dm", "ddokcokr", "vividplanet2dev", "mateb", # 가봄, 소정의수수료지원, 업체로부터지원-진솔리뷰, 마이플레이스, 여기엔다있어/블로그보스/투게더체험단/어바웃라이프
               "reviewjin"] # 리뷰진,

# ... 디너의 여왕,  링블, 서울오빠, 후기업, , 클라우드리뷰
fake_review_blog_id = []

# print(df)

count = 0
for index, row in df.iterrows():
    count+=1
    if row["img_urls"] =='[]':
        continue

    # urls = row["img_urls"]

    # 문자열을 리스트로 변환 (필요한 경우)
    try:
        urls = ast.literal_eval(row["img_urls"]) if isinstance(row["img_urls"], str) else row["img_urls"]
    except ValueError:
        print(f"Error parsing img_urls for row {index}")
        continue

    # 각 행 별 리스트 뒤에서부터 순회
    for url in reversed(urls):
        # ad_keywords의 키워드 중 하나라도 url에 포함되어 있으면
        if any(keyword in url for keyword in ad_keywords):
            fake_review_blog_id.append(row["blog_id"])
            break

print(count)
print(fake_review_blog_id)
print(len(fake_review_blog_id))