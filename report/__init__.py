import os
import json
import pytz
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates
from pprint import pprint


def generate_totals_report(leet_data, gfg_data):
    # Convert UNIX timestamps to readable dates

    datetime_now = datetime.now(pytz.timezone('Asia/Kolkata')).strftime("%d, %B %Y")
    leetcode_total = leet_data["total"]
    gfg_total = gfg_data["total"]
    leetcode_diff, gfg_diff = 0, 0
    if not os.path.exists("db"):
        os.makedirs("db")
    totals_file_path = "db/totals.txt"
    if not os.path.isfile(totals_file_path):
        with open(totals_file_path, "w", encoding="utf-8") as f:
            f.write("{}")  # Initial values
    with open(totals_file_path, "r", encoding="utf-8") as f:
        totals = json.loads(f.read())
        leetcode_diff = leetcode_total - totals.get("leetcode_total", 0)
        gfg_diff = gfg_total - totals.get("gfg_total", 0)
    with open(totals_file_path, "w", encoding="utf-8") as f:
        totals = {
            "leetcode_total": leetcode_total,
            "gfg_total": gfg_total,
        }
        f.write(json.dumps(totals))

    message_lines = []
    message_lines.append(f"*{datetime_now}*\n")
    message_lines.append(f"LeetCode: {leetcode_diff}")
    message_lines.append(f"GFG: {gfg_diff}")
    message = "\n".join(message_lines)
    return message


def generate_report(leet_data, gfg_data):
    # Convert UNIX timestamps to readable dates
    leetcode_total = leet_data["total"]
    leet_data["calender"] = {
        datetime.fromtimestamp(int(ts)).strftime("%Y-%m-%d"): count
        for ts, count in leet_data["calender"].items()
    }
    # Merge both datasets
    merged_data = {**leet_data, **gfg_data}

    # Sort data by date
    sorted_data = dict(sorted(merged_data.items()))

    # Calculate totals
    gfg_total = gfg_data["total"]
    # Prepare the message
    message_lines = ["*Daily Progress Report*"]
    message_lines.append("")

    # Add LeetCode data
    message_lines.append("*LeetCode Progress:*")
    for date, count in sorted(leet_data["calender"].items()):
        message_lines.append(f"  - {date}: {count}")

    message_lines.append(f"Total LeetCode problems solved: {leetcode_total}")
    message_lines.append("")

    # Add GeeksforGeeks data
    message_lines.append("*GeeksforGeeks Progress:*")
    for date, count in sorted(gfg_data["calender"].items()):
        message_lines.append(f"  - {date}: {count}")

    message_lines.append(f"Total GeeksforGeeks problems solved: {gfg_total}")

    # Format message for Telegram
    message = "\n".join(message_lines)
    return message


def generate_image(leet_data, gfg_data):
    # Calculate total values
    leetcode_total = leet_data["total"]
    gfg_total = gfg_data["total"]

    # Get today's date
    today_date = datetime.now().strftime("%Y-%m-%d")

    # Create a figure and axis
    fig, ax = plt.subplots(figsize=(8, 5))

    # Set background color
    fig.patch.set_facecolor("#ffffff")  # White background

    # Hide axes
    ax.axis("off")

    # Create a modern header for the image
    ax.text(
        0.5,
        0.85,
        f"Today's Date: {today_date}",
        fontsize=18,
        ha="center",
        color="#333333",
        fontweight="bold",
    )

    # LeetCode Total Card
    ax.text(
        0.5,
        0.6,
        "LeetCode Total",
        fontsize=24,
        ha="center",
        color="#007bff",
        fontweight="bold",
    )
    ax.text(
        0.5,
        0.45,
        str(leetcode_total),
        fontsize=48,
        ha="center",
        color="#007bff",
        fontweight="bold",
    )

    # GFG Total Card
    ax.text(
        0.5,
        0.25,
        "GFG Total",
        fontsize=24,
        ha="center",
        color="#28a745",
        fontweight="bold",
    )
    ax.text(
        0.5,
        0.1,
        str(gfg_total),
        fontsize=48,
        ha="center",
        color="#28a745",
        fontweight="bold",
    )

    # Add a subtle line to separate sections
    ax.plot(
        [0.1, 0.9], [0.55, 0.55], color="black", lw=1.5, alpha=0.3
    )  # Line below date
    ax.plot(
        [0.1, 0.9], [0.35, 0.35], color="black", lw=1.5, alpha=0.3
    )  # Line below LeetCode total

    # Adjust layout
    plt.tight_layout()

    # Save the image
    image_path = "db/total_overview.png"
    plt.savefig(image_path, dpi=300, bbox_inches="tight", transparent=True)
    plt.show()  # Optional: Show the image
    return image_path
