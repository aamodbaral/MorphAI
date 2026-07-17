import cv2, os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import TRAIN_DIR
from src.landmarks import get_landmarks

def check_landmark_detection(image_dir, sample_size=8000):
    files = os.listdir(image_dir)[:sample_size]
    failures = []
    for fname in files:
        img = cv2.imread(os.path.join(image_dir, fname))
        if get_landmarks(img) is None:
            failures.append(fname)
    rate = 100 * len(failures) / len(files)
    print(f"Failed on {len(failures)}/{len(files)} images ({rate:.1f}%)")
    return failures

if __name__ == "__main__":
    check_landmark_detection(TRAIN_DIR)