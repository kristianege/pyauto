import pyautogui
import os
import time
import pyperclip
from datetime import datetime, timedelta
import sys

pyautogui.FAILSAFE = True

# --- Konfiguration ---
script_dir = os.path.dirname(os.path.abspath(__file__))
start_img = os.path.join(script_dir, 'start.png')
copy_img = os.path.join(script_dir, 'copy.png')
delete_img = os.path.join(script_dir, 'delete.png')
paste_img = os.path.join(script_dir, 'paste.png')

# Tjek filer
if not all(os.path.exists(p) for p in [start_img, copy_img, delete_img, paste_img]):
    print("Mangler en billedfil: Tjek start, copy, delete og paste.")
    sys.exit()

# --- 1. Hent værdi (Copy) ---
start_loc = pyautogui.locateCenterOnScreen(start_img, confidence=0.9)
if not start_loc:
    print("Start ikke fundet.")
    sys.exit()

pyautogui.rightClick(start_loc)
time.sleep(0.8)

copy_loc = pyautogui.locateCenterOnScreen(copy_img, confidence=0.9, grayscale=True)
if not copy_loc:
    print("Copy ikke fundet.")
    sys.exit()

pyautogui.click(copy_loc)
time.sleep(0.5)

# --- 2. Beregn ny tid ---
try:
    original_str = pyperclip.paste().strip()
    dt = datetime.strptime(original_str, "%H.%M")
    utc_dt = dt - timedelta(hours=1)
    new_str = utc_dt.strftime("%H.%M")
    
    # Opdater clipboard
    pyperclip.copy(new_str)
    print(f"Beregnet: {new_str}")
    time.sleep(0.5) # Sikrer at clipboardet er klar
    
except ValueError:
    print(f"Kunne ikke læse tid: {original_str}")
    sys.exit()

# --- 3. Tøm feltet (Delete) ---
# Vi finder start igen
pyautogui.rightClick(start_loc)
time.sleep(0.8)

delete_loc = pyautogui.locateCenterOnScreen(delete_img, confidence=0.9, grayscale=True)
if delete_loc:
    pyautogui.click(delete_loc)
    print("Felt slettet.")
    time.sleep(0.5) # Vent på at feltet bliver tomt
else:
    print("Delete-knap ikke fundet.")
    sys.exit()

# --- 4. Sæt ind (Paste) ---
# Vi finder start en sidste gang (nu bør feltet være tomt)
pyautogui.rightClick(start_loc)
time.sleep(0.8)

paste_loc = pyautogui.locateCenterOnScreen(paste_img, confidence=0.9, grayscale=True)
if paste_loc:
    pyautogui.click(paste_loc)
    print("Ny værdi indsat.")
else:
    print("Paste-knap ikke fundet.")
