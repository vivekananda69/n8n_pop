import requests

url = "https://n8n-pop-3yxb.onrender.com/trigger/youtube/US/"

resp = requests.post(
    url,
    headers={"X-Trigger-Secret": "f91b2d88219a83f0aaecc3fa4423c8d4"},
    timeout=30
)

print("STATUS:", resp.status_code)
print("RESPONSE:", resp.text)
