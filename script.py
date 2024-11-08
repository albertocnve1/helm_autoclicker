import pyautogui
import cv2
import numpy as np
import time
from PIL import ImageGrab
import sys

# Percorso dell'immagine di riferimento
image_path = '/Users/albertocanavese/Desktop/helm_autoclicker/target.png'

# Prova a caricare l'immagine di riferimento
template = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

# Verifica che l'immagine sia stata caricata correttamente
if template is None:
    print(f"Errore: Impossibile aprire il file '{image_path}'. Verifica il percorso e l'integrità del file.")
    sys.exit(1)

# Ottieni le dimensioni dell'immagine di riferimento
w, h = template.shape[::-1]

# Fattore di scala per schermi Retina (imposta a 1 se non è Retina)
scale_factor = 2  # Cambia questo valore a seconda del tuo schermo

def find_and_click():
    while True:
        # Cattura uno screenshot dell'intero schermo
        screenshot = ImageGrab.grab()
        screenshot_np = np.array(screenshot)
        screen_gray = cv2.cvtColor(screenshot_np, cv2.COLOR_BGR2GRAY)

        # Esegui il match template per cercare l'immagine target nello screenshot
        res = cv2.matchTemplate(screen_gray, template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.9  # Soglia per determinare una corrispondenza valida
        loc = np.where(res >= threshold)

        # Se viene trovata una corrispondenza
        if len(loc[0]) > 0:
            y, x = loc[0][0], loc[1][0]
            
            # Calcola le coordinate del centro dell'immagine di riferimento
            center_x, center_y = x + w // 2, y + h // 2
            
            # Applica il fattore di scala
            adjusted_x, adjusted_y = int(center_x / scale_factor), int(center_y / scale_factor)
            
            # Esegui il clic con pyautogui al centro del bersaglio
            pyautogui.moveTo(adjusted_x, adjusted_y)  # Sposta il puntatore al bersaglio
            pyautogui.click()  # Esegue il clic
            print(f"Clic eseguito al punto ({adjusted_x}, {adjusted_y})")

# Esegui la funzione
find_and_click()
