# scripts/06_visual_spotcheck.py
import cv2, json, os, sys
import numpy as np
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import MANIFEST_DIR

with open(os.path.join(MANIFEST_DIR, "manifest_train.json")) as f:
    entries = json.load(f)

# grab one semantic and one rect example
sample = next(e for e in entries if e["mask_type"] == "semantic")
img = cv2.imread(sample["image"])
mask = cv2.imread(sample["mask"], cv2.IMREAD_GRAYSCALE)
heatmap = np.load(sample["heatmap"]).astype(np.float32)

masked_preview = img.copy()
masked_preview[mask > 127] = (0, 0, 255)  # highlight masked region in red

cv2.imwrite("spotcheck_masked.png", masked_preview)
cv2.imwrite("spotcheck_heatmap.png", (heatmap * 255).astype(np.uint8))
print(f"Region: {sample['region']}, mask_type: {sample['mask_type']}")
print(f"Saved spotcheck_masked.png and spotcheck_heatmap.png — open these to verify")
