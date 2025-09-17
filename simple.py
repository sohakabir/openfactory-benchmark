import os
import time
from datetime import datetime, timezone
from openfactory.kafka import KSQLDBClient
from openfactory.assets import Asset

CSV_PATH = "latency.csv"
if not os.path.exists(CSV_PATH):
    with open(CSV_PATH, "w", encoding="utf-8") as f:
        f.write("src_ts,recv_ts\n")  # header once


ksql = KSQLDBClient(ksqldb_url=os.getenv('KSQLDB_URL'))
a = Asset(asset_uuid='VIRTUAL-EVENT-GEN-001', ksqlClient=ksql)
print(a.event_time.value)


def on_event(msg_key, msg_value):
    src_ts = str(msg_value['value'])  # what you already print first
    recv_ts = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    # append to CSV
    with open(CSV_PATH, "a", encoding="utf-8") as f:
        f.write(f"{src_ts},{recv_ts}\n")
        
    print(msg_value['value'], datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"))
   



a.subscribe_to_events(on_event, 'soha_id')


time.sleep(60)
