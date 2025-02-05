import sys
import os
import time
from termcolor import colored

sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

from game import Game, Bot, Player, Dealer, BettingRound

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
    game = Game(num_players=4)
    game.setup_players()

    # Messaggio che indica l'inizio del gioco
    print(colored("\n===== Inizio del Gioco =====\n", 'green'))

    while True:
        while game.phase != Game.SHOWDOWN:
            current_player = game.turn_manager.get_current_player()
            phase = game.phase.replace('_', '-').lower()  # Converte la fase attuale in un formato utilizzabile
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
                game.turn_manager.next_turn()
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
                if action in ['bet', 'raise', 'call']:
                    bet_amount = int(input("Inserisci la quantità di chip da scommettere: "))
                print(colored(f"Azione del Giocatore: {action}", 'green'))
                game.execute_turn(current_player, action, bet_amount)
                game.turn_manager.next_turn()
                game.check_phase_end()
                time.sleep(2)  # Pausa di 2 secondi tra i turni

        # Messaggio che annuncia il vincitore alla fine del gioco
        final_state = game.generate_game_state_response()
        print(colored("\n===== Stato Finale del Gioco =====", 'green'))
        print(final_state)
        print(colored(f"\n===== Vincitore: {final_state['winner']} =====", 'green'))

        # Chiediere all'utente se vuole ricominciare la partita
        restart = input("Vuoi ricominciare la partita? (sì/no): ").lower()
        if restart == 'sì':
            game = Game(num_players=4)
            game.setup_players()
            print(colored("\n===== Ricomincia una Nuova Partita =====\n", 'green'))
        else:
            break

if __name__ == "__main__":
    test_game()