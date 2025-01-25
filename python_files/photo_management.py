from PIL import Image
import os
import time

def crop_image(image_path, output_path):
    try:
        # Carica l'immagine
        img = Image.open(image_path)
        print(f"Caricata immagine: {image_path}")
        
        # Rimuove i bordi vuoti
        bbox = img.getbbox()
        if bbox:
            img_cropped = img.crop(bbox)
            print(f"Ritagliato immagine: {bbox}")
        else:
            img_cropped = img
            print(f"Nessun bordo vuoto trovato: {image_path}")
        
        # Salva l'immagine ritagliata
        img_cropped.save(output_path)
        print(f"Immagine salvata: {output_path}")
    except Exception as e:
        print(f"Errore durante il ritaglio di {image_path}: {e}")

def crop_images_in_folder(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    for root, dirs, files in os.walk(input_folder):
        for file in files:
            if file.endswith(".png") or file.endswith(".jpg"):
                input_path = os.path.join(root, file)
                relative_path = os.path.relpath(input_path, input_folder)
                output_path = os.path.join(output_folder, relative_path)
                
                output_dir = os.path.dirname(output_path)
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)
                
                crop_image(input_path, output_path)
                print(f"Cropped: {relative_path}")
                
                # Introduce una pausa di 0,5 secondi tra ogni operazione di ritaglio
                time.sleep(0.5)

# Esegui il programma con i percorsi di input e output
input_folder = "f:/Texas-Hold-em-poker/static/card_images"
output_folder = "f:/Texas-Hold-em-poker/static/card_images_cropped"

crop_images_in_folder(input_folder, output_folder)