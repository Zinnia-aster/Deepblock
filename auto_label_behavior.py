import pandas as pd

df = pd.read_csv("model_data/behavior_log.csv")

def label_row(row):
    # Rule 1: Tiny SYN packets → suspicious
    if row["is_syn"] == 1 and row["packet_len"] < 70:
        return "suspicious"

    # Rule 2: Unusual destination ports → suspicious
    if row["dst_port"] not in [80, 443, 22]:  
        return "suspicious"

    # Rule 3: Large packets to unknown ports → suspicious
    if row["packet_len"] > 1000 and row["dst_port"] > 1024:
        return "suspicious"

    # Else, treat as normal
    return "normal"

df["label"] = df.apply(label_row, axis=1)
df.to_csv("model_data/labeled_behavior_log.csv", index=False)

print(f"✅ Done. Labeled {len(df)} entries and saved to labeled_behavior_log.csv")
