import json, os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import MANIFEST_DIR

def split_manifest():
    with open(os.path.join(MANIFEST_DIR, "full_manifest.json")) as f:
        entries = json.load(f)

    by_split = {"train": [], "val": [], "test": []}
    for e in entries:
        by_split[e["split"]].append(e)

    for split_name, split_entries in by_split.items():
        out_path = os.path.join(MANIFEST_DIR, f"manifest_{split_name}.json")
        with open(out_path, "w") as f:
            json.dump(split_entries, f, indent=2)
        print(f"{split_name}: {len(split_entries)} entries -> {out_path}")

if __name__ == "__main__":
    split_manifest()