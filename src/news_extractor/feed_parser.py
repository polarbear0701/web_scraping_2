from pathlib import Path
from typing import Dict, List
import feedparser
import src.config.configuration as config
import json
import datetime

def parse_rss_feed(url: str, category: str = None) -> Dict:
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
                    "published_at": item["published"],
                    "category": category
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
    return_date = f"{date.date()}-{date.strftime("%H")}h"
    return return_date
    