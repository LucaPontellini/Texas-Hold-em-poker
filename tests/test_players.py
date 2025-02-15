import sys
import os
import pytest
from unittest.mock import mock_open, patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from python_files.players import Player, Dealer, Bot, BotType, BettingRound
from python_files.deck import Card

# Test per la classe Player
def test_player_add_card():
    player = Player("TestPlayer")
    card = Card("Hearts", "A")
    player.add_card(card)
    assert player.has_card(card)

def test_player_remove_card():
    player = Player("TestPlayer")
    card = Card("Hearts", "A")
    player.add_card(card)
    player.remove_card(card)
    assert not player.has_card(card)

def test_player_bet_chips():
    player = Player("TestPlayer")
    initial_chips = player.get_chips()
    bet_amount = 100
    player.bet_chips(bet_amount)
    assert player.get_chips() == initial_chips - bet_amount

def test_player_add_chips():
    player = Player("TestPlayer")
    initial_chips = player.get_chips()
    player.add_chips(200)
    assert player.get_chips() == initial_chips + 200

# Test per la classe Dealer
def test_dealer_shuffle_deck():
    dealer = Dealer()
    original_deck = dealer.deck.deck_data.copy()
    dealer.shuffle_deck()
    assert dealer.deck.deck_data != original_deck

def test_dealer_deal_hole_cards():
    dealer = Dealer()
    players = [Player("Player1"), Player("Player2")]
    dealer.deal_hole_cards(players)
    for player in players:
        assert len(player.cards) == 2

def test_dealer_deal_community_cards():
    dealer = Dealer()
    game_state = {'community_cards': []}
    dealer.deal_community_cards(game_state, 3)
    assert len(game_state['community_cards']) == 3

def test_dealer_determine_winner():
    dealer = Dealer()
    player1 = Player("Player1")
    player2 = Player("Player2")
    player1.add_card(Card("Hearts", "A"))
    player1.add_card(Card("Diamonds", "A"))
    player2.add_card(Card("Clubs", "K"))
    player2.add_card(Card("Spades", "K"))
    game_state = {'community_cards': [Card("Hearts", "2"), Card("Hearts", "3"), Card("Hearts", "4"), Card("Hearts", "5"), Card("Hearts", "6")]}
    winner = dealer.determine_winner([player1, player2], game_state)
    assert winner == player1

# Test per la classe Bot
@pytest.mark.parametrize("bot_type", BotType)
def test_bot_make_decision(bot_type):
    bot = Bot("TestBot", bot_type)
    game_state = {
        'community_cards': [Card("Hearts", "A"), Card("Diamonds", "K"), Card("Clubs", "Q")],
        'current_bet': 50,
        'pot': 100,
        'players': [bot],
        'dealer_index': 0
    }
    decision, bet_amount = bot.make_decision(game_state, BettingRound.PRE_FLOP)
    assert decision in ["fold", "check", "call", "bet", "raise"]

def test_bot_evaluate_hand():
    bot = Bot("TestBot", BotType.AGGRESSIVE)
    community_cards = [Card("Hearts", "2"), Card("Hearts", "3"), Card("Hearts", "4"), Card("Hearts", "5"), Card("Hearts", "6")]
    bot.add_card(Card("Hearts", "7"))  # Cambiato da "Diamonds" a "Hearts"
    bot.add_card(Card("Hearts", "8"))  # Cambiato da "Diamonds" a "Hearts"
    hand_strength = bot.evaluate_hand(community_cards)
    print(f"Hand strength: {hand_strength}")
    assert hand_strength == 9  # Straight Flush

def test_bot_calculate_pot_odds():
    bot = Bot("TestBot", BotType.AGGRESSIVE)
    game_state = {'current_bet': 50, 'pot': 100}
    pot_odds = bot.calculate_pot_odds(game_state)
    assert pot_odds == 2.0

def test_bot_analyze_opponent_behavior():
    bot = Bot("TestBot", BotType.AGGRESSIVE)
    game_state = {'players': [{'aggressiveness': 0.5}, {'aggressiveness': 0.7}]}
    behavior_score = bot.analyze_opponent_behavior(game_state)
    assert behavior_score == 2

def test_bot_evaluate_table_position():
    bot = Bot("TestBot", BotType.AGGRESSIVE)
    player1 = Player("Player1")
    player2 = Player("Player2")
    game_state = {
        'players': [player1, bot, player2],
        'dealer_index': 0
    }
    position = bot.evaluate_table_position(game_state)
    assert position == 'small blind'

if __name__ == '__main__':
    pytest.main(["-v", "test_players.py"])