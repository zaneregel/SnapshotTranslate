import tkinter as tk
import pyautogui
import html
import os

from PIL import Image, ImageGrab, ImageTk
from google.api_core.exceptions import AlreadyExists
from google.cloud import translate_v2 as translate
from google.cloud import vision

#takes screenshot with coordinates from text fields in GUI
def grab_screenshot():
    x1_val = x1.get()
    y1_val = y1.get()
    x2_val = x2.get()
    y2_val = y2.get()
    if x1_val == '' or y1_val == '' or x2_val == '' or y2_val == '':
        print("Enter Coordinate Fields")
    else:
        image_py = pyautogui.screenshot(region=(int(x1_val),int(y1_val),int(x2_val),int(y2_val)), allScreens=True)
        im = ImageTk.PhotoImage(image_py)
        image_py = image_py.save("screenshot.png")
        label.configure(image=im)
        label.image = im

#translates image from screenshot taken
def translate_screen():
        client = vision.ImageAnnotatorClient()
        with open("./screenshot.png", "rb") as image_file:
            content = image_file.read()
        image = vision.Image(content=content)
        response = client.text_detection(image=image)
        text = response.full_text_annotation.text
        translate_client = translate.Client()
        result = translate_client.translate(text, "en")
        translateBox.insert("1.0", result)

        

window = tk.Tk()
title = window.title("Image")
frame_button = tk.Frame()

#organize the UI so we have x1y1 on top of x2y2 on top of the screenshot
frame_top_point = tk.Frame(master=window)
frame_top_point.pack()
frame_bot_point = tk.Frame(master=window)
frame_bot_point.pack()
frame_button = tk.Frame(master=window)
frame_button.pack()
frame_bot = tk.Frame(master=window)
frame_bot.pack()


#layout of coordinate entry boxes for screenshot image
framex1 = tk.Frame(master=frame_top_point)
framey1 = tk.Frame(master=frame_top_point)
framex2 = tk.Frame(master=frame_bot_point)
framey2 = tk.Frame(master=frame_bot_point)

x1Label = tk.Label(master=framex1, text="x1")
x1Label.pack()
x1 = tk.Entry(master=framex1, width=25)
x1.pack()

framex1.pack(side=tk.LEFT)

y1Label = tk.Label(master= framey1, text="y1")
y1Label.pack()
y1 = tk.Entry(master=framey1, width=25)
y1.pack()

framey1.pack(side=tk.LEFT)

x2Label = tk.Label(master=framex2, text="x2")
x2Label.pack()
x2 = tk.Entry(master=framex2, width=25)
x2.pack()

framex2.pack(side=tk.LEFT)

y2Label = tk.Label(master=framey2, text="y2")
y2Label.pack()
y2 = tk.Entry(master=framey2, width=25)
y2.pack()

framey2.pack(side=tk.LEFT)

bboxCoord = tk.Button(master=frame_button, text="Screenshot", width=15, height=3, command=grab_screenshot)
bboxCoord.pack(side=tk.LEFT)
translateButton = tk.Button(master=frame_button, text="Translate", width=15, height=3, command=translate_screen)
translateButton.pack(side=tk.LEFT)

image_py = pyautogui.screenshot(region=(10,10,500,500))
im = ImageTk.PhotoImage(image_py)
label = tk.Label(master=frame_bot, image=im)
label.pack(side=tk.LEFT)

translateBox = tk.Text(master=frame_bot, width=175, height=50)
translateBox.pack(side=tk.LEFT)

window.mainloop()