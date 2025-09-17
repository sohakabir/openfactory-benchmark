# calc_latency.py
import pandas as pd

# read raw timestamps
df = pd.read_csv("latency.csv", dtype=str)

# parse timestamps (handles trailing 'Z')
df["src_ts"]  = pd.to_datetime(df["src_ts"].str.strip(),  utc=True, errors="coerce")
df["recv_ts"] = pd.to_datetime(df["recv_ts"].str.strip(), utc=True, errors="coerce")

# keep only rows that parsed correctly
df = df.dropna(subset=["src_ts", "recv_ts"])

# compute latency in milliseconds
df["latency_ms"] = (df["recv_ts"] - df["src_ts"]).dt.total_seconds() * 1000

# overwrite the same file
df.to_csv("latency.csv", index=False)

# (optional) quick glance
print(df[["src_ts", "recv_ts", "latency_ms"]].head(10))
