from flask import Flask, jsonify
from flask_cors import CORS
import random
import time
import threading

app = Flask(__name__)
CORS(app)

# Hướng N-S
ns = {
    "state": "green",
    "green_time": 20,
    "red_time": 0,
    "queue": 0,
    "history_queue": []
}

# Hướng E-W
ew = {
    "state": "red",
    "green_time": 0,
    "red_time": 20,
    "queue": 0,
    "history_queue": []
}

lock = threading.Lock()

def traffic_controller():
    while True:
        with lock:
            # Xe đến ngẫu nhiên (1-3 xe mỗi giây) nếu đèn đỏ
            if ns["state"] == "red":
                ns["queue"] += random.randint(0, 2)
            if ew["state"] == "red":
                ew["queue"] += random.randint(0, 2)

            # Xe đi qua nếu đèn xanh
            if ns["state"] == "green":
                ns["queue"] = max(0, ns["queue"] - random.uniform(1, 3))
            if ew["state"] == "green":
                ew["queue"] = max(0, ew["queue"] - random.uniform(1, 3))

            # Giảm thời gian đèn
            if ns["state"] == "green":
                ns["green_time"] -= 1
                if ns["green_time"] <= 0:
                    ns["state"] = "red"
                    ns["red_time"] = 20
                    ew["state"] = "green"
                    ew["green_time"] = 20
            else:
                ns["red_time"] -= 1

            if ew["state"] == "green":
                ew["green_time"] -= 1
                if ew["green_time"] <= 0:
                    ew["state"] = "red"
                    ew["red_time"] = 20
                    ns["state"] = "green"
                    ns["green_time"] = 20
            else:
                ew["red_time"] -= 1

            # Lưu lịch sử để tính trung bình
            ns["history_queue"].append(ns["queue"])
            ew["history_queue"].append(ew["queue"])

            # Sau mỗi 40 lần, điều chỉnh đèn
            if len(ns["history_queue"]) >= 40:
                avg_ns = sum(ns["history_queue"]) / len(ns["history_queue"])
                avg_ew = sum(ew["history_queue"]) / len(ew["history_queue"])
                if avg_ns > avg_ew + 5:
                    ns["green_time"] += 5
                    print("Tăng thời gian đèn xanh cho N-S lên", ns["green_time"])
                elif avg_ew > avg_ns + 5:
                    ew["green_time"] += 5
                    print("Tăng thời gian đèn xanh cho E-W lên", ew["green_time"])
                ns["history_queue"].clear()
                ew["history_queue"].clear()
        time.sleep(1)

# API
@app.route("/intersection/status")
def intersection_status():
    with lock:
        return jsonify({
            "north_south": {
                "state": ns["state"],
                "queue": round(ns["queue"],1),
                "green_time": ns["green_time"],
                "red_time": ns["red_time"]
            },
            "east_west": {
                "state": ew["state"],
                "queue": round(ew["queue"],1),
                "green_time": ew["green_time"],
                "red_time": ew["red_time"]
            }
        })

if __name__ == "__main__":
    threading.Thread(target=traffic_controller, daemon=True).start()
    app.run(host="0.0.0.0", port=5002)
