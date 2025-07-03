import requests
import random
import time

ORION_URL = "http://localhost:1026/v2/entities"

# Giao lộ gồm 2 hướng chính
entities = [
    {
        "id": "TrafficFlowObserved:north_south",
        "type": "TrafficFlowObserved",
        "laneDirection": "forward",
        "laneId": 1,
        "location": {
            "type": "Point",
            "coordinates": [105.85, 21.03]
        }
    },
    {
        "id": "TrafficFlowObserved:east_west",
        "type": "TrafficFlowObserved",
        "laneDirection": "forward",
        "laneId": 2,
        "location": {
            "type": "Point",
            "coordinates": [105.8505, 21.0305]
        }
    }
]

# Khởi tạo entity nếu chưa tồn tại
def create_entity_if_not_exists(entity):
    payload = {
        "id": entity["id"],
        "type": entity["type"],
        "intensity": {"value": 0, "type": "Number"},
        "occupancy": {"value": 0, "type": "Number"},
        "averageVehicleSpeed": {"value": 0, "type": "Number"},
        "laneDirection": {"value": entity["laneDirection"], "type": "Text"},
        "laneId": {"value": entity["laneId"], "type": "Number"},
        "location": {"type": "geo:json", "value": entity["location"]}
    }
    res = requests.post(ORION_URL, json=payload)
    if res.status_code == 201:
        print(f"✅ Created entity {entity['id']}")
    elif res.status_code == 422 and "Already Exists" in res.text:
        pass  # Entity đã tồn tại
    else:
        print(f"❌ Create failed: {res.status_code} {res.text}")

# Khởi tạo ban đầu
for entity in entities:
    create_entity_if_not_exists(entity)

# Cập nhật liên tục
# Cập nhật liên tục
while True:
    for entity in entities:
        # Sinh dữ liệu ngẫu nhiên
        intensity = round(random.uniform(20, 50), 2)
        occupancy = round(random.uniform(0.1, 0.9), 2)
        speed = round(random.uniform(30, 60), 2)

        payload = {
            "intensity": {"value": intensity, "type": "Number"},
            "occupancy": {"value": occupancy, "type": "Number"},
            "averageVehicleSpeed": {"value": speed, "type": "Number"},
            "laneDirection": {"value": entity["laneDirection"], "type": "Text"},
            "laneId": {"value": entity["laneId"], "type": "Number"},
            "location": {"type": "geo:json", "value": entity["location"]}
        }

        res = requests.patch(f"{ORION_URL}/{entity['id']}/attrs", json=payload)
        if res.status_code == 204:
            print(f"✅ Updated {entity['id']}: intensity={intensity}, occupancy={occupancy}, speed={speed}")
        else:
            print(f"❌ Failed to update {entity['id']}: {res.status_code} {res.text}")

        time.sleep(1)  # 👉 THÊM DÒNG NÀY
    time.sleep(2)      # Giữ lại để giãn giữa mỗi vòng lặp
