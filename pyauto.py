import pyautogui
import os
import time
import pyperclip
from datetime import datetime, timedelta
import sys
import tkinter # Vi bruger denne til at tvinge clipboardet

pyautogui.FAILSAFE = True

# Stier til billeder
script_dir = os.path.dirname(os.path.abspath(__file__))
start_img = os.path.join(script_dir, 'start.png')
copy_img = os.path.join(script_dir, 'copy.png')
paste_img = os.path.join(script_dir, 'paste.png')

if not all(os.path.exists(p) for p in [start_img, copy_img, paste_img]):
    print("Mangler billedfiler.")
    sys.exit()

# --- Del 1: Kopier ---
print("Finder start...")
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

# --- Del 2: Beregn og TVING ny værdi ind ---
try:
    original_str = pyperclip.paste().strip()
    dt = datetime.strptime(original_str, "%H.%M")
    utc_dt = dt - timedelta(hours=1)
    new_str = utc_dt.strftime("%H.%M")
    
    print(f"Beregnet værdi: {new_str}")

    # HER ER FIXET:
    # Vi bruger tkinter til at rydde og sætte clipboardet, da det er mere robust
    r = tkinter.Tk()
    r.withdraw()        # Skjul det lille vindue der ellers kommer
    r.clipboard_clear() # Tøm clipboard helt
    r.clipboard_append(new_str) # Sæt den nye værdi
    r.update()          # Tving systemet til at opdatere
    r.destroy()         # Luk tkinter ned igen
    
    print("Clipboard er tvangs-opdateret.")
    
except ValueError:
    print(f"Fejl i tidsformat: {original_str}")
    sys.exit()

# --- Del 3: Sæt ind med musen ---
pyautogui.rightClick(start_loc)
time.sleep(0.8) 

paste_loc = pyautogui.locateCenterOnScreen(paste_img, confidence=0.9, grayscale=True)
if paste_loc:
    pyautogui.click(paste_loc)
    print("Indsat korrekt.")
else:
    print("Kunne ikke finde 'Sæt ind'.")
