import pygame
import time

# Inizializza il mixer di pygame
pygame.mixer.init()

# Lista dei file musicali
playlist = [
    'F:\\Texas-Hold-em-poker\\static\\music\\best_jazz_club_NO.mp3',
    'F:\\Texas-Hold-em-poker\\static\\music\\casino.mp3',
    'F:\\Texas-Hold-em-poker\\static\\music\\jazz_casino_bar.mp3',
    'F:\\Texas-Hold-em-poker\\static\\music\\jazz_whiskey_casino.mp3',
    'F:\\Texas-Hold-em-poker\\static\\music\\two_cigarettes_please.mp3',
    'F:\\Texas-Hold-em-poker\\static\\music\\welcome_to_new_orleans.mp3'
]

while True:
    for song in playlist:
        pygame.mixer.music.load(song)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(1)  # Aspetta finché la musica è in riproduzione