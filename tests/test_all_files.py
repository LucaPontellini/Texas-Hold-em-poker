"""
Questo file esegue test sui vari moduli del progetto Texas Hold'em Poker,
escludendo il file test_game.py che avvia il gioco dal terminale.
I test inclusi verificano il corretto funzionamento delle classi e delle funzioni
relative alle carte, ai giocatori, alle regole del poker e alle rotte dell'app Flask.
"""

import os
import sys
import pytest
import random
from flask import app
from itertools import combinations

# Percorso alla directory principale del progetto
project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Aggiunge il percorso alla directory principale del progetto al sys.path
sys.path.insert(0, project_path)

from python_files.deck import Card, Deck
from python_files.players import Player, Dealer, Bot, BotType, BettingRound
from python_files.poker_rules import PokerRules
from python_files.game import Game, TurnManager

# Test per la classe Card
def test_card_initialization():
    card = Card('Hearts', 'A')
    assert card.suit == 'Hearts'
    assert card.value == 'A'

def test_card_representation():
    card = Card('Diamonds', 'K')
    assert repr(card) == 'K Diamonds'

def test_card_equality():
    card1 = Card('Clubs', 'Q')
    card2 = Card('Clubs', 'Q')
    assert card1 == card2
    card3 = Card('Spades', 'J')
    assert card1 != card3

# Test per la classe Deck
def test_deck_initialization(monkeypatch):
    def mock_load_deck(_):
        return [Card('Hearts', 'A'), Card('Diamonds', 'K')]
    
    monkeypatch.setattr(Deck, 'load_deck', mock_load_deck)
    deck = Deck()
    assert len(deck.deck_data) == 2

def test_deck_shuffle(monkeypatch):
    def mock_load_deck(_):
        return [Card('Hearts', 'A'), Card('Diamonds', 'K')]
    
    monkeypatch.setattr(Deck, 'load_deck', mock_load_deck)
    deck = Deck()
    initial_deck = deck.deck_data.copy()
    deck.shuffle()
    assert deck.deck_data != initial_deck
    assert sorted(deck.deck_data, key=lambda card: card.suit + card.value) == sorted(initial_deck, key=lambda card: card.suit + card.value)

def test_draw_card(monkeypatch):
    def mock_load_deck(_):
        return [Card('Hearts', 'A'), Card('Diamonds', 'K')]
    
    monkeypatch.setattr(Deck, 'load_deck', mock_load_deck)
    deck = Deck()
    drawn_card = deck.draw_card()
    assert drawn_card == Card('Diamonds', 'K')
    assert len(deck.deck_data) == 1

def test_print_deck(monkeypatch, capsys):
    def mock_load_deck(_):
        return [Card('Hearts', 'A'), Card('Diamonds', 'K')]
    
    monkeypatch.setattr(Deck, 'load_deck', mock_load_deck)
    deck = Deck()
    deck.print_deck()
    captured = capsys.readouterr()
    assert "Deck size: 2" in captured.out
    assert "A Hearts" in captured.out
    assert "K Diamonds" in captured.out

# Test per la classe Player
def test_player_initialization():
    player = Player('Test Player')
    assert player.name == 'Test Player'
    assert player.chips == 1000000000
    assert player.has_acted == False
    assert player.current_bet == 0

def test_add_and_remove_card():
    player = Player('Test Player')
    card = Card('Hearts', 'A')
    player.add_card(card)
    assert player.has_card(card)
    player.remove_card(card)
    assert not player.has_card(card)

def test_increase_aggressiveness():
    player = Player('Test Player')
    initial_aggressiveness = player.aggressiveness
    player.increase_aggressiveness()
    assert player.aggressiveness == initial_aggressiveness + 1

def test_bet_chips():
    player = Player('Test Player')
    initial_chips = player.chips
    bet_amount = player.bet_chips(100)
    assert player.chips == initial_chips - 100
    assert bet_amount == 100
    assert player.current_bet == 100

def test_reset_and_set_has_acted():
    player = Player('Test Player')
    player.set_has_acted()
    assert player.has_acted
    player.reset_has_acted()
    assert not player.has_acted

# Test per la classe Bot
def test_bot_initialization():
    bot = Bot('Test Bot', BotType.AGGRESSIVE)
    assert bot.name == 'Test Bot'
    assert bot.bot_type == BotType.AGGRESSIVE
    assert 0.1 <= bot.aggressiveness <= 0.9

def test_bot_make_decision(monkeypatch):
    bot = Bot('Test Bot', BotType.AGGRESSIVE)
    game_state = {
        'community_cards': [Card('Hearts', 'A'), Card('Diamonds', 'K')],
        'current_bet': 50,
        'pot': 200,
        'players': []
    }

    def mock_evaluate_hand(_):
        return 5

    def mock_calculate_pot_odds(_):
        return 1.5

    def mock_analyze_opponent_behavior(_):
        return 1

    monkeypatch.setattr(bot, 'evaluate_hand', mock_evaluate_hand)
    monkeypatch.setattr(bot, 'calculate_pot_odds', mock_calculate_pot_odds)
    monkeypatch.setattr(bot, 'analyze_opponent_behavior', mock_analyze_opponent_behavior)
    
    decision, bet_amount = bot.make_decision(game_state, BettingRound.PRE_FLOP)
    assert decision in ['raise', 'bet', 'fold']
    assert bet_amount >= 0

# Test per la classe PokerRules
def test_poker_rules_hand_rankings():
    poker_rules = PokerRules()
    hand_rankings = poker_rules.define_hand_rankings()
    assert hand_rankings['royal_flush'] == 10
    assert hand_rankings['straight_flush'] == 9
    assert hand_rankings['four_of_a_kind'] == 8
    assert hand_rankings['full_house'] == 7
    assert hand_rankings['flush'] == 6
    assert hand_rankings['straight'] == 5
    assert hand_rankings['three_of_a_kind'] == 4
    assert hand_rankings['two_pairs'] == 3
    assert hand_rankings['pair'] == 2
    assert hand_rankings['high_card'] == 1

def test_poker_rules_determine_winner():
    poker_rules = PokerRules()
    player_hand = [Card('Hearts', 'A'), Card('Hearts', 'K')]
    opponent_hand = [Card('Diamonds', 'A'), Card('Diamonds', 'K')]
    community_cards = [
        Card('Hearts', 'Q'),
        Card('Hearts', 'J'),
        Card('Hearts', '10'),
        Card('Clubs', '9'),
        Card('Spades', '8')
    ]

    result = poker_rules.determine_winner(player_hand, opponent_hand, community_cards)
    assert "wins with" in result or "It's a tie" in result

# Test per la classe Deck
def test_deck_initialization(monkeypatch):
    def mock_load_deck(self, _):
        return [Card('Hearts', 'A'), Card('Diamonds', 'K')]
    
    monkeypatch.setattr(Deck, 'load_deck', mock_load_deck)
    deck = Deck()
    assert len(deck.deck_data) == 2

def test_deck_shuffle(monkeypatch):
    def mock_load_deck(self, _):
        return [
            Card('Hearts', 'A'), Card('Diamonds', 'K'), Card('Clubs', 'Q'),
            Card('Spades', 'J'), Card('Hearts', '10'), Card('Diamonds', '9')
        ]
    
    monkeypatch.setattr(Deck, 'load_deck', mock_load_deck)
    deck = Deck()
    initial_deck = deck.deck_data.copy()
    deck.shuffle()
    
    # Verifica che il mazzo mescolato non sia uguale al mazzo iniziale
    assert deck.deck_data != initial_deck
    
    # Verifica che tutte le carte siano ancora presenti dopo la mescolatura
    assert sorted(deck.deck_data, key=lambda card: card.suit + card.value) == sorted(initial_deck, key=lambda card: card.suit + card.value)
    
    monkeypatch.setattr(Deck, 'load_deck', mock_load_deck)
    deck = Deck()
    initial_deck = deck.deck_data.copy()
    deck.shuffle()
    assert deck.deck_data != initial_deck
    assert sorted(deck.deck_data, key=lambda card: card.suit + card.value) == sorted(initial_deck, key=lambda card: card.suit + card.value)

def test_draw_card(monkeypatch):
    def mock_load_deck(self, _):
        return [Card('Diamonds', 'K'), Card('Hearts', 'A')]
    
    monkeypatch.setattr(Deck, 'load_deck', mock_load_deck)
    deck = Deck()
    
    # Verifica che il mazzo iniziale sia ordinato come previsto
    assert deck.deck_data == [Card('Diamonds', 'K'), Card('Hearts', 'A')]
    
    drawn_card = deck.draw_card()
    
    # Verifica che la carta estratta sia quella attesa
    assert drawn_card == Card('Hearts', 'A')
    assert len(deck.deck_data) == 1  # Verifica che la dimensione del mazzo sia diminuita
    assert deck.deck_data == [Card('Diamonds', 'K')]  # Verifica che la carta rimanente sia quella attesa

def test_print_deck(monkeypatch, capsys):
    def mock_load_deck(self, _):
        return [Card('Hearts', 'A'), Card('Diamonds', 'K')]
    
    monkeypatch.setattr(Deck, 'load_deck', mock_load_deck)
    deck = Deck()
    deck.print_deck()
    captured = capsys.readouterr()
    assert "Deck size: 2" in captured.out
    assert "A Hearts" in captured.out
    assert "K Diamonds" in captured.out

# Test per la classe Game
def test_game_initialization(monkeypatch):
    def mock_create_players(self, _):
        return [Player("player"), Bot("Bot1", BotType.AGGRESSIVE), Bot("Bot2", BotType.CONSERVATIVE)]
    
    monkeypatch.setattr(Game, 'create_players', mock_create_players)
    game = Game()
    assert len(game.players) == 3

def test_game_phase_transition(monkeypatch):
    def mock_create_players(self, _):
        return [Player("player"), Bot("Bot1", BotType.AGGRESSIVE), Bot("Bot2", BotType.CONSERVATIVE)]
    
    monkeypatch.setattr(Game, 'create_players', mock_create_players)
    game = Game()
    game.setup_players()
    game.move_to_flop()
    assert game.phase == Game.FLOP
    game.move_to_turn()
    assert game.phase == Game.TURN
    game.move_to_river()
    assert game.phase == Game.RIVER
    game.move_to_showdown()
    assert game.phase == Game.SHOWDOWN

def test_game_generate_game_state_response(monkeypatch):
    def mock_create_players(self, _):
        return [Player("player"), Bot("Bot1", BotType.AGGRESSIVE), Bot("Bot2", BotType.CONSERVATIVE)]
    
    monkeypatch.setattr(Game, 'create_players', mock_create_players)
    game = Game()
    game.setup_players()
    response = game.generate_game_state_response()
    assert 'player_hand' in response
    assert 'community_cards' in response
    assert 'current_turn' in response

# Test per l'app Flask
def test_index_route(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b'id="turn-message"' in response.data  # Verifica la presenza di un elemento specifico nell'output HTML

def test_new_game_route(client):
    response = client.post("/new-game")
    assert response.status_code == 200
    assert b"players" in response.data

def test_start_game_route(client):
    response = client.post("/start-game")
    assert response.status_code == 200
    assert b"current_turn" in response.data
    assert b"blinds_info" in response.data

def test_advance_turn_route(client):
    response = client.post("/advance-turn")
    assert response.status_code == 200

def test_execute_bot_turn_route(client):
    response = client.post("/execute-bot-turn")
    assert response.status_code == 200

@pytest.fixture
def client():
    from texas_hold_em_poker import app
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

import pytest

if __name__ == "__main__":
    pytest.main(["--ignore=test_game.py", "-s"])