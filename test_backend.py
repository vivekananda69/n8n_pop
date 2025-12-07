import requests, time

url = "https://n8n-pop-3yxb.onrender.com/api/workflows"
start = time.time()

resp = requests.get(url + "?limit=10", timeout=60)
end = time.time()

print("STATUS:", resp.status_code)
print("TIME:", round(end - start, 2), "sec")
print(resp.text[:500])
