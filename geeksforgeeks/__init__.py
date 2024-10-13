import os
import requests
def get_gfg_user_profile_data():
    username = os.getenv("GFG_USERNAME", "")
    data = {
        "handle": username,
        "month": "",
        "requestType": "getYearwiseUserSubmissions",
        "year": 2024,
    }
    url = "https://practiceapi.geeksforgeeks.org/api/v1/user/problems/submissions/"
    response = requests.post(url, json=data)
    result = response.json()["result"]
    return result