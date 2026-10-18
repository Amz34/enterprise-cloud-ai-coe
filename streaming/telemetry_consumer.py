"""Real-time columnar lakehouse ingestion worker for industrial plant telemetry."""
import json
import sqlite3
from datetime import datetime, timezone

class TelemetryLakehouseSink:
    def __init__(self, db_path=":memory:"):
        self.conn = sqlite3.connect(db_path)
        self._init_schema()

    def _init_schema(self):
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS plant_telemetry (
                    timestamp TEXT,
                    sensor_id TEXT,
                    site TEXT,
                    temperature REAL,
                    pressure REAL,
                    vibration REAL,
                    status TEXT
                )
            """)

    def ingest_record(self, raw_json: str):
        record = json.loads(raw_json)
        metrics = record.get("metrics", {})
        with self.conn:
            self.conn.execute("""
                INSERT INTO plant_telemetry VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                record.get("timestamp"),
                record.get("sensor_id"),
                record.get("site"),
                metrics.get("temperature_celsius"),
                metrics.get("pressure_bar"),
                metrics.get("vibration_rms"),
                record.get("status")
            ))

    def get_summary_stats(self):
        cur = self.conn.cursor()
        cur.execute("SELECT COUNT(*), AVG(temperature), AVG(pressure) FROM plant_telemetry")
        count, avg_temp, avg_pres = cur.fetchone()
        return {
            "records_ingested": count,
            "avg_temperature_c": round(avg_temp, 2) if avg_temp else 0.0,
            "avg_pressure_bar": round(avg_pres, 2) if avg_pres else 0.0
        }

if __name__ == "__main__":
    from telemetry_producer import generate_telemetry
    sink = TelemetryLakehouseSink()
    print("Ingesting simulated telemetry stream into columnar lakehouse...")
    for i in range(10):
        data = generate_telemetry(f"SEN-DHR-{i:03d}", 75.0 + i, 12.0 + (i * 0.1))
        sink.ingest_record(data)
    stats = sink.get_summary_stats()
    print(f"Lakehouse Summary -> {stats}")
