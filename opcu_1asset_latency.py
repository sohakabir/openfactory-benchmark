import os
import time
from datetime import datetime, timezone
from openfactory.kafka import KSQLDBClient
from openfactory.assets import Asset

ksql = KSQLDBClient(ksqldb_url=os.getenv('KSQLDB_URL'))
a = Asset(asset_uuid='OPCUA-SENSOR-001', ksqlClient=ksql)

latencies = []

def on_sample(msg_key, msg_value):
    timestamp_str = msg_value['attributes']['ingestion_timestamp']
    ingested_at = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
    now = datetime.now(tz=timezone.utc)
    latency_ms = (now - ingested_at).total_seconds() * 1000
    latencies.append(latency_ms)
    print(f"{msg_key} | ingested: {ingested_at} | latency: {latency_ms:.1f} ms")

a.subscribe_to_attribute(attribute_id='temp', on_message=on_sample)

time.sleep(60)

if latencies:
    print(f"\n--- Stats over {len(latencies)} samples ---")
    print(f"  min:  {min(latencies):.1f} ms")
    print(f"  max:  {max(latencies):.1f} ms")
    print(f"  mean: {sum(latencies)/len(latencies):.1f} ms")