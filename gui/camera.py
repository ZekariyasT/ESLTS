import cv2
from PIL import Image, ImageDraw, ImageFont, ImageTk
import numpy as np
from utils.mediapipe_utils import mediapipe_detection, draw_styled_landmarks
import mediapipe as mp
import os

class Camera:
    def __init__(self, cap, label_camera_preview, isCameraActive, model, font):
        self.cap = cap
        self.label_camera_preview = label_camera_preview
        self.isCameraActive = isCameraActive
        self.model = model
        self.font = font
        self.sequence = []
        self.sentence = []
        self.predictions = []
        self.threshold = 0.75
        self.update_interval = 30  # Time in ms between frames
        self.start_preview()

    def start_preview(self):
        with mp.solutions.holistic.Holistic(
                min_detection_confidence=0.5,
                min_tracking_confidence=0.5) as holistic:
            while self.isCameraActive and self.cap.isOpened():
                ret, frame = self.cap.read()
                if not ret:
                    break

                image, results = mediapipe_detection(frame, holistic)
                draw_styled_landmarks(image, results)
                self.process_sequence(results)
                self.display_frame(image)

                if cv2.waitKey(10) & 0xFF == ord('q'):
                    break

            self.cap.release()
            cv2.destroyAllWindows()

    def process_sequence(self, results):
        keypoints = self.extract_keypoints(results)
        self.sequence.append(keypoints)
        self.sequence = self.sequence[-20:]

        if len(self.sequence) == 20:
            res = self.model.predict(np.expand_dims(self.sequence, axis=0))[0]
            self.predictions.append(np.argmax(res))

            if np.unique(self.predictions[-10:])[0] == np.argmax(res):
                # main_folder_path = "Collected Data"
                main_folder_path = "Greeting_Data7"
                subfolder_names = [f for f in os.listdir(main_folder_path) if os.path.isdir(os.path.join(main_folder_path, f))]
                actions = np.array(subfolder_names)

                if res[np.argmax(res)] > self.threshold:
                    if len(self.sentence) > 0:
                        if actions[np.argmax(res)] != self.sentence[-1]:
                            self.sentence.append(actions[np.argmax(res)])
                    else:
                        self.sentence.append(actions[np.argmax(res)])

            if len(self.sentence) > 5:
                self.sentence = self.sentence[-5:]

    def extract_keypoints(self, results):
        pose = np.array([[res.x, res.y, res.z, res.visibility] for res in results.pose_landmarks.landmark]).flatten() if results.pose_landmarks else np.zeros(33*4)
        face = np.array([[res.x, res.y, res.z] for res in results.face_landmarks.landmark]).flatten() if results.face_landmarks else np.zeros(468*3)
        lh = np.array([[res.x, res.y, res.z] for res in results.left_hand_landmarks.landmark]).flatten() if results.left_hand_landmarks else np.zeros(21*3)
        rh = np.array([[res.x, res.y, res.z] for res in results.right_hand_landmarks.landmark]).flatten() if results.right_hand_landmarks else np.zeros(21*3)
        return np.concatenate([pose, face, lh, rh])


    def display_frame(self, frame):
        # Convert BGR to RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Create PIL Image
        img_pil = Image.fromarray(frame_rgb)

        # Draw text on the image
        draw = ImageDraw.Draw(img_pil)
        draw.text((5, 5), ' '.join(self.sentence), font=self.font, fill=(0, 255, 0))

        # Convert PIL Image to PhotoImage
        imgtk = ImageTk.PhotoImage(image=img_pil)

        # Configure the label with the new image
        self.label_camera_preview.configure(image=imgtk)
        self.label_camera_preview.imgtk = imgtk  # Keep a reference to the image

