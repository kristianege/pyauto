import pyautogui
import os
import time
import pyperclip
from datetime import datetime, timedelta
import sys

# Sikkerhed
pyautogui.FAILSAFE = True

# Stier til billeder
script_dir = os.path.dirname(os.path.abspath(__file__))
start_img = os.path.join(script_dir, 'start.png')
copy_img = os.path.join(script_dir, 'copy.png')
paste_img = os.path.join(script_dir, 'paste.png')

# Tjek at billederne findes
if not all(os.path.exists(p) for p in [start_img, copy_img, paste_img]):
    print("Mangler start.png, copy.png eller paste.png")
    sys.exit()

# --- Del 1: Kopier ---
start_loc = pyautogui.locateCenterOnScreen(start_img, confidence=0.9)
if not start_loc:
    print("Fandt ikke start.png")
    sys.exit()

pyautogui.rightClick(start_loc)
time.sleep(1.0) # Vent på menu

# Bruger grayscale=True da det ofte er bedre til tekst i menuer
copy_loc = pyautogui.locateCenterOnScreen(copy_img, confidence=0.9, grayscale=True)
if not copy_loc:
    print("Fandt ikke copy.png i menuen")
    sys.exit()

pyautogui.click(copy_loc)
time.sleep(0.5) # Vent på clipboard

# --- Del 2: Omregn tid ---
try:
    original_str = pyperclip.paste().strip()
    dt = datetime.strptime(original_str, "%H.%M")
    utc_dt = dt - timedelta(hours=1)
    new_str = utc_dt.strftime("%H.%M")
    pyperclip.copy(new_str)
    print(f"Omregnet {original_str} til {new_str}")
except ValueError:
    print(f"Kunne ikke forstå tidsformatet: {original_str}")
    sys.exit()

# --- Del 3: Sæt ind ---
# Finder start-lokationen igen for en sikkerheds skyld
start_loc = pyautogui.locateCenterOnScreen(start_img, confidence=0.9)
if not start_loc:
     print("Kunne ikke finde start.png igen")
     sys.exit()

pyautogui.rightClick(start_loc)
time.sleep(1.0) # Vent på menu

paste_loc = pyautogui.locateCenterOnScreen(paste_img, confidence=0.9, grayscale=True)
if not paste_loc:
    print("Fandt ikke paste.png i menuen")
    sys.exit()

pyautogui.click(paste_loc)
print("Færdig.")
