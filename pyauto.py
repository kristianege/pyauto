import pyautogui
import os
import time
import pyperclip
from datetime import datetime, timedelta
import sys

# Sikkerhed
pyautogui.FAILSAFE = True

# Stier
script_dir = os.path.dirname(os.path.abspath(__file__))
start_img = os.path.join(script_dir, 'start.png')
copy_img = os.path.join(script_dir, 'copy.png')

# Tjek filer
if not os.path.exists(start_img) or not os.path.exists(copy_img):
    print("Mangler start.png eller copy.png")
    sys.exit()

# --- Del 1: Hent data ---
start_loc = pyautogui.locateCenterOnScreen(start_img, confidence=0.9)
if not start_loc:
    print("Fandt ikke start.png")
    sys.exit()

# Højreklik på feltet
pyautogui.rightClick(start_loc)
time.sleep(0.8) # Vent på menu

# Find og klik kopier
copy_loc = pyautogui.locateCenterOnScreen(copy_img, confidence=0.9, grayscale=True)
if not copy_loc:
    print("Fandt ikke copy.png i menuen")
    sys.exit()

pyautogui.click(copy_loc)
time.sleep(0.5) # Vigtigt: Vent mens menuen lukker og clipboard opdateres

# --- Del 2: Beregn ---
try:
    original_str = pyperclip.paste().strip()
    dt = datetime.strptime(original_str, "%H.%M")
    utc_dt = dt - timedelta(hours=1)
    new_str = utc_dt.strftime("%H.%M")
    print(f"Omregnet: {original_str} -> {new_str}")
except ValueError:
    print(f"Formatfejl i tid: {original_str}")
    sys.exit()

# --- Del 3: Skriv ny værdi ---
# Skriver direkte, da feltet antages at have fokus efter menuen lukker
pyautogui.write(new_str)
print("Ny tid indtastet.")
