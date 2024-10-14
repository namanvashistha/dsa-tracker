import time
from dotenv import load_dotenv
from leetcode.sync import send_leetcode_submissions_to_telegram, sync_leetcode_submissions

load_dotenv()

def sync_recent_submissions():
    sync_leetcode_submissions()
    time.sleep(5)
    send_leetcode_submissions_to_telegram()

if __name__ == "__main__":
    sync_recent_submissions()
