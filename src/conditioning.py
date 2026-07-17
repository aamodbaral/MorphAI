import cv2
import numpy as np
from src.landmarks import mirror_landmarks

def landmarks_to_heatmap(landmarks, image_shape, mask, sigma=4):
    h, w = image_shape[:2]
    heatmap = np.zeros((h, w), dtype=np.float32)
    for (x, y) in landmarks:
        xi, yi = int(x), int(y)
        if 0 <= yi < h and 0 <= xi < w and mask[yi, xi] == 0:
            cv2.circle(heatmap, (xi, yi), 1, 1.0, -1)
    heatmap = cv2.GaussianBlur(heatmap, (0, 0), sigmaX=sigma)
    maxval = heatmap.max()
    if maxval > 1e-8:
        heatmap = heatmap / maxval
    return heatmap

def build_conditioning_map(image_shape, landmarks, mask, one_sided=False):
    if one_sided:
        w = image_shape[1]
        mirrored = mirror_landmarks(landmarks, w)
        return landmarks_to_heatmap(mirrored, image_shape, mask)
    return landmarks_to_heatmap(landmarks, image_shape, mask)