import pygame
import time
import os

# Inizializza il mixer di pygame
pygame.mixer.init()

# Lista dei file musicali
playlist = [
    'E:Texas-Hold-em-poker/static/music/best_jazz_club_NO.mp3',
    'E:Texas-Hold-em-poker/static/music/casino.mp3',
    'E:Texas-Hold-em-poker/static/music/jazz_casino_bar.mp3',
    'E:Texas-Hold-em-poker/static/music/jazz_whiskey_casino.mp3',
    'E:Texas-Hold-em-poker/static/music/two_cigarettes_please.mp3',
    'E:Texas-Hold-em-poker/static/music/welcome_to_new_orleans.mp3'
]

# Verifica che i file esistano
playlist = [song for song in playlist if os.path.exists(song)]

if not playlist:
    print("Nessun file musicale trovato!")
else:
    try:
        for song in playlist:
            pygame.mixer.music.load(song)
            pygame.mixer.music.play()
            print(f"Riproduzione in corso: {song}")
            while pygame.mixer.music.get_busy():
                time.sleep(1)  # Aspetta finché la musica è in riproduzione
    except pygame.error as e:
        print(f"Errore nel caricamento o riproduzione del file: {e}")

# Controlla se sei in un ambiente SSH
if 'SSH_CLIENT' in os.environ or 'SSH_TTY' in os.environ:
    print("Attenzione: La riproduzione audio potrebbe non funzionare correttamente via SSH.")
    print("Considera di usare 'mpg123' o 'vlc' per la riproduzione remota.")