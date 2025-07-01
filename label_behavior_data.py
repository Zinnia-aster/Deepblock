import pandas as pd

df = pd.read_csv("model_data/behavior_log.csv")

def label_row(row):
    # Rule 1: If it's a SYN packet and very small → maybe a scan
    if row['is_syn'] == 1 and row['packet_len'] < 70:
        return 'suspicious'

    # Rule 2: If it's going to a weird port → suspicious
    if row['dst_port'] not in [80, 443, 22]:
        return 'suspicious'

    # Else → normal traffic
    return 'normal'

df['label'] = df.apply(label_row, axis=1)


df.to_csv("model_data/labeled_behavior_log.csv", index=False)
print("✅ Labeled behavior log saved to → model_data/labeled_behavior_log.csv")
