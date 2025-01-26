from deck import Deck, Card
from player import Player
from poker_rules import PokerRules

class Game:
    def __init__(self):
        self.deck = Deck('deck.json').deck_data
        self.player = Player("player")
        self.opponent = Player("opponent")
        self.community_cards = []
        self.turn_count = 0
        self.phase = 'pre-flop'
        self.poker_rules = PokerRules()
        self.setup_players()

    def setup_players(self):
        self.player.cards, self.opponent.cards = self.deck[:2], self.deck[2:4]
        self.deck = self.deck[4:]

    def next_phase(self):
        if self.phase == 'pre-flop':
            self.phase = 'flop'
            self.community_cards = self.deck[:3]
            self.deck = self.deck[3:]
        elif self.phase == 'flop':
            self.phase = 'turn'
            self.community_cards.append(self.deck.pop(0))
        elif self.phase == 'turn':
            self.phase = 'river'
            self.community_cards.append(self.deck.pop(0))
        elif self.phase == 'river':
            self.phase = 'showdown'

    def execute_player_turn(self, action, bet_amount=0):
        if action in ['check', 'call', 'bet', 'raise']:
            self.next_phase()
        elif action == 'fold':
            return 'opponent wins'


    def get_winner(self):
        player_hand = self.player.cards + self.community_cards
        opponent_hand = self.opponent.cards + self.community_cards
        winner = self.poker_rules.determine_winner(player_hand, opponent_hand)
        return winner