import os
from datetime import datetime, timezone
from pymongo.errors import DuplicateKeyError
from mongo import database


def make_submission_call(lastkey=None):
    username = os.getenv("LEETCODE_USERNAME", "")
    import requests

    cookies = {}

    headers = {}

    params = {
        # "offset": "20",
        "limit": "20",
    }
    if lastkey:
        params["lastkey"] = lastkey

    response = requests.get(
        "https://leetcode.com/api/submissions/",
        params=params,
        cookies=cookies,
        headers=headers,
        timeout=30,
    )
    print(response.status_code)
    return response.json()


def sync_leetcode_submissions_all():
    import time, json

    result = []
    lastkey = None
    submissions = make_submission_call()
    while True:
        result.extend(submissions["submissions_dump"])
        with open("submissions_data.json", "w") as json_file:
            json.dump(result, json_file, indent=4)
        lastkey = submissions["last_key"]
        submissions = make_submission_call(lastkey)
        if not submissions["has_next"]:
            break

        time.sleep(2)


def insert_leetcode_submissions():
    import json

    with open("submissions_data.json") as json_file:
        submissions = json.load(json_file)
    for sub in submissions:
        if sub["status_display"] != "Accepted":
            continue
        result = {
            "_id": f'leetcode_{sub["id"]}',
            "title": sub["title"],
            "title_slug": sub["title_slug"],
            "timestamp": datetime.fromtimestamp(int(sub["timestamp"]), timezone.utc),
            "status": "accepted",
            "telegram_sent": True,
        }
        try:
            if not database.submissions.find_one({"title_slug": result["title_slug"]}):
                database.submissions.insert_one(result)
            else:
                print(result["title_slug"], "already exists")
        except DuplicateKeyError as exp:
            print(exp)
