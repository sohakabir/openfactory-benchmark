import os
import time
from datetime import datetime, timezone
from openfactory.kafka import KSQLDBClient
from openfactory.assets import Asset

ksql = KSQLDBClient(ksqldb_url=os.getenv('KSQLDB_URL'))

latencies = []

def make_callback():
    def on_sample(msg_key, msg_value):
        print(msg_value['attributes'])
        now = datetime.now(tz=timezone.utc)
        timestamp_str = msg_value['attributes']['ingestion_timestamp']
        ingested_at = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
        latency_ms = (now - ingested_at).total_seconds() * 1000
        latencies.append(latency_ms)
        print(f"{msg_key} | latency: {latency_ms:.1f} ms")
    return on_sample

assets = []
for i in range(1, 2):  # OPCUA-SENSOR-001 and OPCUA-SENSOR-002
    uuid = f"OPCUA-SENSOR-{i:03d}"
    a = Asset(asset_uuid=uuid, ksqlClient=ksql)
    a.subscribe_to_attribute(attribute_id='temp', on_message=make_callback())
    a.subscribe_to_attribute(attribute_id='hum', on_message=make_callback())
    assets.append(a)

time.sleep(20)

if latencies:
    print(f"\n--- Combined stats across all assets ({len(latencies)} samples) ---")
    print(f"  min:  {min(latencies):.1f} ms")
    print(f"  max:  {max(latencies):.1f} ms")
    print(f"  mean: {sum(latencies)/len(latencies):.1f} ms")
