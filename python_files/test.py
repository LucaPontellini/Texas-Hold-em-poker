Capisco, organizzare ogni classe in un file Python separato può rendere il codice più leggibile e gestibile. Possiamo farlo mantenendo l'architettura modulare e poi unire tutto nel file principale dove usiamo Flask.

Ecco un esempio di come puoi strutturare i file Python:

### card.py

python
class Card:
    def __init__(self, suit: str, value: str):
        self.suit = suit
        self.value = value

    def __repr__(self):
        return f"{self.value} {self.suit}"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Card) and self.suit == other.suit and self.value == self.value


### deck.py

python
import json
import random
from card import Card

class Deck:
    def __init__(self, deck_file_path):
        self.deck_data = self.load_deck(deck_file_path)

    def load_deck(self, deck_file_path):
        with open(deck_file_path, 'r') as file:
            deck = json.load(file)
        random.shuffle(deck)
        return deck


### player.py

python
from card import Card

class Player:
    def __init__(self, name: str):
        self.name = name
        self.cards = []

    def add_card(self, card: Card):
        self.cards.append(card)

    def remove_card(self, card: Card):
        self.cards.remove(card)

    def has_card(self, card: Card) -> bool:
        return card in self.cards


### poker_rules.py

python
class PokerRules:
    def __init__(self):
        self.hand_rankings = {
            self.straight_flush: 9,
            self.four_of_a_kind: 8,
            self.full_house: 7,
            self.flush: 6,
            self.straight: 5,
            self.three_of_a_kind: 4,
            self.two_pairs: 3,
            self.pair: 2
        }

    def pair(self, hand):
        values = [card['value'] for card in hand]
        return any(values.count(value) == 2 for value in values)

    def two_pairs(self, hand):
        values = [card['value'] for card in hand]
        pairs = [value for value in values if values.count(value) == 2]
        return len(set(pairs)) == 2

    def three_of_a_kind(self, hand):
        values = [card['value'] for card in hand]
        return any(values.count(value) == 3 for value in values)

    def straight(self, hand):
        card_values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        values = sorted(card_values.index(card['value']) for card in hand)
        return all(values[i] - values[i-1] == 1 for i in range(1, len(values))) or \
               (values[-1] == 12 and all(values[i] - values[i-1] == 1 for i in range(1, len(values)-1)))

    def flush(self, hand):
        suits = [card['suit'] for card in hand]
        return len(set(suits)) == 1

    def full_house(self, hand):
        return self.three_of_a_kind(hand) and self.pair(hand)

    def four_of_a_kind(self, hand):
        values = [card['value'] for card in hand]
        return any(values.count(value) == 4 for value in values)

    def straight_flush(self, hand):
        return self.straight(hand) and self.flush(hand)

    def determine_winner(self, player_hand, opponent_hand):
        player_ranking = max((ranking for check_hand, ranking in self.hand_rankings.items() if check_hand(player_hand)), default=1)
        opponent_ranking = max((ranking for check_hand, ranking in self.hand_rankings.items() if check_hand(opponent_hand)), default=1)

        if player_ranking > opponent_ranking:
            return "Player wins!"
        elif opponent_ranking > player_ranking:
            return "Dealer wins!"
        else:
            return "It's a tie!"


### game.py

python
from deck import Deck
from player import Player
from poker_rules import PokerRules
from card import Card

class Game:
    def __init__(self):
        self.deck = Deck('python_files/deck.json').deck_data
        self.player = Player("player")
        self.opponent = Player("opponent")
        self.community_cards = []
        self.turn_count = 0
        self.last_player_name = None
        self.last_played_card_turn = 0
        self.poker_rules = PokerRules()
        self.setup_players()

    def setup_players(self):
        self.player.cards, self.opponent.cards = self.poker_rules.distribute_cards(self.deck)

    def get_last_played_card(self) -> Card | None:
        return self.community_cards[-1] if self.community_cards else None

    def can_execute_turn(self, player_name: str) -> bool:
        if self.last_player_name == player_name or self.last_player_name is None or self.last_played_card_turn < self.turn_count - 1:
            return True
        return False

    def can_card_be_played(self, card: Card) -> bool:
        top_card = self.get_last_played_card()
        if top_card is None:
            return False
        return card.suit == top_card.suit or card.value == top_card.value

    def execute_player_turn(self, action: str, played_card: Card | None = None) -> bool:
        if action == "draw":
            self.player.add_card(self.deck.pop())
            return True
        elif action == "pass":
            return True
        elif action == "play" and isinstance(played_card, Card) and self.player.has_card(played_card) and self.can_card_be_played(played_card):
            self.community_cards.append(played_card)
            self.player.remove_card(played_card)
            self.last_played_card_turn = self.turn_count
            return True
        return False

    def execute_opponent_turn(self):
        for card in self.opponent.cards:
            if self.can_card_be_played(card):
                self.community_cards.append(card)
                self.opponent.remove_card(card)
                self.last_played_card_turn = self.turn_count
                return
        self.opponent.add_card(self.deck.pop())

    def get_winner(self) -> str:
        player_hand = self.player.cards + self.community_cards
        opponent_hand = self.opponent.cards + self.community_cards
        player_ranking = self.poker_rules.determine_winner(player_hand, opponent_hand)
        if player_ranking == "Player wins!":
            return "player"
        elif player_ranking == "Dealer wins!":
            return "opponent"
        return ""


### app.py (file principale)

python
from flask import Flask, render_template, request, jsonify
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


In questo modo, ogni classe è separata in un proprio file Python, rendendo il codice più ordinato e gestibile. Il file principale app.py integra tutto utilizzando Flask. Se hai bisogno di ulteriori modifiche o chiarimenti, sono qui per aiutarti!