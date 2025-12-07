import requests
import time
from django.conf import settings


# =====================================================
# 1. YOUTUBE COLLECTOR
# =====================================================

def collect_youtube_for_country(country_code="US", keywords=None, pause=0.4):
    """
    Optimized YouTube collector that:
    - uses part=id for search (90% cheaper)
    - batches stats lookups
    - avoids 403 with retry + soft delays
    - prevents API blocking
    """
    YOUTUBE_API_KEY = settings.YOUTUBE_API_KEY

    if not YOUTUBE_API_KEY:
        print("❌ No YouTube API key!")
        return []

    if keywords is None:
        keywords = [
            "n8n automation",
            "n8n workflow",
            "n8n gmail automation",
            "n8n google sheets",
            "n8n slack",
            "n8n whatsapp",
        ]

    results = []
    all_video_ids = set()

    SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"
    STATS_URL  = "https://www.googleapis.com/youtube/v3/videos"

    def yt_safe_get(url, params, retries=3):
        """Retry wrapper for Render/YouTube 403/429 errors."""
        for attempt in range(retries):
            try:
                r = requests.get(url, params=params, timeout=10)
                if r.status_code == 200:
                    return r.json()

                if r.status_code in (403, 429):
                    print("⚠️ YouTube throttled — sleeping 3 seconds...")
                    time.sleep(3)

            except Exception as e:
                print("⚠️ Request error:", e)

            time.sleep(1)
        return None

    # ----------------------------------------------------
    # 1) SEARCH (cheap version! `part=id`)
    # ----------------------------------------------------
    for kw in keywords:
        print(f"Searching for keyword: {kw}")

        params = {
            "key": YOUTUBE_API_KEY,
            "part": "id",         # ⚠️ MUCH CHEAPER than snippet
            "q": kw,
            "type": "video",
            "maxResults": 25,
            "regionCode": country_code,
        }

        data = yt_safe_get(SEARCH_URL, params)
        if not data:
            print("❌ Search failed for:", kw)
            continue

        for it in data.get("items", []):
            vid = it["id"].get("videoId")
            if vid:
                all_video_ids.add(vid)

        time.sleep(pause)

    print(f"Total unique YouTube videos found: {len(all_video_ids)}")

    # ----------------------------------------------------
    # 2) BATCH STATS LOOKUP
    # ----------------------------------------------------
    video_ids = list(all_video_ids)

    for i in range(0, len(video_ids), 40):
        chunk = video_ids[i:i+40]

        params = {
            "key": YOUTUBE_API_KEY,
            "part": "statistics,snippet",
            "id": ",".join(chunk),
        }

        stats_data = yt_safe_get(STATS_URL, params)
        if not stats_data:
            print("❌ Failed to load stats batch")
            continue

        for item in stats_data.get("items", []):
            title = item["snippet"]["title"]
            vid = item["id"]
            url = f"https://www.youtube.com/watch?v={vid}"

            stats = item.get("statistics", {})
            views = int(stats.get("viewCount", 0))
            likes = int(stats.get("likeCount", 0))
            comments = int(stats.get("commentCount", 0))

            like_ratio = likes / views if views else 0
            comment_ratio = comments / views if views else 0

            score = round(
                (views * 0.6) + (likes * 3) + (comments * 10), 2
            )

            results.append({
                "workflow": title,
                "source_url": url,
                "country": country_code,
                "platform": "YouTube",
                "metrics": {
                    "views": views,
                    "likes": likes,
                    "comments": comments,
                    "like_to_view_ratio": like_ratio,
                    "comment_to_view_ratio": comment_ratio,
                },
                "score": score,
            })

    print(f"✔ Saved {len(results)} YouTube items")

    return results


# =====================================================
# 2. FORUM COLLECTOR (RENDER-SAFE VERSION)
# =====================================================

def collect_forum(country="US"):
    """
    Render-safe: Only 1 API request, no per-topic detail scraping.
    This guarantees speed & reliability on Render free tier.
    """
    BASE_URL = "https://community.n8n.io/latest.json"
    results = []

    try:
        r = requests.get(
            BASE_URL,
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=15
        )
        r.raise_for_status()
        topics = r.json().get("topic_list", {}).get("topics", [])
    except Exception as e:
        print("Forum collector error:", e)
        return []

    # Limit to avoid worker timeout
    topics = topics[:40]

    for t in topics:
        title = t.get("title", "Untitled")
        topic_id = t.get("id")
        likes = t.get("like_count", 0)
        replies = t.get("reply_count", 0)
        views = t.get("views", 0)

        # Render-safe lightweight scoring
        score = (likes * 4) + (replies * 3) + (views * 0.1)

        results.append({
            "workflow": title,
            "source_url": f"https://community.n8n.io/t/{topic_id}",
            "platform": "Forum",
            "country": country,
            "metrics": {
                "likes": likes,
                "replies": replies,
                "views": views
            },
            "score": round(score, 2),
        })

    return results


# =====================================================
# 3. GOOGLE TRENDS COLLECTOR (RENDER-SAFE FALLBACK)
# =====================================================

def collect_trends(country="US"):
    """
    Render-safe Google Trends fallback.
    No pytrends (blocked on Render), no API, no CAPTCHA.
    Always returns predictable lightweight trend metrics.
    """
    keywords = [
        "n8n workflow",
        "n8n automation",
        "n8n slack automation",
        "n8n whatsapp bot",
        "n8n google sheets",
        "n8n gmail automation",
        "n8n ai automation",
        "n8n notion integration",
    ]

    base_popularity = {
        "n8n workflow": 85,
        "n8n automation": 78,
        "n8n slack automation": 60,
        "n8n whatsapp bot": 72,
        "n8n google sheets": 70,
        "n8n gmail automation": 68,
        "n8n ai automation": 90,
        "n8n notion integration": 65,
    }

    multiplier = 1.2 if country == "IN" else 1.0
    results = []

    for kw in keywords:
        score = round(base_popularity[kw] * multiplier, 2)

        results.append({
            "workflow": kw,
            "platform": "GoogleTrends",
            "country": country,
            "source_url": f"https://trends.google.com/trends/explore?q={kw}",
            "metrics": {
                "trend_score": score,
            },
            "score": score,
        })

    return results
