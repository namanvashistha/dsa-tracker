import os
import json
import requests


def get_leet_user_profile_data():
    username = os.getenv("LEETCODE_USERNAME", "")
    data = {
        "query": (
            "query userProfileCalendar($username: String!, $year: Int) { matchedUser(username: $username)"
            "{userCalendar(year: $year) {submissionCalendar}}}"
        ),
        "variables": {"username": username},
        "operationName": "userProfileCalendar",
    }
    url = "https://leetcode.com/graphql/"
    response = requests.post(url, json=data)
    
    result = {}
    result["calender"] = json.loads(response.json()["data"]["matchedUser"]["userCalendar"][
        "submissionCalendar"
    ])
    data = {
        "query": "\n    query languageStats($username: String!) {\n  matchedUser(username: $username) {\n    languageProblemCount {\n      languageName\n      problemsSolved\n    }\n  }\n}\n    ",
        "variables": {"username": username},
        "operationName": "languageStats",
    }
    response = requests.post(url, json=data)
    print(response.text)
    for sub in response.json()["data"]["matchedUser"]["languageProblemCount"]:
        if sub["languageName"] == "Python3":
            result["total"] = sub["problemsSolved"]
    return result
