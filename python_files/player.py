from deck import Card

class Player:
    def __init__(self, name: str):
        self.name = name
        self.cards = []

    def add_card(self, card: Card):
        if card not in self.cards:
            self.cards.append(card)

    def remove_card(self, card: Card):
        if card in self.cards:
            self.cards.remove(card)

    def has_card(self, card: Card) -> bool:
        return card in self.cards