import os
import pytz
from datetime import datetime, timezone
import requests

from pymongo.errors import DuplicateKeyError
from mongo import database
from telegram.send_message import send_msg

IST_TIMEZONE = pytz.timezone("Asia/Kolkata")


def sync_leetcode_submissions():
    username = os.getenv("LEETCODE_USERNAME", "")
    url = "https://leetcode.com/graphql/"
    data = {
        "query": "\n    query recentAcSubmissions($username: String!, $limit: Int!) {\n  recentAcSubmissionList(username: $username, limit: $limit) {\n    id\n    title\n    titleSlug\n    timestamp\n  }\n}\n    ",
        "variables": {"username": username, "limit": 30},
        "operationName": "recentAcSubmissions",
    }
    response = requests.post(url, json=data, timeout=30)
    results = []
    for sub in response.json()["data"]["recentAcSubmissionList"]:
        results.append(
            {
                "_id": f'leetcode_{sub["id"]}',
                "title": sub["title"],
                "title_slug": sub["titleSlug"],
                "timestamp": datetime.fromtimestamp(
                    int(sub["timestamp"]), timezone.utc
                ),
                "status": "accepted",
            }
        )

    for result in results:
        try:
            submission = database.submissions.find_one(
                {"title_slug": result["title_slug"]}
            )
            if not submission:
                database.submissions.insert_one(result)
            else:
                database.submissions.update_one(
                    {"title_slug": result["title_slug"]},
                    {"$addToSet": {"ac_timestamps": result["timestamp"]}},
                    {"$set": {"timestamp": result["timestamp"]}},
                )
                if submission["timestamp"] != result["timestamp"]:
                    database.submissions.update_one(
                        {"title_slug": result["title_slug"]},
                        {"$set": {"telegram_sent": True}},
                    )

        except DuplicateKeyError:
            pass
    return results


def send_leetcode_submissions_to_telegram():
    submissions = database.submissions.find(
        {"status": "accepted", "telegram_sent": {"$ne": True}}
    ).sort("timestamp", 1)
    message_lines = []
    for result in submissions:
        utc_timestamp = result["timestamp"].replace(tzinfo=pytz.utc)

        # Convert UTC timestamp to IST
        ist_timestamp = utc_timestamp.astimezone(IST_TIMEZONE)
        formatted_timestamp = ist_timestamp.strftime("%A, %d %b, %Y %I:%M %p")
        message_lines.append(f"🌟 *{result['title']}*\n")
        message_lines.append(f"📅 *{formatted_timestamp}*\n")
        message_lines.append(f"🔗 https://leetcode.com/problems/{result['title_slug']}")
        database.submissions.update_one(
            {"_id": result["_id"]}, {"$set": {"telegram_sent": True}}
        )
        text = "\n".join(message_lines)
        print(text)
        send_msg(text)
        message_lines = []
