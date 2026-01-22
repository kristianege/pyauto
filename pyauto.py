import pyautogui
import os
import time
import pyperclip
from datetime import datetime, timedelta
import sys
import ctypes
from ctypes import wintypes

pyautogui.FAILSAFE = True

# --- Opsætning af Windows System-kald (Hardcore clipboard adgang) ---
user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

def force_text_to_clipboard(text):
    """
    Denne funktion tømmer udklipsholderen HELT og indsætter KUN ren tekst.
    Dette fjerner alle 'smarte' formateringer fra applikationen.
    """
    # 1. Konverter streng til bytes (Windows kræver null-termineret C-streng)
    data = text.encode('utf-8')
    
    # 2. Åbn clipboard og TØM det (fjerner applikationens ejerskab)
    user32.OpenClipboard(None)
    user32.EmptyClipboard()
    
    # 3. Alloker hukommelse i Windows
    hCd = kernel32.GlobalAlloc(0x0002, len(data) + 1) # GMEM_MOVEABLE
    pchData = kernel32.GlobalLock(hCd)
    
    # 4. Kopier vores tekst ind i hukommelsen
    ctypes.memmove(pchData, data, len(data))
    kernel32.GlobalUnlock(hCd)
    
    # 5. Sæt clipboard data til typen CF_TEXT (1)
    user32.SetClipboardData(1, hCd)
    user32.CloseClipboard()

# --- Script Start ---

script_dir = os.path.dirname(os.path.abspath(__file__))
start_img = os.path.join(script_dir, 'start.png')
copy_img = os.path.join(script_dir, 'copy.png')
paste_img = os.path.join(script_dir, 'paste.png')

if not all(os.path.exists(p) for p in [start_img, copy_img, paste_img]):
    print("Mangler billedfiler.")
    sys.exit()

# 1. FIND OG KOPIER
print("Finder celle...")
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

# 2. BEREGN OG "NUKE" CLIPBOARD
try:
    original_str = pyperclip.paste().strip()
    print(f"Original værdi: {original_str}")
    
    dt = datetime.strptime(original_str, "%H.%M")
    utc_dt = dt - timedelta(hours=1)
    new_str = utc_dt.strftime("%H.%M")
    
    print(f"Ny værdi: {new_str}")

    # Her bruger vi den hårde metode
    force_text_to_clipboard(new_str)
    print("Clipboard er tvangs-opdateret med ren tekst.")
    
except ValueError:
    print(f"Formatfejl. Kunne ikke læse: {original_str}")
    sys.exit()

# 3. SÆT IND (Kun mus)
# Vi finder start-stedet igen for at være sikre
start_loc = pyautogui.locateCenterOnScreen(start_img, confidence=0.9)
pyautogui.rightClick(start_loc)
time.sleep(0.8) 

paste_loc = pyautogui.locateCenterOnScreen(paste_img, confidence=0.9, grayscale=True)
if paste_loc:
    pyautogui.click(paste_loc)
    print("Klikket på 'Sæt ind'.")
else:
    print("Paste knap ikke fundet.")
