"""
Questo file contiene uno script per testare il funzionamento del gioco di Texas Hold'em Poker.
L'obiettivo è simulare una partita completa con bot e giocatori umani, gestendo le varie fasi del gioco e le azioni dei giocatori.

Funzionalità testate:
- Inizializzazione del gioco e distribuzione delle carte.
- Gestione delle fasi del gioco (pre-flop, flop, turn, river, showdown).
- Esecuzione delle azioni dei giocatori (check, call, bet, raise, fold).
- Visualizzazione delle informazioni di gioco (carte dei giocatori, carte comuni, piatto).

Il gioco prosegue fino al raggiungimento del numero massimo di turni o fino alla fase di showdown.
L'interfaccia utente è basata su testo e utilizza il modulo `termcolor` per colorare le informazioni mostrate.
"""

import sys
import os
import time
from termcolor import colored

# Percorso principale del progetto
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from python_files.game import Game, Bot, Player, Dealer, BettingRound

# Colori per i giocatori e le fasi di gioco
player_colors = {
    'small_blind': 'red',
    'big_blind': 'blue',
    'player': 'green',
    'Bot1': 'yellow',
    'Bot2': 'cyan',
    'Bot3': 'magenta'
}

phase_colors = {
    'pre-flop': 'yellow',
    'flop': 'cyan',
    'turn': 'magenta',
    'river': 'blue',
    'showdown': 'red'
}

def display_action_menu():
    print(colored("\n===== Menù delle Azioni =====", 'green'))
    print(colored("check - Controlla senza scommettere", 'green'))
    print(colored("call - Chiedi per pareggiare la scommessa corrente", 'green'))
    print(colored("bet - Scommetti una quantità di chip", 'green'))
    print(colored("raise - Rilancia aumentando la scommessa corrente", 'green'))
    print(colored("fold - Passa e abbandona la mano", 'green'))
    print(colored("=" * 30, 'green'))

def display_player_hand(player):
    print(colored("\nLe tue carte:", player_colors.get(player.name, 'white')))
    for card in player.cards:
        print(f"{card.value} di {card.suit}")

def display_community_cards(game):
    if game.community_cards:
        print(colored("\n===== Carte Comuni sul Tavolo =====", 'green'))
        for card in game.community_cards:
            print(f"{card.value} di {card.suit}")
        print(colored("=" * 30, 'green'))
    else:
        print(colored("\n===== Carte Comuni sul Tavolo =====", 'green'))
        print("Non ci sono ancora carte comuni sul tavolo.")
        print(colored("=" * 30, 'green'))

def display_pot(game):
    print(colored(f"\nPiatto corrente: {game.pot} fiches", 'green'))

def test_game():
    game = Game()
    game.setup_players()

    print(colored("\n===== Inizio del Gioco =====\n", 'green'))
    
    max_turns = 100  # Limite massimo ai turni
    turn_count = 0

    while True:
        while game.phase != Game.SHOWDOWN and turn_count < max_turns:
            current_player = game.turn_manager.get_current_player()
            phase = game.phase.replace('_', '-').lower()
            print(colored("\n" + "=" * 30, phase_colors.get(phase, 'white')))
            print(colored(f"Turno del Giocatore: {current_player.name}", player_colors.get(current_player.name, 'white')))
            print(colored(f"Fase attuale: {game.phase}", phase_colors.get(phase, 'white')))
            print(colored(f"Piatto corrente: {game.pot}", 'green'))
            print(colored(f"Scommessa corrente: {game.current_bet}", 'green'))
            print(colored("=" * 30, phase_colors.get(phase, 'white')))

            if isinstance(current_player, Bot):
                action, bet_amount = current_player.make_decision(game.generate_game_state_response(), game.phase)
                print(colored(f"Azione del Bot: {action}, bet amount: {bet_amount}", 'cyan'))
                game.execute_turn(current_player, action, bet_amount)
            else:
                display_action_menu()
                display_player_hand(current_player)
                display_community_cards(game)
                display_pot(game)

                valid_action = False
                while not valid_action:
                    action = input(f"{current_player.name}, scegli la tua azione: ").lower()
                    if action not in ['check', 'call', 'bet', 'raise', 'fold']:
                        print(colored("Azione non valida. Per favore, scegli un'azione valida.", 'red'))
                    elif game.current_bet > 0 and action == 'check':
                        print(colored("Non puoi fare check quando c'è una scommessa in corso. Scegli un'altra azione.", 'red'))
                    else:
                        valid_action = True

                bet_amount = 0
                if action in ['bet', 'raise']:
                    bet_amount = int(input("Inserisci la quantità di chip da scommettere: "))
                elif action == 'call':
                    bet_amount = game.current_bet  # Pareggia la scommessa corrente

                print(colored(f"Azione del Giocatore: {action}", 'green'))
                game.execute_turn(current_player, action, bet_amount)
                
            if game.phase == Game.SHOWDOWN:  # Controlla se il gioco è finito
                break

            game.turn_manager.next_turn()  # Avanza al turno successivo
            time.sleep(2)

            turn_count += 1

        if turn_count >= max_turns:
            print(colored("\n===== Raggiunto il limite massimo dei turni =====", 'red'))
            break

        final_state = game.generate_game_state_response()
        print(colored("\n===== Stato Finale del Gioco =====", 'green'))
        print(final_state)
        print(colored(f"\n===== Vincitore: {final_state['winner']} =====", 'green'))

        restart = input("Vuoi ricominciare la partita? (sì/no): ").lower()
        if restart == 'sì':
            game = Game()
            game.setup_players()
            print(colored("\n===== Ricomincia una Nuova Partita =====\n", 'green'))
            turn_count = 0
        else:
            break

if __name__ == "__main__":
    test_game()

#da controllare perchè va in errore
#trovare una soluzione al problema di questo file
#testarlo dal terminale