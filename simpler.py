import os, time
from datetime import datetime, timezone
from openfactory.kafka import KSQLDBClient
from openfactory.assets import Asset

CSV_PATH = "latency.csv"

with open(CSV_PATH, "w", encoding="utf-8") as f:
        f.write("src_ts,recv_ts\n")

ksql = KSQLDBClient(ksqldb_url=os.getenv("KSQLDB_URL"))
a = Asset(asset_uuid="VIRTUAL-EVENT-GEN-005", ksqlClient=ksql)
print(a.event_time.value)


START = datetime.now(timezone.utc)  # <— only take events created after this

def on_event(msg_key, msg_value):
    src_ts = str(msg_value["value"])  # your event’s source timestamp
    recv_ts = datetime.now(timezone.utc).isoformat().replace("+00:00","Z")

    # skip backlog (events created before we subscribed)
   
    with open(CSV_PATH, "a", encoding="utf-8") as f:
        f.write(f"{src_ts},{recv_ts}\n")
    print(src_ts, recv_ts)

a.subscribe_to_events(on_event, f"soha_id_live_{int(START.timestamp())}")  # fresh group id 
time.sleep(60)
