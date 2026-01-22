import pyautogui
import os
import time
import pyperclip
from datetime import datetime, timedelta
import sys

pyautogui.FAILSAFE = True

# --- Opsætning ---
script_dir = os.path.dirname(os.path.abspath(__file__))
start_img = os.path.join(script_dir, 'start.png')
copy_img = os.path.join(script_dir, 'copy.png')
delete_img = os.path.join(script_dir, 'delete.png')
paste_img = os.path.join(script_dir, 'paste.png')

if not all(os.path.exists(p) for p in [start_img, copy_img, delete_img, paste_img]):
    print("Mangler billeder.")
    sys.exit()

# 1. FIND OG KOPIER
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

# VIGTIGT: Vent længe nok til at GUI'en er HELT færdig med at kopiere
print("Venter på at GUI slipper clipboardet...")
time.sleep(2.0) 

# 2. BEREGN
try:
    original_str = pyperclip.paste().strip()
    dt = datetime.strptime(original_str, "%H.%M")
    utc_dt = dt - timedelta(hours=1)
    target_value = utc_dt.strftime("%H.%M")
    print(f"Mål-værdi: {target_value}")
    
except ValueError:
    print(f"Kunne ikke læse tid: {original_str}")
    sys.exit()

# 3. TVING VÆRDIEN IND (WATCHDOG)
# Vi bliver her, indtil clipboardet faktisk indeholder det rigtige
max_retries = 10
success = False

for i in range(max_retries):
    pyperclip.copy(target_value)
    time.sleep(0.5) # Vent lidt
    
    current_clipboard = pyperclip.paste().strip()
    
    if current_clipboard == target_value:
        print(f"Succes! Clipboard indeholder nu: {current_clipboard}")
        success = True
        break
    else:
        print(f"Forsøg {i+1}: Clipboard har stadig '{current_clipboard}'. Prøver igen...")

if not success:
    print("FEJL: Kunne ikke tvinge værdien ind i clipboardet. Stopper.")
    sys.exit()

# 4. SLET GAMMELT INDHOLD
pyautogui.rightClick(start_loc)
time.sleep(0.8)

delete_loc = pyautogui.locateCenterOnScreen(delete_img, confidence=0.9, grayscale=True)
if delete_loc:
    pyautogui.click(delete_loc)
    time.sleep(0.5)
else:
    print("Delete-knap ikke fundet (fortsætter alligevel).")

# 5. SÆT IND
# Tjekker lige clipboard en SIDSTE gang før vi paster
if pyperclip.paste().strip() != target_value:
    print("ADVARSEL: Clipboard ændrede sig i sidste øjeblik! Retter det...")
    pyperclip.copy(target_value)
    time.sleep(0.2)

pyautogui.rightClick(start_loc)
time.sleep(0.8)

paste_loc = pyautogui.locateCenterOnScreen(paste_img, confidence=0.9, grayscale=True)
if paste_loc:
    pyautogui.click(paste_loc)
    print("Færdig.")
else:
    print("Paste-knap ikke fundet.")
