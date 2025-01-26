import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), 'python_files'))

from flask import Flask, render_template, request, jsonify
from python_files.game import Game

app = Flask(__name__, static_url_path="/static")
game = Game()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("game.html")

    if request.method == "POST":
        action = request.form.get("action")
        bet_amount = int(request.form.get("betAmount", 0))
        
        if action in ['check', 'call', 'bet', 'raise']:
            result = game.execute_player_turn(action, bet_amount)
            if result == 'opponent wins':
                return jsonify({'winner': 'opponent', 'phase': game.phase})
        
        player_hand = [{'value': card.value, 'suit': card.suit} for card in game.player.cards]
        dealer_hand = [{'value': card.value, 'suit': card.suit} for card in game.opponent.cards]
        community_cards = [{'value': card.value, 'suit': card.suit} for card in game.community_cards]
        deck_card = {'value': 'back', 'suit': 'card_back'}
        winner = game.get_winner() if game.phase == 'showdown' else None

        return jsonify({
            'player_hand': player_hand,
            'dealer_hand': dealer_hand,
            'community_cards': community_cards,
            'deck_card': deck_card,
            'winner': winner,
            'phase': game.phase
        })

@app.route("/start-game", methods=["POST"])
def start_game():
    global game
    game = Game()  # Inizializza una nuova partita
    game.setup_players()  # Inizializza le carte dei giocatori e del mazzo
    player_hand = [{'value': card.value, 'suit': card.suit} for card in game.player.cards]
    dealer_hand = [{'value': card.value, 'suit': card.suit} for card in game.opponent.cards]
    community_cards = [{'value': card.value, 'suit': card.suit} for card in game.community_cards]
    deck_card = {'value': 'back', 'suit': 'card_back'}

    return jsonify({
        'player_hand': player_hand,
        'dealer_hand': dealer_hand,
        'community_cards': community_cards,
        'deck_card': deck_card,
        'winner': None
    })

@app.route("/new-game", methods=["POST"])
def new_game():
    global game
    game = Game()  # Crea una nuova istanza del gioco per riavviare la partita
    game.setup_players()  # Inizializza le carte dei giocatori e del mazzo
    player_hand = [{'value': card.value, 'suit': card.suit} for card in game.player.cards]
    dealer_hand = [{'value': card.value, 'suit': card.suit} for card in game.opponent.cards]
    community_cards = [{'value': card.value, 'suit': card.suit} for card in game.community_cards]
    deck_card = {'value': 'back', 'suit': 'card_back'}

    return jsonify({
        'player_hand': player_hand,
        'dealer_hand': dealer_hand,
        'community_cards': community_cards,
        'deck_card': deck_card,
        'winner': None
    })

@app.route("/home_poker", methods=["GET"])
def home_poker():
    return render_template("home_poker.html")

#TODO:
#creare delle route per le altre pagine: home_poker e poker_rules
#gestire i casi in cui il giocatore vince o perde per aggiornare le fiches
#gestire il caso in cui il giocatore non ha più soldi o fiches
#gestire il caso in cui il giocatore si arrende
#migliorare la parte di scommessa delle fiches tramite il menu dove sono presenti i pulsanti per le azioni
#gestire gli errori per quando si premono i pulsanti senza aver premuto prima il pulsante di start game perchè compare il messaggio delle fasi del gioco anche quando si clicca su start game
#aggiungere la possibilità di giocare con più giocatori
#se si realizza la possibilità di giocare con più giocatori, aggiungere la possibilità di scegliere il numero di giocatori e di creare i turni di gioco
#creare una tabella per l'utente per vedere il quantitativo di fiches durante la partita per aggiornarla dinamicamente

if __name__ == "__main__":
    app.run(debug=True, port=5000)