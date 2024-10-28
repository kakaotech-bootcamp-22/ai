from utils.title_article_url import get_blog_links, scrape_blog_content

search_query = "맛집 리뷰"
blog_links = get_blog_links(search_query)
scrape_blog_content(blog_links)

