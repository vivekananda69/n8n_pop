import requests

BASE = "https://n8n-pop-3yxb.onrender.com/trigger"
SECRET = "f91b2d88219a83f0aaecc3fa4423c8d4"

sources = ["youtube", "forum", "trends"]
countries = ["US", "IN"]

for src in sources:
    for c in countries:
        url = f"{BASE}/{src}/{c}/"
        print("\nTesting:", url)

        resp = requests.post(url, headers={"X-Trigger-Secret": SECRET})
        print("STATUS:", resp.status_code)
        print("RESPONSE:", resp.text)
