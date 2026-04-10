import feedparser
import trafilatura
from src.source_url.url_collection import rss_dict

url = rss_dict.get("vnexpress").get("technology")

news = feedparser.parse(url)

print(news.keys())
# print(news['entries'])
print(news['entries'][0].keys())