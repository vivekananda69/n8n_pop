import requests

resp = requests.post(
    "https://n8n-pop-3yxb.onrender.com/trigger/forum/US/",
    headers={"X-Trigger-Secret": "f91b2d88219a83f0aaecc3fa4423c8d4"}
)

print("STATUS:", resp.status_code)
print("RESPONSE:", resp.text)
