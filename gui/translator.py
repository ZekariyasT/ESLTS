import tkinter as tk
from tkinter import ttk
from pathlib import Path
from PIL import Image, ImageTk, ImageFont, ImageDraw
import threading
import tensorflow as tf
from utils.mediapipe_utils import mediapipe_detection, draw_styled_landmarks
from utils.gui_utils import create_button
import cv2
import constants as const

ASSETS_PATH = Path(__file__).resolve().parent.parent / "assets" / "Image"

class Translator:
    def __init__(self, window):
        self.window = window
        self.setup_window()
        self.isCameraActive = False
        self.create_widgets()
        self.progressbar = ttk.Progressbar(window, mode="indeterminate")
        self.load_model()

    def setup_window(self):
        self.window.title("ETHSLT")
        self.window.iconbitmap("icon.ico")
        self.window.geometry("1240x630+0+0")
        self.window.configure(bg="#3A7FF6")

    def create_widgets(self):
        self.canvas = tk.Canvas(self.window, bg="#3A7FF6", height=900, width=1800, bd=0, highlightthickness=0, relief="ridge")
        self.canvas.place(x=0, y=0)
        self.canvas.create_rectangle(600, 0, 1800, 900, fill="#FCFCFC", outline="")

        self.background_image = tk.PhotoImage(file=ASSETS_PATH / const.backgroundImage)
        self.canvas.create_image(300, 600, image=self.background_image)

        self.label_camera_preview = tk.Label(self.window)
        self.label_camera_preview.place(x=930, y=250, anchor=tk.CENTER)

        self.create_labels()
        self.load_images()
        create_button(self, const.generate)

    def create_labels(self):
        title = tk.Label(text="Welcome to ETHSLT", bg="#3A7FF6", fg="white", justify="left", font=("Arial-BoldMT", 20))
        title.place(x=20.0, y=120.0)
        self.canvas.create_rectangle(25, 160, 85, 165, fill="#FCFCFC", outline="")

        info_text = tk.Label(text=const.infoText, bg="#3A7FF6", fg="white", justify="left", font=("Georgia", 16))
        info_text.place(x=20.0, y=200.0)

    def load_images(self):
        self.defaultView = tk.PhotoImage(file=ASSETS_PATH / const.defaultView)
        self.canvas.create_image(930, 250, image=self.defaultView)

        self.point_image = tk.PhotoImage(file=ASSETS_PATH / const.points)
        self.canvas.create_image(1450, 200, image=self.point_image)

        self.wave_image = tk.PhotoImage(file=ASSETS_PATH / const.multipoints)
        self.canvas.create_image(1450, 650, image=self.wave_image)

    def start_camera(self):
        if not self.isCameraActive:
            self.progressbar.place(x=700, y=575, width=400, height=30)
            self.progressbar.start()
            self.camera_thread = threading.Thread(target=self.initialize_camera)
            self.camera_thread.start()
            self.generate_btn.place_forget()

    def initialize_camera(self):
        from gui.camera import Camera
        self.cap = cv2.VideoCapture(0)

        if self.cap.isOpened():
            self.progressbar.stop()
            self.progressbar.place_forget()
            create_button(self, const.startCamera)
            create_button(self, const.stopCamera)
            self.isCameraActive = True
            Camera(self.cap, self.label_camera_preview, self.isCameraActive, self.model, self.font)
        else:
            self.progressbar.stop()
            self.progressbar.place_forget()
            print("Failed to open the camera.")

    def stop_camera(self):
        if self.isCameraActive:
            self.isCameraActive = False
            self.cap.release()
            cv2.destroyAllWindows()

            if self.stop_btn:
                self.stop_btn.config(state="disabled")

                default_image = Image.open(ASSETS_PATH / "logo1.png")
                default_photo = ImageTk.PhotoImage(default_image)
                self.label_camera_preview.configure(image=default_photo)
                self.label_camera_preview.image = default_photo

            create_button(self, const.generate)

# code for loading model and amharic fonts
    def load_model(self):
        self.model = tf.keras.models.load_model('Greeting8c.h5')
        self.font = ImageFont.truetype('assets/font/AbyssinicaSIL-Regular.ttf', 32)
