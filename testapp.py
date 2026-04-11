import src.news_extractor.news_extractor as fp
from src.source_url.url_collection import rss_dict

rss = rss_dict['vnexpress']

for category, url in rss.items():
    fp.parse_rss_feed(url=url, category=category)


# from trafilatura import fetch_url, extract

# url = "https://vnexpress.net/ha-van-tien-lan-dau-vo-dich-co-tuong-quoc-gia-5060357.html"

# downloaded = fetch_url(url=url)

# result = extract(downloaded)

# print(result)


# print(fp.news_content_extractor(feed_url=url))
