import sys
from flask import Flask, render_template, request, jsonify
sys.path.append('./Texas-Hold-em-poker/python_files')
from game import Game

app = Flask(__name__, static_url_path="")
game = Game()

@app.route("/", methods=["GET", "POST"])
def index():
    winner = game.get_winner()
    if winner:
        return render_template("game.html", winner=winner, game=game)

    if game.can_execute_turn("player"):
        if request.method == "POST":
            action = request.form.get("action")
            if isinstance(action, str):
                played_card_name = request.form.get("played_card")
                played_card = None
                if isinstance(played_card_name, str):
                    played_card_data = played_card_name.split(" ")
                    played_card = Card(played_card_data[1], played_card_data[0])
                game.execute_player_turn(action, played_card)

    if game.can_execute_turn("opponent"):
        game.execute_opponent_turn()

    player_hand = [{'value': card.value, 'suit': card.suit} for card in game.player.cards]
    dealer_hand = [{'value': card.value, 'suit': card.suit} for card in game.opponent.cards]

    return jsonify({
        'player_hand': player_hand,
        'dealer_hand': dealer_hand,
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