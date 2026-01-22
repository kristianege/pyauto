import pyautogui
import os
import time
import pyperclip
from datetime import datetime, timedelta

# Sikkerhed
pyautogui.FAILSAFE = True

script_dir = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(script_dir, 'gui_element.png')

if os.path.exists(image_path):
    location = pyautogui.locateCenterOnScreen(image_path, confidence=0.9)

    if location:
        # 1. Højreklik og kopier ('c')
        pyautogui.rightClick(location)
        time.sleep(0.5)
        pyautogui.press('c')
        
        # Vent på at clipboard opdateres
        time.sleep(0.5)
        
        # 2. Hent, omregn og opdater værdi
        original_time_str = pyperclip.paste().strip()
        
        try:
            # Parse formatet hh.mm
            dt = datetime.strptime(original_time_str, "%H.%M")
            
            # Træk 1 time fra
            utc_dt = dt - timedelta(hours=1)
            
            # Formater tilbage til hh.mm og læg i clipboard
            new_time_str = utc_dt.strftime("%H.%M")
            pyperclip.copy(new_time_str)
            
            print(f"Ændret fra {original_time_str} til {new_time_str}")
            
            # 3. Højreklik igen og tast 'p'
            pyautogui.rightClick(location)
            time.sleep(0.5)
            pyautogui.press('p')
            print("Højreklikket og tastet 'p'.")
            
        except ValueError:
            print(f"Kunne ikke genkende tidsformatet: {original_time_str}")

    else:
        print("Billede ikke fundet.")
else:
    print(f"Filen mangler: {image_path}")
