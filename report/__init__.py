from datetime import datetime

def generate_report(leet_data, gfg_data):
    # Convert UNIX timestamps to readable dates
    leetcode_total = leet_data["total"]
    leet_data = {
        datetime.fromtimestamp(int(ts)).strftime("%Y-%m-%d"): count
        for ts, count in leet_data["calender"].items()
    }

    # Merge both datasets
    merged_data = {**leet_data, **gfg_data}

    # Sort data by date
    sorted_data = dict(sorted(merged_data.items()))

    # Calculate totals
    gfg_total = sum(gfg_data.values())

    # Prepare the message
    message_lines = ["*Daily Progress Report*"]
    message_lines.append("")


    # Add LeetCode data
    message_lines.append("*LeetCode Progress:*")
    for date, count in sorted(leet_data.items()):
        message_lines.append(f"  - {date}: {count}")

    message_lines.append(f"Total LeetCode problems solved: {leetcode_total}")
    message_lines.append("")

    # Add GeeksforGeeks data
    message_lines.append("*GeeksforGeeks Progress:*")
    for date, count in sorted(gfg_data.items()):
        message_lines.append(f"  - {date}: {count}")

    message_lines.append(f"Total GeeksforGeeks problems solved: {gfg_total}")

    # Format message for Telegram
    message = "\n".join(message_lines)
    return message
