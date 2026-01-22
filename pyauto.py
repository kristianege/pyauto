import pyautogui
import os
import time

# Sikkerhed
pyautogui.FAILSAFE = True

# Find sti til billedet (samme mappe som scriptet)
script_dir = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(script_dir, 'gui_element.png')

if os.path.exists(image_path):
    # Find billedet
    location = pyautogui.locateCenterOnScreen(image_path, confidence=0.9)

    if location:
        # Udfør dobbeltklik
        pyautogui.click(location, clicks=2)
        print("Fundet og dobbeltklikket.")
    else:
        print("Billede ikke fundet på skærmen.")
else:
    print(f"Filen mangler: {image_path}")
