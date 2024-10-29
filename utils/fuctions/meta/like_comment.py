def get_like_comment_count(soup): # 좋아요와 코멘트 개수 세는 함수
    # 좋아요 코멘트 개수: "u_cnt _count" 클래스를 가진 요소를 찾고 텍스트 추출
    like_count_element = soup.find('em', class_='u_cnt _count')
    like_count = 0
    if like_count_element:
        like_count = like_count_element.get_text(strip=True)
        # print("공감 수:", like_count)
    else:
        print("공감 수를 찾을 수 없습니다.")

    # 댓글 개수; "_commentCount" 클래스를 가진 요소를 찾고 텍스트 추출
    comment_count_element = soup.find('em', id='commentCount')
    comment_cnt = 0
    if comment_count_element:
        comment_cnt = comment_count_element.get_text(strip=True)
        # print("댓글 수:", comment_count)
    else:
        print("댓글 수를 찾을 수 없습니다.")

    return like_count, comment_cnt

"""if __name__ == "__main__":
    article(url="https://blog.naver.com/hj861031/223601136491")"""