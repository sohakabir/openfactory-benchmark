# hist_latency.py
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("latency.csv", dtype=str)

# parse & compute latency_ms if missing
if "latency_ms" not in df.columns:
    df["src_ts"]  = pd.to_datetime(df["src_ts"].str.strip(),  utc=True, errors="coerce")
    df["recv_ts"] = pd.to_datetime(df["recv_ts"].str.strip(), utc=True, errors="coerce")
    df = df.dropna(subset=["src_ts", "recv_ts"])
    df["latency_ms"] = (df["recv_ts"] - df["src_ts"]).dt.total_seconds() * 1000
else:
    df["latency_ms"] = pd.to_numeric(df["latency_ms"], errors="coerce")

lat = df["latency_ms"].dropna()

plt.figure()
plt.hist(lat, bins=(30))                  # single chart, no custom colors/styles
plt.xlabel("Latency (ms)")
plt.ylabel("Count")
plt.title("End-to-end latency")
plt.tight_layout()
plt.savefig("latency_hist.png", dpi=150)
plt.show()

print(f"histogram built from {len(lat)} rows → latency_hist.png")
