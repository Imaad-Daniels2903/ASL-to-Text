import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from pprint import pprint

# 1. Configure HandLandmarker options
base_options = python.BaseOptions(model_asset_path='src/asl_to_text/tracker/hand_landmarker.task')
options = vision.HandLandmarkerOptions(
    base_options=base_options,
    num_hands=2,
    min_hand_detection_confidence=0.5,
    min_tracking_confidence=0.5,
    running_mode=vision.RunningMode.IMAGE
)

# 2. Create the detector instance
detector = vision.HandLandmarker.create_from_options(options)

# Connections mapping landmark indices (equivalent to mp_hands.HAND_CONNECTIONS)
HAND_CONNECTIONS = [
    (0, 1), (1, 2), (2, 3), (3, 4),                 # Thumb
    (0, 5), (5, 6), (6, 7), (7, 8),                 # Index finger
    (5, 9), (9, 10), (10, 11), (11, 12),            # Middle finger
    (9, 13), (13, 14), (14, 15), (15, 16),          # Ring finger
    (13, 17), (0, 17), (17, 18), (18, 19), (19, 20) # Pinky
]

cap = cv2.VideoCapture(0)

while True:
    data, image = cap.read()
    if not data:
        break

    # Flip horizontally and convert BGR to RGB
    rgb_image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    
    # 3. Convert frame to MediaPipe Image object
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_image)

    # 4. Perform hand landmark detection
    result = detector.detect(mp_image)

    # Convert back to BGR for drawing with OpenCV
    display_image = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2BGR)
    h, w, _ = display_image.shape

    # 5. Draw detected landmarks and connections
    if result.hand_landmarks:
        
        for hand_landmarks in result.hand_landmarks:
            # Convert normalized landmarks to pixel coordinates
            pixel_landmarks = [
                (int(lm.x * w), int(lm.y * h)) for lm in hand_landmarks
            ]
            print("cords")
            pprint(pixel_landmarks)

            # Draw connection lines between landmarks
            for start_idx, end_idx in HAND_CONNECTIONS:
                cv2.line(display_image, pixel_landmarks[start_idx], pixel_landmarks[end_idx], (0, 255, 0), 2)

            # Draw landmark keypoints
            for cx, cy in pixel_landmarks:
                cv2.circle(display_image, (cx, cy), 5, (0, 0, 255), -1)

    cv2.imshow('Handtracker (Tasks API)', display_image)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()