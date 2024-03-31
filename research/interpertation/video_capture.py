# import cv2

# def video_capture_and_preprocess(model_input_size, desired_color_format, feature_extractor=None):
#   """
#   Captures video from the webcam, performs pre-processing, and extracts features (optional).

#   Args:
#       model_input_size (tuple): Target size for frames (width, height).
#       desired_color_format (str): Desired color format (e.g., 'BGR', 'RGB').
#       feature_extractor (function, optional): Function to extract specific features.

#   Returns:
#       None: Processes video frames continuously.
#   """

#   # Initialize video capture
#   cap = cv2.VideoCapture(0)

#   while True:
#     # Capture frame-by-frame
#     ret, frame = cap.read()

#     if not ret:
#       print("Error: Frame not captured")
#       break

#     # Pre-processing
#     frame = cv2.resize(frame, model_input_size)  # Resize to model input size
#     frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) if desired_color_format == 'RGB' else frame  # Convert color format (if needed)

#     # Feature extraction (optional)
#     if feature_extractor is not None:
#       features = feature_extractor(frame)
#       # Process or use features as needed

#     # Display the resulting frame
#     cv2.imshow('Preprocessed Frame', frame)

#     # Exit loop on 'q' key press
#     if cv2.waitKey(1) == ord('q'):
#       break

#   # Release capture
#   cap.release()
#   cv2.destroyAllWindows()

# # Example usage (assuming a hand landmark detection model)
# def detect_hand_landmarks(frame):
#   # Replace with your specific hand landmark detection code using OpenCV or other libraries
#   # (assuming it returns a list of landmark coordinates)
#   landmarks = [...]  # Implement hand landmark detection logic here
#   return landmarks

# # Set model input size and desired color format
# model_input_size = (300, 300)
# desired_color_format = 'HSV'

# # Optionally provide a feature extraction function if needed
# feature_extractor = detect_hand_landmarks  # Replace with your feature extraction logic

# # Start video capture and pre-processing
# video_capture_and_preprocess(model_input_size, desired_color_format, feature_extractor)




import cv2
import mediapipe as mp

# Install and import dependencies if not done already
# !pip install mediapipe opencv-python

mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic

cap = cv2.VideoCapture(0)

with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = holistic.process(image)

        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Draw face landmarks
        mp_drawing.draw_landmarks(image, results.face_landmarks, mp_holistic.FACEMESH_TESSELATION,
                                   mp_drawing.DrawingSpec(color=(80, 110, 10), thickness=1, circle_radius=1),
                                   mp_drawing.DrawingSpec(color=(80, 256, 121), thickness=1, circle_radius=1)
                                   )

        # Draw right hand landmarks
        mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS,
                                   mp_drawing.DrawingSpec(color=(80, 22, 10), thickness=2, circle_radius=4),
                                   mp_drawing.DrawingSpec(color=(80, 44, 121), thickness=2, circle_radius=2)
                                   )

        # Draw left hand landmarks
        mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS,
                                   mp_drawing.DrawingSpec(color=(121, 22, 76), thickness=2, circle_radius=4),
                                   mp_drawing.DrawingSpec(color=(121, 44, 250), thickness=2, circle_radius=2)
                                   )

        # Draw pose landmarks
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS,
                                   mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=4),
                                   mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2)
                                   )

        cv2.imshow('Webcam Feed', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()

