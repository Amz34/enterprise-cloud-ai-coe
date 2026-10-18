"""Automated verification test suite for Enterprise Cloud & AI CoE stack."""
import os
import sys

# Add subdirectories to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../streaming')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../ai_mlops')))

from telemetry_producer import generate_telemetry
from telemetry_consumer import TelemetryLakehouseSink
from sovereign_rag_engine import SovereignRAGMatcher
from predictive_maintenance import evaluate_equipment_health

def test_telemetry_streaming_and_lakehouse():
    sink = TelemetryLakehouseSink()
    for i in range(5):
        raw = generate_telemetry(f"SEN-TST-{i}", 80.0 + i, 12.0)
        sink.ingest_record(raw)
    stats = sink.get_summary_stats()
    assert stats["records_ingested"] == 5
    assert stats["avg_temperature_c"] > 0
    assert stats["avg_pressure_bar"] > 0

def test_sovereign_rag_retrieval():
    rag = SovereignRAGMatcher()
    matches = rag.query("piping material specifications", top_k=1)
    assert len(matches) > 0
    assert "ARAMCO-SAES-L-105" in matches[0]["doc_id"]

def test_predictive_maintenance_health():
    normal_reading = {"temperature_celsius": 70.0, "pressure_bar": 10.0, "vibration_rms": 0.02}
    res_normal = evaluate_equipment_health(normal_reading)
    assert res_normal["status"] == "NORMAL"
    assert res_normal["health_score"] == 100.0

    critical_reading = {"temperature_celsius": 92.0, "pressure_bar": 16.5, "vibration_rms": 0.055}
    res_crit = evaluate_equipment_health(critical_reading)
    assert res_crit["status"] == "ANOMALY_DETECTED"
    assert len(res_crit["alerts"]) == 3
    assert res_crit["health_score"] < 50.0

if __name__ == "__main__":
    test_telemetry_streaming_and_lakehouse()
    test_sovereign_rag_retrieval()
    test_predictive_maintenance_health()
    print("All CoE architecture contract tests PASSED!")
