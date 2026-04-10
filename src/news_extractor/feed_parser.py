from typing import Dict
import feedparser

def parse_rss_feed(url: str) -> Dict:
    try:
        feedparser.parse(url)
        
    except Exception as e:
        print(e)