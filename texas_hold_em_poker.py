import sys
sys.path.append('f:/Texas-Hold-em-poker/python_files')

from flask import Flask, render_template, request, jsonify
try:
    from game import Game
    from deck import Card
    print("Importazione riuscita!")
except ImportError as e:
    print(f"Errore di importazione: {e}")

app = Flask(__name__, static_url_path="")
game = Game()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("game.html")

    if request.method == "POST":
        action = request.form.get("action")
        if isinstance(action, str):
            game.execute_player_turn(action)
            if game.can_execute_turn("opponent"):
                game.execute_opponent_turn()

        player_hand = [{'value': card.value, 'suit': card.suit} for card in game.player.cards]
        dealer_hand = [{'value': card.value, 'suit': card.suit} for card in game.opponent.cards]
        community_cards = [{'value': card.value, 'suit': card.suit} for card in game.community_cards]
        deck_card = {'value': 'back', 'suit': 'card_back'}
        winner = game.get_winner()

        return jsonify({
            'player_hand': player_hand,
            'dealer_hand': dealer_hand,
            'community_cards': community_cards,
            'deck_card': deck_card,
            'enemy_cards_count': len(game.opponent.cards),
            'last_played_card': game.get_last_played_card(),
            'player_cards_count': len(game.player.cards),
            'can_draw': True,
            'can_play': any(game.can_card_be_played(card) for card in game.player.cards),
            'can_pass': True,
            'winner': winner
        })

if __name__ == "__main__":
    app.run(debug=True, port=5000)