import pyautogui
import time
import os

# Sikkerhed
pyautogui.FAILSAFE = True 

# 1. Konstruer den absolutte sti til billedet
# Dette sikrer, at scriptet leder i samme mappe, som .py filen ligger i
script_dir = os.path.dirname(os.path.abspath(__file__))
image_filename = 'gui_element.png'
full_image_path = os.path.join(script_dir, image_filename)

print(f"Leder efter billede på stien: {full_image_path}")

# Tjek om filen faktisk eksisterer, før vi beder pyautogui om at lede
if not os.path.exists(full_image_path):
    print("FEJL: Billedfilen blev ikke fundet på den angivne sti.")
else:
    print("Fil fundet. Scanner skærmen (dette kan tage et øjeblik)...")

    # Vi kører uden try/except for at se evt. fejlbeskeder direkte i IDLE
    location = pyautogui.locateCenterOnScreen(full_image_path, confidence=0.9)

    if location is not None:
        print(f"Billede fundet ved: {location}")
        
        pyautogui.click(location)
        time.sleep(0.5)

        for i in range(9):
            pyautogui.press('tab')
            time.sleep(0.1)
        
        print("Færdig med at trykke tab.")
    else:
        print("Kunne ikke finde billedet på skærmen. Tjek om det er synligt.")
