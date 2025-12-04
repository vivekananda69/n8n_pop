import requests
import time
from django.conf import settings


def collect_youtube_for_country(country_code="US", keywords=None, pause=0.3):
    YOUTUBE_API_KEY = settings.YOUTUBE_API_KEY

    if not YOUTUBE_API_KEY:
        print("❌ No YOUTUBE_API_KEY found")
        return []

    if keywords is None:
        keywords = [
            "n8n workflow", "n8n automation", "n8n google sheets",
            "n8n slack", "n8n gmail automation", "n8n whatsapp",
            "n8n webhook", "n8n notion", "n8n airtable"
        ]

    results = []

    for kw in keywords:
        try:
            search_url = "https://www.googleapis.com/youtube/v3/search"
            params = {
                "part": "snippet",
                "q": kw,
                "type": "video",
                "regionCode": country_code,
                "maxResults": 50,
                "key": YOUTUBE_API_KEY,
            }

            r = requests.get(search_url, params=params, timeout=10)
            r.raise_for_status()
            items = r.json().get("items", [])

            video_ids = [it["id"]["videoId"] for it in items if it.get("id", {}).get("videoId")]

            # Fetch stats for videos in batches of 50
            for i in range(0, len(video_ids), 50):
                chunk = video_ids[i:i+50]

                stats_url = "https://www.googleapis.com/youtube/v3/videos"
                sparams = {
                    "part": "statistics,snippet",
                    "id": ",".join(chunk),
                    "key": YOUTUBE_API_KEY,
                }

                s = requests.get(stats_url, params=sparams, timeout=10)
                s.raise_for_status()

                for item in s.json().get("items", []):
                    title = item["snippet"]["title"]
                    url = f"https://www.youtube.com/watch?v={item['id']}"

                    stats = item.get("statistics", {})
                    views = int(stats.get("viewCount", 0))
                    likes = int(stats.get("likeCount", 0))
                    comments = int(stats.get("commentCount", 0))

                    # simple scoring to rank items
                    score = views * 0.6 + likes * 3 + comments * 10

                    results.append({
                        "workflow": title,
                        "source_url": url,
                        "metrics": stats,
                        "score": score,
                    })

                time.sleep(pause)

        except Exception as e:
            print("YouTube Collector error:", e)
            continue

    return results
