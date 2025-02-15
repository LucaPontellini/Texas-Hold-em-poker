import sys
import os
import pytest
from unittest.mock import mock_open, patch

# Aggiungi la directory principale del progetto al PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from python_files.deck import Card, Deck

def test_create_standard_deck():
    deck = Deck()
    assert len(deck.deck_data) == 52  # Check if the deck has 52 cards
    expected_suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    expected_values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    for suit in expected_suits:
        for value in expected_values:
            assert Card(suit, value) in deck.deck_data

def test_shuffle_deck():
    deck = Deck()
    original_deck = deck.deck_data.copy()
    deck.shuffle()
    assert deck.deck_data != original_deck  # Check if the deck order has changed

def test_draw_card():
    deck = Deck()
    initial_size = len(deck.deck_data)
    card = deck.draw_card()
    assert isinstance(card, Card)  # Check if the drawn card is an instance of Card
    assert len(deck.deck_data) == initial_size - 1  # Check if the deck size decreased by 1

def test_load_deck():
    mock_deck_data = '[{"seed": "Hearts", "value": "2"}, {"seed": "Diamonds", "value": "3"}]'
    with patch('builtins.open', mock_open(read_data=mock_deck_data)):
        deck = Deck('deck.json')
        assert len(deck.deck_data) == 2  # Check if the deck was loaded correctly
        assert Card('Hearts', '2') in deck.deck_data
        assert Card('Diamonds', '3') in deck.deck_data

if __name__ == '__main__':
    pytest.main(["-v", "test_deck.py"])