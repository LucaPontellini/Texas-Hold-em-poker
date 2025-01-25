from deck import Card

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