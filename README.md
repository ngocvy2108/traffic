
🚦 Smart Traffic Dashboard - FIWARE Project

Hệ thống mô phỏng giám sát giao thông thông minh tại ngã tư, sử dụng nền tảng FIWARE. Gồm các thành phần:
- Cập nhật dữ liệu cảm biến giao thông theo mô hình `TrafficFlowObserved`
- Mô phỏng đèn giao thông theo thời gian thực
- Giao diện bản đồ và biểu đồ phân tích lưu lượng xe
- Kết nối Orion, MongoDB, QuantumLeap, CrateDB bằng Docker

📦 Yêu cầu hệ thống

- [x] Python 3.9+ (đã test với Python 3.11–3.13)
- [x] Docker Desktop (bật trước khi chạy)
- [x] Internet để tải Docker images lần đầu

🚀 Hướng dẫn chạy dự án

1️⃣ Cài đặt

```bash
git clone https://github.com/ngocvy2108/traffic.git
cd traffic
pip install -r requirements.txt
```

Nếu không có `git`, bạn có thể tải [traffic.zip từ GitHub](https://github.com/ngocvy2108/traffic/archive/refs/heads/main.zip) và giải nén.

2️⃣ Chạy hệ thống

```bash
python run_all.py
```

👉 Khi chạy lệnh trên, hệ thống sẽ:
- Tự khởi động các dịch vụ Docker (MongoDB, Orion, CrateDB, QuantumLeap)
- Tự động chờ Orion khởi động xong
- Tự chạy các script Python cần thiết cho hệ thống hoạt động

🌐 Truy cập giao diện

- Dashboard (bản đồ + biểu đồ):  
  👉 http://localhost/index.html  
  (chạy trực tiếp bằng file `index.html` nếu không dùng webserver)

- Các API:
  - http://localhost:5001/traffic/junctions (lấy thông tin giao lộ)
  - http://localhost:5002/... (mô phỏng đèn giao thông)

🧩 Cấu trúc thư mục

```
traffic/
├── docker-compose.yml              # Khởi động MongoDB, Orion, CrateDB, QuantumLeap
├── run_all.py                      # Tự động khởi động toàn bộ hệ thống
├── stop_all.bat                    # Dừng toàn bộ hệ thống
├── update_traffic.py               # Cập nhật dữ liệu giao thông
├── traffic_controller.py           # API dữ liệu giao lộ
├── smart_intersection.py           # Mô phỏng đèn giao thông
├── index.html / script.js / style.css  # Giao diện người dùng
├── requirements.txt                # Thư viện Python cần thiết
└── README.md
```
🛠 Nếu gặp lỗi Orion

Nếu chạy mà báo lỗi như `❌ Không thể kết nối với Orion`, có thể do:
- Docker chưa khởi động xong
- MongoDB chưa hoạt động kịp

Hãy thử:

```bash
docker volume prune
docker-compose down
docker-compose up -d
```

❌ Khi muốn dừng hệ thống

Chỉ cần chạy file:

```bat
stop_all.bat
```

File này sẽ tự động dừng Docker và tắt tất cả script Python đang chạy.

[GitHub cá nhân](https://github.com/ngocvy2108)
