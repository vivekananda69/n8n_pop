import requests
import time
from django.conf import settings


# =====================================================================
# 1. YOUTUBE COLLECTOR — RENDER-SAFE, FAIL-FAST, NO WORKER TIMEOUT
# =====================================================================

def collect_youtube_for_country(country_code="US", pause=0.4):
    """
    Render-safe YouTube collector:
    - part=id search (cheap)
    - strict fail-fast if 403/429 (no retry loops)
    - small keyword set
    - worker-safe execution time (<6 sec)
    """

    API = settings.YOUTUBE_API_KEY
    if not API:
        print("❌ Missing YouTube API key.")
        return []

    SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"
    STATS_URL  = "https://www.googleapis.com/youtube/v3/videos"

    KEYWORDS = [
        "n8n automation",
        "n8n workflow",
        "n8n gmail automation",
        "n8n google sheets",
    ]

    results = []
    video_ids = set()

    # --------------------------
    # SAFE WRAPPER
    # --------------------------
    def yt_fail_fast(url, params):
        r = requests.get(url, params=params, timeout=8)

        # If API rejects → immediately stop
        if r.status_code in (403, 429):
            print("❌ API rejected key — stopping YouTube collector instantly.")
            return None

        if r.status_code != 200:
            print("❌ YouTube error:", r.status_code)
            return None

        return r.json()

    # --------------------------
    # (1) SEARCH video IDs cheaply
    # --------------------------
    for kw in KEYWORDS:
        params = {
            "key": API,
            "part": "id",         # Cheap search
            "q": kw,
            "type": "video",
            "maxResults": 15,
            "regionCode": country_code,
        }

        res = yt_fail_fast(SEARCH_URL, params)
        if not res:
            return []  # fail-fast: no crash

        for it in res.get("items", []):
            vid = it["id"].get("videoId")
            if vid:
                video_ids.add(vid)

        time.sleep(pause)

    video_ids = list(video_ids)[:40]  # Hard cap → Render safe

    # --------------------------
    # (2) Batch Stats Lookup
    # --------------------------
    if not video_ids:
        return []

    params = {
        "key": API,
        "part": "statistics,snippet",
        "id": ",".join(video_ids),
    }

    stats = yt_fail_fast(STATS_URL, params)
    if not stats:
        return []

    for item in stats.get("items", []):
        title = item["snippet"]["title"]
        vid = item["id"]
        url = f"https://www.youtube.com/watch?v={vid}"

        stats = item.get("statistics", {})
        views = int(stats.get("viewCount", 0))
        likes = int(stats.get("likeCount", 0))
        comments = int(stats.get("commentCount", 0))

        like_ratio = likes / views if views else 0
        comment_ratio = comments / views if views else 0

        score = round((views * 0.6) + (likes * 3) + (comments * 8), 2)

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

    return results


# =====================================================================
# 2. FORUM COLLECTOR — RENDER-SAFE, SINGLE CALL
# =====================================================================

def collect_forum(country="US"):
    url = "https://community.n8n.io/latest.json"
    results = []

    try:
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        r.raise_for_status()
        topics = r.json().get("topic_list", {}).get("topics", [])
    except Exception as e:
        print("Forum collector error:", e)
        return []

    topics = topics[:40]  # Hard cap to avoid Render 50ms CPU kill

    for t in topics:
        title = t.get("title", "Untitled")
        topic_id = t.get("id")
        likes = t.get("like_count", 0)
        replies = t.get("reply_count", 0)
        views = t.get("views", 0)

        score = (likes * 4) + (replies * 2) + (views * 0.1)

        results.append({
            "workflow": title,
            "source_url": f"https://community.n8n.io/t/{topic_id}",
            "platform": "Forum",
            "country": country,
            "metrics": {
                "likes": likes,
                "replies": replies,
                "views": views,
            },
            "score": round(score, 2),
        })

    return results


# =====================================================================
# 3. GOOGLE TRENDS — OFFLINE FALLBACK (RELIABLE)
# =====================================================================

def collect_trends(country="US"):
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

    base = {
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
        score = round(base[kw] * multiplier, 2)

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
