from pathlib import Path
from typing import Dict, List
import feedparser
import src.config.configuration as config
import json
import datetime
from trafilatura import fetch_url, extract

def parse_rss_feed(url: str, category: str = None) -> Dict:
    output_dir = Path("src/output")
    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        feed = feedparser.parse(url)

        if getattr(feed, "bozo", 0):
            return {
                "success": False,
                "error": str(getattr(feed, "bozo_exception", None)),
                "feed_title": None,
                "entries": [],
            }
        

        entries: List[Dict[str, str]] = []
        for item in feed['entries']:
            item_url = item.get("link", "")
            content = news_content_extractor(feed_url=item_url)
            entries.append(
                {
                    "title": item.get("title", ""),
                    "url": item_url,
                    "published_at": item.get("published", ""),
                    "category": category,
                    "content": content
                }
            )
        
        if config.EXPORT_JSON:
            output_file = output_dir / f"rss_output_{date_generator()}.json"
            existing_entries: List[Dict[str, str]] = []
            if output_file.exists():
                with open(output_file, "r", encoding="utf-8") as f:
                    try:
                        existing_entries = json.load(f)
                    except json.JSONDecodeError:
                        existing_entries = []
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(existing_entries + entries, f, ensure_ascii=False, indent=2)

        return {
            "success": True,
            "error": None,
            "feed_title": feed["feed"]['title'],
            "entries": entries,
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "feed_title": None,
            "entries": [],
        }
        
def date_generator() -> str:
    date = datetime.datetime.now()
    return_date = f"{date.date()}-{date.strftime('%H')}h"
    return return_date

def news_content_extractor(feed_url: str) -> str:
    try: 
        result = extract(fetch_url(url=feed_url))
        return result
    except Exception as e:
        print(f"Error: {e}")
    