from pathlib import Path
from typing import Dict, List
import feedparser
import src.config.configuration as config
import json

def parse_rss_feed(url: str) -> Dict:
    output_dir = Path("src/output")
    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        feed = feedparser.parse(url)

        if getattr(feed, "bozo", 0):
            return {
                "success": False,
                "error": str(getattr(feed['boze_exception'])),
                "feed_title": None,
                "entries": [],
            }
        

        entries: List[Dict[str, str]] = []
        for item in feed['entries']:
            entries.append(
                {
                    "title": item['title'],
                    "url": item['link'],
                    "published_at": item["published"]
                }
            )
        
        if config.EXPORT_JSON:
            with open(f"{output_dir}/rss_output.json", "w", encoding="utf-8") as f:
                json.dump(entries, f, ensure_ascii=False, indent=2)

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