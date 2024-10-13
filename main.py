import os
from dotenv import load_dotenv
from geeksforgeeks import get_gfg_user_profile_data
from leetcode import get_leet_user_profile_data
from telegram.send_message import send_image, send_msg
from report import generate_image, generate_report, generate_totals_report

load_dotenv()

def send_dsa_stats_to_telegram():
    leet_data = get_leet_user_profile_data()
    gfg_data = get_gfg_user_profile_data()
    data = str(leet_data) + str(gfg_data)
    message = generate_totals_report(
        leet_data=leet_data,
        gfg_data=gfg_data,
    )
    # image_path = generate_image(
    #     leet_data=leet_data,
    #     gfg_data=gfg_data,
    #     )
    send_msg(message)
    # send_image(image_path)


if __name__ == "__main__":
    send_dsa_stats_to_telegram()
