from pathlib import Path
from typing import Dict, List
import feedparser
import src.config.configuration as config
import json
import datetime
from trafilatura import fetch_url, extract
from tqdm.contrib.concurrent import thread_map

def parse_rss_feed(url: str, category: str = None) -> Dict:

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
        meta_rows: list[dict] = []
        item_urls: list[str] = []
        for item in feed['entries']:
            
            item_url = item.get("link", "")
            item_urls.append(item_url)
            meta_rows.append({
                "title": item.get("title", ""),
                "url": item_url,
                "published_at": item.get("published", ""),
                "category": category,
            })
        contents = list(
            thread_map(
                news_content_extractor,
                item_urls,
                max_workers=config.MAX_WORKER,
                desc=category or "article",
            )
        )
        
        entries = [
            {**meta, "content": content} for meta, content in zip(meta_rows, contents)
        ]
        
        if config.EXPORT_JSON:
            save_to_json(new_entries=entries)

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
    if not feed_url:
        return ""

    try: 
        downloaded = fetch_url(url=feed_url)
        if not downloaded:
            return ""
        content = extract(downloaded)
        return content or ""
    except Exception as e:
        print(f"Error: {e}")
        return ""

def save_to_json(new_entries: Dict) -> None:
    output_dir = Path("src/output")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / f"rss_output_{date_generator()}.json"
    existing_entries: List[Dict[str, str]] = []
    if output_file.exists():
        with open(output_file, "r", encoding="utf-8") as f:
            try:
                existing_entries = json.load(f)
            except json.JSONDecodeError:
                existing_entries = []
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(existing_entries + new_entries, f, ensure_ascii=False, indent=2)