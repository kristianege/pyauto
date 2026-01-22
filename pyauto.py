import pyautogui
import time
import os

# Sikkerhedsindstilling: Træk musen til et hjørne for at dræbe scriptet
pyautogui.FAILSAFE = True 

# 1. Find stien til billedet dynamisk
# Dette sikrer, at IDLE kigger i den mappe, hvor du har gemt dette script
script_dir = os.path.dirname(os.path.abspath(__file__))
image_filename = 'gui_element.png'
full_image_path = os.path.join(script_dir, image_filename)

print(f"Leder efter: {full_image_path}")

# Tjek om billedfilen eksisterer
if not os.path.exists(full_image_path):
    print("FEJL: Billedfilen mangler. Sørg for at 'gui_element.png' ligger samme sted som scriptet.")
else:
    print("Scanner skærmen...")

    # Find midten af billedet
    # 'confidence=0.9' kræver at du har installeret opencv-python
    location = pyautogui.locateCenterOnScreen(full_image_path, confidence=0.9)

    if location is not None:
        print(f"Fundet ved: {location}")
        
        # 2. Sæt fokus
        # Vi klikker to gange for at sikre, at vinduet aktiveres
        pyautogui.click(location)
        time.sleep(0.1)
        pyautogui.click(location)
        
        # VIGTIGT: Vent 1 sekund så Windows når at skifte fokus til programmet
        print("Venter på at vinduet får fokus...")
        time.sleep(1.0)

        # 3. Udfør Tab-tryk langsomt
        print("Udfører 9 tab-tryk...")
        for i in range(1, 10):
            pyautogui.press('tab')
            print(f"Tab {i}")
            # Pause på 0.3 sekunder mellem hvert tryk
            time.sleep(0.3)
            
        print("Færdig.")
        
    else:
        print("Kunne ikke finde billedet. Prøv at tage et nyt screenshot på den korrekte skærm.")
