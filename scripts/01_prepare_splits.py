import pandas as pd
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import PARTITION_CSV, MANIFEST_DIR

def prepare_splits(subset_size = None):
    df = pd.read_csv(PARTITION_CSV)  # columns: image_id, partition
    splits = {0: "train", 1: "val", 2: "test"}

    for code, name in splits.items():
        subset = df[df["partition"] == code]["image_id"].tolist()
        if subset_size:
            # cap size per split proportionally (project-scale subset)
            cap = subset_size if name == "train" else subset_size // 8
            subset = subset[:cap]
        out_path = os.path.join(MANIFEST_DIR, f"filelist_{name}.txt")
        with open(out_path, "w") as f:
            f.write("\n".join(subset))
        print(f"{name}: {len(subset)} images -> {out_path}")

if __name__ == "__main__":
    # project-scale subset: ~8000 train, ~1000 val, ~1000 test
    prepare_splits(subset_size=8000)