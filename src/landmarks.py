import mediapipe as mp
import numpy as np
import cv2

mp_face_mesh = mp.solutions.face_mesh
_face_mesh = mp_face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1, refine_landmarks=True)

REGION_LANDMARKS = {
    "left_eye":      list(range(33, 42)) + list(range(160, 173)),
    "right_eye":     list(range(263, 272)) + list(range(387, 398)),
    "left_eyebrow":  list(range(276, 283)),
    "right_eyebrow": list(range(46, 53)),
    "nose":          list(range(1, 6)) + list(range(97, 100)),
    "mouth":         list(range(61, 68)) + list(range(291, 308)),
}

def get_landmarks(image_bgr):
    h, w = image_bgr.shape[:2]
    results = _face_mesh.process(cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB))
    if not results.multi_face_landmarks:
        return None
    lm = results.multi_face_landmarks[0].landmark
    pts = np.array([[p.x * w, p.y * h] for p in lm], dtype=np.float32)
    return pts  # shape (478, 2) with refine_landmarks=True

def mirror_landmarks(landmarks, image_width):
    mirrored = landmarks.copy()
    mirrored[:, 0] = image_width - mirrored[:, 0]
    return mirrored