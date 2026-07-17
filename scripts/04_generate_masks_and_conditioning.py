import cv2, os, sys, json
import numpy as np
from tqdm import tqdm
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import TRAIN_DIR, VAL_DIR, TEST_DIR, MASK_DIR, HEATMAP_DIR, MANIFEST_DIR
from src.landmarks import get_landmarks, REGION_LANDMARKS
from src.masks import semantic_mask, random_rect_mask
from src.conditioning import build_conditioning_map

SEMANTIC_REGIONS = list(REGION_LANDMARKS.keys())
RECT_COVERAGES = [0.10, 0.25, 0.50]
ONE_SIDED_REGIONS = {"left_eye", "right_eye", "left_eyebrow", "right_eyebrow"}

def process_split(split_name, img_dir):
    entries = []
    files = os.listdir(img_dir)

    for fname in tqdm(files, desc=f"Processing {split_name}"):
        img_path = os.path.join(img_dir, fname)
        img = cv2.imread(img_path)
        if img is None:
            continue
        landmarks = get_landmarks(img)
        if landmarks is None:
            continue

        stem = os.path.splitext(fname)[0]

        # semantic masks
        for region in SEMANTIC_REGIONS:
            mask = semantic_mask(img.shape, region, landmarks)
            one_sided = region in ONE_SIDED_REGIONS
            heatmap = build_conditioning_map(img.shape, landmarks, mask, one_sided=one_sided)

            mask_path = os.path.join(MASK_DIR, f"{stem}_{region}.png")
            heatmap_path = os.path.join(HEATMAP_DIR, f"{stem}_{region}.npy")
            cv2.imwrite(mask_path, mask)
            np.save(heatmap_path, heatmap.astype(np.float16))

            entries.append({
                "image": img_path, "mask": mask_path, "heatmap": heatmap_path,
                "mask_type": "semantic", "region": region, "split": split_name
            })

        # random rectangular masks
        for cov in RECT_COVERAGES:
            mask = random_rect_mask(img.shape, coverage=cov)
            heatmap = build_conditioning_map(img.shape, landmarks, mask, one_sided=False)

            tag = f"rect{int(cov*100)}"
            mask_path = os.path.join(MASK_DIR, f"{stem}_{tag}.png")
            heatmap_path = os.path.join(HEATMAP_DIR, f"{stem}_{tag}.npy")
            cv2.imwrite(mask_path, mask)
            np.save(heatmap_path, heatmap.astype(np.float16))

            entries.append({
                "image": img_path, "mask": mask_path, "heatmap": heatmap_path,
                "mask_type": "rect", "region": tag, "split": split_name
            })

    return entries

if __name__ == "__main__":
    all_entries = []
    all_entries += process_split("train", TRAIN_DIR)
    all_entries += process_split("val", VAL_DIR)
    all_entries += process_split("test", TEST_DIR)

    out_path = os.path.join(MANIFEST_DIR, "full_manifest.json")
    with open(out_path, "w") as f:
        json.dump(all_entries, f, indent=2)
    print(f"Wrote {len(all_entries)} entries to {out_path}")