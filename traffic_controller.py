from flask import Flask, jsonify
from flask_cors import CORS
import requests
from traffic_models import TrafficFlowObserved

app = Flask(__name__)
CORS(app)

entities = {
    "north_south": "TrafficFlowObserved:north_south",
    "east_west": "TrafficFlowObserved:east_west"
}

def get_entity_data(entity_id):
    url = f"http://localhost:1026/v2/entities/{entity_id}"
    res = requests.get(url, timeout=3)
    res.raise_for_status()
    data = res.json()
    clean_data = {
        key: val.get("value") if isinstance(val, dict) and "value" in val else val
        for key, val in data.items()
    }
    traffic = TrafficFlowObserved(**clean_data)
    intensity = traffic.intensity or 0
    occupancy = traffic.occupancy or 0
    speed = traffic.averageVehicleSpeed or 1
    load = round(intensity * occupancy * (1 / speed), 3)
    decision = "increase green" if load > 0.5 else "normal"
    return {
        "intensity": intensity,
        "occupancy": occupancy,
        "speed": speed,
        "load": load,
        "decision": decision
    }

# ✅ Route cũ để index.html hoạt động
@app.route("/traffic/intersection")
def intersection():
    try:
        return jsonify({
            direction: get_entity_data(entity_id)
            for direction, entity_id in entities.items()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✅ Route mới để lấy lịch sử từ QuantumLeap
@app.route("/traffic/history/<entity_id>")
def history(entity_id):
    try:
        url = f"http://localhost:8668/v2/entities/{entity_id}/attrs"
        res = requests.get(url, timeout=3)
        res.raise_for_status()
        return jsonify(res.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
