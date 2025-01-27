import json
import random

class Card:
    def __init__(self, seed: str, value: str):
        self.suit = seed
        self.value = value

    def __repr__(self):
        return f"{self.value} {self.suit}"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Card) and self.suit == other.suit and self.value == self.value

class Deck:
    def __init__(self, deck_file_path):
        self.deck_data = self.load_deck(deck_file_path)

    def load_deck(self, deck_file_path):
        try:
            with open(deck_file_path, 'r') as file:
                deck = json.load(file)
            random.shuffle(deck)
            deck_of_cards = self.create_cards(deck)
            return deck_of_cards
        except FileNotFoundError:
            print(f"File not found: {deck_file_path}")
        except json.JSONDecodeError:
            print("Error decoding JSON from the file")
        return []

    def create_cards(self, deck):
        cards = []
        for card in deck:
            cards.append(Card(card['seed'], card['value']))
        return cards