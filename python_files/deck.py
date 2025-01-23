import json
import os
import random

class Deck:
    def __init__(self, deck_file_path):
        self.deck_data = self.load_deck(deck_file_path)

    def load_deck(self, deck_file_path):

        """Carica il mazzo di carte da un file JSON."""
        
        with open(deck_file_path, 'r') as file:
            deck = json.load(file)
        random.shuffle(deck)
        return deck
    
    def save_deck_data(self):

        """Salva i dati del mazzo di carte in un file JSON."""

        try:
            with open(self.deck_file_path, 'w') as f:
                json.dump(self.deck_data, f, indent=4)
        except Exception as e:
            print(f"Error writing file: {e}")

    def create_default_deck_data(self):

        """Crea i dati predefiniti del mazzo di carte."""

        numeric_values = [str(i) for i in range(2, 11)]
        face_values = ["J", "Q", "K", "A"]
        all_values = numeric_values + face_values

        def create_suit_data(suit, values):

            """Crea i dati del seme."""

            return [{"value": value, "suit": suit} for value in values]

        hearts = create_suit_data("Hearts", all_values)
        diamonds = create_suit_data("Diamonds", all_values)
        clubs = create_suit_data("Clubs", all_values)
        spades = create_suit_data("Spades", all_values)

        deck_data = {
            "Hearts": hearts,
            "Diamonds": diamonds,
            "Clubs": clubs,
            "Spades": spades
        }

        self.deck_data = deck_data
        self.save_deck_data()
        return deck_data