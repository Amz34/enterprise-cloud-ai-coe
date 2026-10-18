"""High-velocity industrial IoT telemetry producer for JAL plant operations."""
import json
import time
from datetime import datetime, timezone

def generate_telemetry(sensor_id: str, temperature: float, pressure: float):
    payload = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "sensor_id": sensor_id,
        "site": "Dhahran-Refinery-Substation-4",
        "metrics": {
            "temperature_celsius": round(temperature, 2),
            "pressure_bar": round(pressure, 2),
            "vibration_rms": 0.042
        },
        "status": "NORMAL"
    }
    return json.dumps(payload)

if __name__ == "__main__":
    print("=== Simulating JAL Industrial IoT Event Stream ===")
    for i in range(5):
        msg = generate_telemetry(f"SEN-DHR-{i:03d}", 78.4 + i * 0.5, 12.1 + (i % 2) * 0.3)
        print(f"Produced event -> {msg}")
        time.sleep(0.3)
    print("=== Stream simulation complete ===")
