def collect_youtube_for_country(country_code="US", keywords=None, max_per_kw=30, pause=0.3):
    if keywords is None:
        keywords = [
            "n8n workflow", "n8n automation", "n8n google sheets",
            "n8n slack", "n8n gmail automation", "n8n whatsapp bot",
            "n8n notion", "n8n airtable", "n8n api automation",
            # add more — keep a long list, we'll call multiple jobs to reach 20k
        ]

    results = []
    for kw in keywords:
        try:
            # search for videos (maxResults limited by API; we may call multiple times with page tokens)
            search_url = "https://www.googleapis.com/youtube/v3/search"
            params = {"part":"snippet", "q": kw, "type":"video", "regionCode":country_code, "maxResults": 50, "key": YOUTUBE_API_KEY}
            r = requests.get(search_url, params=params, timeout=15)
            r.raise_for_status()
            items = r.json().get("items", [])
            video_ids = [it["id"]["videoId"] for it in items if it.get("id", {}).get("videoId")]
            # chunk video_ids to fetch stats in batches of 50
            for i in range(0, len(video_ids), 50):
                chunk = video_ids[i:i+50]
                stats_url = "https://www.googleapis.com/youtube/v3/videos"
                sparams = {"part":"statistics,snippet", "id": ",".join(chunk), "key": YOUTUBE_API_KEY}
                s = requests.get(stats_url, params=sparams, timeout=15)
                s.raise_for_status()
                for item in s.json().get("items", []):
                    # same as before: parse title, stats, compute score
                    ...
                    results.append({...})
                time.sleep(pause)
        except Exception:
            continue
    return results
