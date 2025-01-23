import json
import os

class Deck:
    def __init__(self, deck_file_path):
        self.deck_file_path = deck_file_path
        self.deck_data = self.load_deck_data()

    def load_deck_data(self):

        """Carica i dati del mazzo di carte dal file JSON."""

        if os.path.exists(self.deck_file_path):
            try:
                with open(self.deck_file_path, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error reading file: {e}")
                return self.create_default_deck_data()
        else:
            return self.create_default_deck_data()

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