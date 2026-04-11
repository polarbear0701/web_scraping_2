from unicodedata import category
import src.news_extractor.feed_parser as fp
from src.source_url.url_collection import rss_dict

# rss = rss_dict['vnexpress']

# for category, url in rss.items():
#     fp.parse_rss_feed(url=url, category=category)


# from trafilatura import fetch_url, extract

# url = "https://vnexpress.net/kien-nghi-lap-quy-du-phong-rui-ro-cho-lao-dong-bi-treo-quyen-loi-bhxh-5060567.html"

# downloaded = fetch_url(url=url)

# result = extract(downloaded)

# print(result)

print(fp.date_generator())