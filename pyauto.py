import pyautogui
import os
import time
import pyperclip
from datetime import datetime, timedelta
import sys
import subprocess # Vi bruger denne til at tale direkte med Windows

pyautogui.FAILSAFE = True

# Stier
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
time.sleep(1.0) # Vi giver den lige lidt ekstra tid her

# --- Del 2: Beregn og TVING med PowerShell ---
try:
    original_str = pyperclip.paste().strip()
    print(f"Læste fra clipboard: {original_str}")
    
    dt = datetime.strptime(original_str, "%H.%M")
    utc_dt = dt - timedelta(hours=1)
    new_str = utc_dt.strftime("%H.%M")
    
    print(f"Vil indsætte ny værdi: {new_str}")

    # HER ER MAGIEN:
    # Vi beder Windows PowerShell om at sætte clipboardet. 
    # Dette kører på system-niveau og ignorerer python-bibliotekernes begrænsninger.
    cmd = f'powershell Set-Clipboard -Value "{new_str}"'
    subprocess.run(cmd, shell=True)
    
    # Vent kort for at sikre at Windows har fanget beskeden
    time.sleep(1.0)
    
    # DEBUG-TJEK: Vi læser clipboardet igen for at se om det lykkedes
    check_val = pyperclip.paste().strip()
    if check_val == new_str:
        print("Succes: Clipboard er opdateret korrekt!")
    else:
        print(f"FEJL: Clipboard indeholder stadig {check_val}")

except ValueError:
    print(f"Kunne ikke læse tid (fik: '{original_str}')")
    sys.exit()

# --- Del 3: Sæt ind ---
pyautogui.rightClick(start_loc)
time.sleep(0.8) 

paste_loc = pyautogui.locateCenterOnScreen(paste_img, confidence=0.9, grayscale=True)
if paste_loc:
    pyautogui.click(paste_loc)
    print("Indsat.")
else:
    print("Kunne ikke finde 'Sæt ind'.")
