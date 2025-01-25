import tkinter as tk
from pathlib import Path

import constants as const

ASSETS_PATH = Path(__file__).resolve().parent.parent / "assets" / "Image"

def create_button(translator, image):
    translator.generate_btn_img = tk.PhotoImage(file=ASSETS_PATH / image)
    if image == const.generate:
        translator.generate_btn = tk.Button(
            image=translator.generate_btn_img, borderwidth=0, highlightthickness=0,
            command=translator.start_camera, relief="flat")
        translator.generate_btn.place(x=800, y=510, width=180, height=55)

    elif image == const.stopCamera:
        translator.stop_btn = tk.Button(
            image=translator.generate_btn_img, borderwidth=0, highlightthickness=0,
            command=translator.stop_camera, relief="flat")
        translator.stop_btn.place(x=800, y=500, width=180, height=55)

def configure_style(style):
    style.theme_use('clam')
    style.configure("TProgressbar", background="#3A7FF6", troughcolor="#FCFCFC", bordercolor="#3A7FF6",
                    lightcolor="#3A7FF6", darkcolor="#3A7FF6", relief="flat", troughrelief="flat",
                    borderwidth=0, lightthickness=0, darkthickness=0, thickness=10, borderRadius=20)
