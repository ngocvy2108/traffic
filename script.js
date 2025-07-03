const centerLat = 10.353769;
const centerLng = 106.362912;

let map = L.map('map').setView([centerLat, centerLng], 19);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

// Đèn Bắc - Nam đặt phía trên giao lộ
let lightMarkerNS = L.marker([10.35405, 106.362912], {
  icon: L.divIcon({
    html: '<i id="icon_static_ns" class="fas fa-traffic-light green-icon"></i>',
    className: '',
    iconSize: [30, 30]
  })
}).addTo(map);

// Đèn Nam - Bắc đặt phía dưới, cùng trạng thái với NS
let lightMarkerSN = L.marker([10.35345, 106.362912], {
  icon: L.divIcon({
    html: '<i id="icon_static_sn" class="fas fa-traffic-light green-icon"></i>',
    className: '',
    iconSize: [30, 30]
  })
}).addTo(map);

// Đèn Đông - Tây đặt bên phải giao lộ
let lightMarkerEW = L.marker([10.353769, 106.36305], {
  icon: L.divIcon({
    html: '<i id="icon_static_ew" class="fas fa-traffic-light red-icon"></i>',
    className: '',
    iconSize: [30, 30]
  })
}).addTo(map);

// Đèn Tây - Đông đặt bên trái, cùng trạng thái với EW
let lightMarkerWE = L.marker([10.353769, 106.36275], {
  icon: L.divIcon({
    html: '<i id="icon_static_we" class="fas fa-traffic-light red-icon"></i>',
    className: '',
    iconSize: [30, 30]
  })
}).addTo(map);

let markerCarsNS = [], markerCarsSN = [], markerCarsEW = [], markerCarsWE = [];

function vietHoaDecision(decision) {
  switch (decision) {
    case "normal": return "Bình thường";
    case "increase green": return "Gia hạn đèn xanh";
    case "reduce": return "Rút ngắn đèn xanh";
    case "hold": return "Giữ nguyên";
    default: return decision;
  }
}

// Biểu đồ
const chart_ns = new Chart(document.getElementById('chart_ns'), {
  type: 'line',
  data: {
    labels: [],
    datasets: [
      { label: 'Tốc độ', data: [], borderColor: 'blue', fill: false },
      { label: 'Mật độ', data: [], borderColor: 'red', fill: false }
    ]
  },
  options: { responsive: false, animation: false }
});

const chart_ew = new Chart(document.getElementById('chart_ew'), {
  type: 'line',
  data: {
    labels: [],
    datasets: [
      { label: 'Tốc độ', data: [], borderColor: 'green', fill: false },
      { label: 'Mật độ', data: [], borderColor: 'orange', fill: false }
    ]
  },
  options: { responsive: false, animation: false }
});

// Xe
function renderQueueCars(queue, direction, lightState) {
  const carSize = [24, 24];
  const carMarkers = direction === 'NS' ? markerCarsNS :
                     direction === 'SN' ? markerCarsSN :
                     direction === 'EW' ? markerCarsEW : markerCarsWE;

  carMarkers.forEach(m => map.removeLayer(m));
  carMarkers.length = 0;

  if (queue === 0) return;

  // Vị trí ban đầu & kết thúc
  let startLat, startLng, stopLat, stopLng;

  if (direction === 'NS') {
    startLat = 10.3545;
    startLng = 106.362912;
    stopLat = 10.35430; 
    stopLng = 106.362912;
  } else if (direction === 'SN') {
    startLat = 10.3529;
    startLng = 106.362912;
    stopLat = 10.35325;
    stopLng = 106.362912;
  } else if (direction === 'EW') {
    startLat = 10.353769;
    startLng = 106.3634;
    stopLat = 10.353769;
    stopLng = 106.36255;
  } else if (direction === 'WE') {
    startLat = 10.353769;
    startLng = 106.3623;
    stopLat = 10.353768;
    stopLng = 106.3632;
  }

  let iconHTML = (direction === 'NS' || direction === 'SN')
    ? '<i class="fas fa-car" style="font-size:24px; color: gray;"></i>'
    : '<i class="fas fa-car-side" style="font-size:24px; color: gray;"></i>';

  let marker = L.marker([startLat, startLng], {
    icon: L.divIcon({ html: iconHTML, className: '', iconSize: carSize })
  }).addTo(map);

  carMarkers.push(marker);

  if (lightState === 'green') {
    // Di chuyển qua ngã tư mượt
    let steps = 30;
    let step = 0;
    let deltaLat = (stopLat - startLat) / steps;
    let deltaLng = (stopLng - startLng) / steps;

    let interval = setInterval(() => {
      step++;
      let newLat = startLat + deltaLat * step;
      let newLng = startLng + deltaLng * step;
      marker.setLatLng([newLat, newLng]);

      if (step >= steps) {
        clearInterval(interval);
        map.removeLayer(marker); // Xoá xe khi chạy xong
      }
    }, 50);
  } else {
    // Đèn đỏ: dừng ngay trước đèn
    marker.setLatLng([stopLat, stopLng]);
  }
}

// Cập nhật dữ liệu
async function updateData() {
  try {
    let res1 = await fetch("http://127.0.0.1:5001/traffic/intersection");
    let data = await res1.json();
    let ns = data.north_south;
    let ew = data.east_west;

    const colorByLoad = load => load > 0.7 ? 'red' : load > 0.4 ? 'orange' : 'green';

    document.getElementById("info_text_ns").innerHTML = 
      `<h4 style="color:${colorByLoad(ns.load)}">Hướng Bắc - Nam</h4>
      <p>Tốc độ: ${ns.speed} km/h</p>
      <p>Mật độ: ${ns.intensity}</p>
      <p>Tỷ lệ chiếm dụng: ${(ns.occupancy * 100).toFixed(1)}%</p>
      <p>Mức tải: ${ns.load}</p>
      <p>Quyết định: <strong>${vietHoaDecision(ns.decision)}</strong></p>`;

    document.getElementById("info_text_ew").innerHTML = 
      `<h4 style="color:${colorByLoad(ew.load)}">Hướng Đông - Tây</h4>
      <p>Tốc độ: ${ew.speed} km/h</p>
      <p>Mật độ: ${ew.intensity}</p>
      <p>Tỷ lệ chiếm dụng: ${(ew.occupancy * 100).toFixed(1)}%</p>
      <p>Mức tải: ${ew.load}</p>
      <p>Quyết định: <strong>${vietHoaDecision(ew.decision)}</strong></p>`;

    const now = new Date().toLocaleTimeString();
    chart_ns.data.labels.push(now);
    chart_ns.data.datasets[0].data.push(ns.speed);
    chart_ns.data.datasets[1].data.push(ns.intensity);
    chart_ew.data.labels.push(now);
    chart_ew.data.datasets[0].data.push(ew.speed);
    chart_ew.data.datasets[1].data.push(ew.intensity);

    if (chart_ns.data.labels.length > 20) {
      chart_ns.data.labels.shift();
      chart_ns.data.datasets.forEach(ds => ds.data.shift());
      chart_ew.data.labels.shift();
      chart_ew.data.datasets.forEach(ds => ds.data.shift());
    }

    chart_ns.update();
    chart_ew.update();

    let res2 = await fetch("http://127.0.0.1:5002/intersection/status");
    let light = await res2.json();

    document.getElementById("icon_ns").className = `fas fa-circle ${light.north_south.state === "green" ? "green-icon" : "red-icon"}`;
    document.getElementById("icon_ew").className = `fas fa-circle ${light.east_west.state === "green" ? "green-icon" : "red-icon"}`;
    document.getElementById("icon_static_ns").className = `fas fa-traffic-light ${light.north_south.state === "green" ? "green-icon" : "red-icon"}`;
    document.getElementById("icon_static_ew").className = `fas fa-traffic-light ${light.east_west.state === "green" ? "green-icon" : "red-icon"}`;
    document.getElementById("icon_static_sn").className = `fas fa-traffic-light ${light.north_south.state === "green" ? "green-icon" : "red-icon"}`;
    document.getElementById("icon_static_we").className = `fas fa-traffic-light ${light.east_west.state === "green" ? "green-icon" : "red-icon"}`;

    document.getElementById("queue_ns").textContent = light.north_south.queue;
    document.getElementById("green_ns").textContent = light.north_south.green_time;
    document.getElementById("red_ns").textContent = light.north_south.red_time;

    document.getElementById("queue_ew").textContent = light.east_west.queue;
    document.getElementById("green_ew").textContent = light.east_west.green_time;
    document.getElementById("red_ew").textContent = light.east_west.red_time;

    // Render xe cho cả 4 hướng
    renderQueueCars(1, 'NS', light.north_south.state);
    renderQueueCars(1, 'SN', light.north_south.state);
    renderQueueCars(1, 'EW', light.east_west.state);
    renderQueueCars(1, 'WE', light.east_west.state);

  } catch (e) {
    console.error("Lỗi khi fetch dữ liệu:", e);
  }
}

setInterval(updateData, 1000);
updateData();
