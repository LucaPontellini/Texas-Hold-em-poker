import sys
sys.path.append('f:/Texas-Hold-em-poker/python_files')  # Percorso corretto per il modulo

from flask import Flask, render_template, request, jsonify
from game import Game
from deck import Card

app = Flask(__name__, static_url_path="/static")
game = Game()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("game.html")

    if request.method == "POST":
        action = request.form.get("action")
        if isinstance(action, str):
            result = game.execute_player_turn(action)
            if result == 'opponent wins':
                return jsonify({'winner': 'opponent'})

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
            'winner': winner
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
    player_hand = []
    dealer_hand = []
    community_cards = []
    deck_card = {'value': 'back', 'suit': 'card_back'}

    return jsonify({
        'player_hand': player_hand,
        'dealer_hand': dealer_hand,
        'community_cards': community_cards,
        'deck_card': deck_card
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)