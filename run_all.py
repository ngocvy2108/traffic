import subprocess
import time
import requests
import os

base_dir = os.path.dirname(__file__)  # Tự lấy thư mục hiện tại
  
def wait_for_orion():
    print("⏳ Đang chờ Orion khởi động...", end="")
    for i in range(60):  # Tăng lên 60 lần (mỗi lần 2s) = 2 phút
        try:
            r = requests.get("http://localhost:1026/version")
            if r.status_code == 200:
                print(f"\n✅ Orion sẵn sàng sau {i*2} giây!")
                return True
        except Exception:
            pass
        print(".", end="", flush=True)
        time.sleep(2)
    print("\n❌ Không thể kết nối với Orion sau 2 phút.")
    return False

print("🚀 Bắt đầu khởi động Docker...")
subprocess.run(["docker-compose", "up", "-d"], cwd=base_dir)

if wait_for_orion():
    print("▶️ Chạy update_traffic.py...")
    subprocess.Popen(["python", "update_traffic.py"], cwd=base_dir)

    print("▶️ Chạy traffic_controller.py...")
    subprocess.Popen(["python", "traffic_controller.py"], cwd=base_dir)

    print("▶️ Chạy smart_intersection.py...")
    subprocess.Popen(["python", "smart_intersection.py"], cwd=base_dir)
else:
    print("❌ Hủy vì Orion chưa khởi động.")

print("🎉 Hoàn tất! Tất cả tiến trình đang chạy.")
