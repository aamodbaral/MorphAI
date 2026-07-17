import cv2
import numpy as np
from src.landmarks import REGION_LANDMARKS

def semantic_mask(image_shape, region_name, landmarks, dilation=15):
    h, w = image_shape[:2]
    mask = np.zeros((h, w), dtype=np.uint8)
    idxs = REGION_LANDMARKS[region_name]
    pts = landmarks[idxs].astype(np.int32)
    hull = cv2.convexHull(pts)
    cv2.fillConvexPoly(mask, hull, 255)
    if dilation > 0:
        mask = cv2.dilate(mask, np.ones((dilation, dilation), np.uint8))
    return mask

def random_rect_mask(image_shape, coverage=0.25, aspect_range=(0.5, 2.0), seed=None):
    if seed is not None:
        np.random.seed(seed)
    h, w = image_shape[:2]
    area = h * w * coverage
    aspect = np.random.uniform(*aspect_range)
    mw = int(np.sqrt(area * aspect))
    mh = int(area / max(mw, 1))
    mw, mh = min(mw, w), min(mh, h)
    x = np.random.randint(0, max(1, w - mw))
    y = np.random.randint(0, max(1, h - mh))
    mask = np.zeros((h, w), dtype=np.uint8)
    mask[y:y+mh, x:x+mw] = 255
    return mask