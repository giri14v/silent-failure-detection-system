# scripts/traffic_simulator.py

import time
import random
import requests

API_URL = "http://127.0.0.1:8000/predict"


def send_request(feature_1, feature_2, feature_3):
    payload = {
        "feature_1": feature_1,
        "feature_2": feature_2,
        "feature_3": feature_3,
    }
    r = requests.post(API_URL, json=payload, timeout=30)
    return r.status_code


def healthy_traffic(n=30, delay=0.6):
    print("\n--- Sending HEALTHY traffic ---")
    for _ in range(n):
        send_request(
            feature_1=random.uniform(20, 40),
            feature_2=random.uniform(0.4, 0.6),
            feature_3=random.uniform(200, 400),
        )
        time.sleep(delay)


# def degrading_traffic(n=40, delay=0.6):
#     print("\n--- Sending DEGRADED traffic ---")
#     for i in range(n):
#         send_request(
#             feature_1=random.uniform(0, 0),      # distribution shift
#             feature_2=random.uniform(0.0, 0.2),   # low signal
#             feature_3=random.uniform(900, 1200),  # extreme range
#         )
#         time.sleep(delay)

def degrading_traffic(n=40, delay=2.0):
    print("\n--- Sending SLOW, LOW-CONFIDENCE traffic ---")

    for _ in range(n):
        send_request(
            feature_1=30,
            feature_2=0.1,
            feature_3=200
        )
        time.sleep(delay)


def recovery_traffic(n=30, delay=0.6):
    print("\n--- Sending RECOVERY traffic ---")
    for _ in range(n):
        send_request(
            feature_1=random.uniform(25, 45),
            feature_2=random.uniform(0.45, 0.65),
            feature_3=random.uniform(250, 450),
        )
        time.sleep(delay)


if __name__ == "__main__":
    # healthy_traffic()
    degrading_traffic()
    # recovery_traffic()