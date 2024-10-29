## main
- Chrome 옵션 설정 후 크롬 드라이버 초기화
- API 인증 정보 로드
- def get_blog_links(keyword) : keyword를 검색어로 블로그 링크 가져오기


### crawler

blog_content.py (포스트 컨텐츠 데이터)
: 블로그 포스트 제목, 본문 텍스트, 이미지 내 텍스트, 포스트 내 이미지 개수, 포스트 내 이모지 수, 링크 수 크롤링 하는 파일

blog_meta(포스트 메타 데이터)
: 포스트 제목 길이, 포스트 길이, 포스트 업로드 날짜, , 공감 개수, 댓글 개수 크롤링 하는 파일

blogger_meta(블로거 메타 데이터)
: 블로거 자기소개, 블로거 배너, 이웃 수, 블로그 메뉴 개수, 포스트가 속한 메뉴 게시글 개수, 글 업로드 주기, 하루 평균 업로드 개수 크로링 하는 파일


### functions

content
: 포스트 컨텐츠 데이터 크롤링 해오는 함수 폴더

meta
: 포스트 메타 데이터 크롤링 해오는 함수 폴더

### blogger_meta
: 블로거 메타 데이터 크롤링 해오는 함수 폴더

₩₩₩ .
└── ai-crawler/
    ├── main.py
    └── utils/
        ├── crawler/
        │   ├── blog_content.py
        │   ├── blog_meta.py
        │   └── blogger_meta.py
        ├── functions/
        │   ├── blogger_meta
        │   ├── content
        │   └── meta
        ├── search.py
        └── .env
₩₩₩