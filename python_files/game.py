from deck import Deck, Card
from player import Player
from poker_rules import PokerRules

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