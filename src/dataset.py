import json
import cv2
import numpy as np
import torch
from torch.utils.data import Dataset

def _load_image(path, size=256):
    img = cv2.imread(path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (size, size))
    img = img.astype(np.float32) / 127.5 - 1.0  # normalize to [-1, 1]
    return torch.from_numpy(img).permute(2, 0, 1)  # (3, H, W)

def _load_mask(path, size=256):
    mask = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    mask = cv2.resize(mask, (size, size))
    mask = (mask > 127).astype(np.float32)
    return torch.from_numpy(mask).unsqueeze(0)  # (1, H, W)

def _load_heatmap(path, size=256):
    heatmap = np.load(path).astype(np.float32)
    if heatmap.shape[0] != size:
        heatmap = cv2.resize(heatmap, (size, size))
    return torch.from_numpy(heatmap).unsqueeze(0)  # (1, H, W)

class MorphAIDataset(Dataset):
    def __init__(self, manifest_path, img_size=256):
        with open(manifest_path) as f:
            self.entries = json.load(f)
        self.img_size = img_size

    def __len__(self):
        return len(self.entries)

    def __getitem__(self, idx):
        entry = self.entries[idx]

        gt = _load_image(entry["image"], self.img_size)          # (3, H, W), [-1, 1]
        mask = _load_mask(entry["mask"], self.img_size)           # (1, H, W), {0,1}
        heatmap = _load_heatmap(entry["heatmap"], self.img_size)  # (1, H, W), [0,1]

        masked_rgb = gt * (1 - mask)  # zero out masked region

        return {
            "masked_rgb": masked_rgb,
            "mask": mask,
            "heatmap": heatmap,
            "gt": gt,
            "region": entry["region"],
            "mask_type": entry["mask_type"],
        }