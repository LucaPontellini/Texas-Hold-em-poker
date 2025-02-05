import json
import os
import random

# Classe che rappresenta una carta
class Card:
    def __init__(self, seed: str, value: str):
        self.suit = seed
        self.value = value

    def __repr__(self):
        # Rappresentazione leggibile della carta
        return f"{self.value} {self.suit}"

    def __eq__(self, other: object) -> bool:
        # Confronto tra due carte (stesso seme e valore)
        return isinstance(other, Card) and self.suit == other.suit and self.value == other.value

# Classe che rappresenta un mazzo di carte
class Deck:
    def __init__(self, deck_file='deck.json'):
        deck_path = os.path.join(os.path.dirname(__file__), '..', deck_file)
        if not os.path.exists(deck_path):
            print(f"File not found: {deck_path}")
            self.deck_data = []
        else:
            self.deck_data = self.load_deck(deck_path)
            self.shuffle()  # Mescola le carte
            self.print_deck()  # Stampa il mazzo per debug

    def load_deck(self, deck_file_path):
        try:
            with open(deck_file_path, 'r') as file:
                deck = json.load(file)
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

    def shuffle(self):
        random.shuffle(self.deck_data)

    def draw_card(self):
        return self.deck_data.pop() if self.deck_data else None

    def print_deck(self):
        print(f"Deck size: {len(self.deck_data)}")
        for card in self.deck_data:
            print(card)