"""Industrial Predictive Maintenance & Anomaly Detection for Substation Equipment."""

def evaluate_equipment_health(metrics: dict) -> dict:
    temp = metrics.get("temperature_celsius", 25.0)
    pres = metrics.get("pressure_bar", 1.0)
    vib = metrics.get("vibration_rms", 0.01)

    is_anomaly = False
    reasons = []

    if temp > 85.0:
        is_anomaly = True
        reasons.append(f"High temperature threshold exceeded: {temp}C > 85.0C")
    if pres > 15.0:
        is_anomaly = True
        reasons.append(f"High pressure threshold exceeded: {pres} bar > 15.0 bar")
    if vib > 0.048:
        is_anomaly = True
        reasons.append(f"Severe vibration RMS detected: {vib} mm/s > 0.048 mm/s")

    health_score = 100.0 - (len(reasons) * 30.0)
    health_score = max(0.0, health_score)

    return {
        "status": "ANOMALY_DETECTED" if is_anomaly else "NORMAL",
        "health_score": round(health_score, 1),
        "alerts": reasons
    }

if __name__ == "__main__":
    test_reading = {"temperature_celsius": 88.5, "pressure_bar": 12.0, "vibration_rms": 0.052}
    res = evaluate_equipment_health(test_reading)
    print("Health Evaluation:", res)
