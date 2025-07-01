import requests
from requests.auth import HTTPBasicAuth

BASE_URL = "http://localhost:8000"
ADMIN_USER = "admin"
ADMIN_PASS = "admin123"

resp = requests.get(
    f"{BASE_URL}/admin/index/stats",
    auth=HTTPBasicAuth(ADMIN_USER, ADMIN_PASS)
)
print(resp.json())