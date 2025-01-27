from deck import Deck, Card
from player import Player
from poker_rules import PokerRules

class Game:
    PRE_FLOP = 'pre-flop'
    FLOP = 'flop'
    TURN = 'turn'
    RIVER = 'river'
    SHOWDOWN = 'showdown'

    VALID_ACTIONS = ['check', 'call', 'bet', 'raise', 'fold']

    def __init__(self):
        self.deck = Deck('deck.json').deck_data
        self.player = Player("player")
        self.opponent = Player("opponent")
        self.community_cards = []
        self.turn_count = 0
        self.phase = Game.PRE_FLOP
        self.poker_rules = PokerRules()
        self.setup_players()

    def setup_players(self):
        self.deal_hole_cards()
        self.remove_dealt_cards_from_deck()

    def deal_hole_cards(self):
        self.player.cards, self.opponent.cards = self.deck[:2], self.deck[2:4]

    def remove_dealt_cards_from_deck(self):
        self.deck = self.deck[4:]

    def next_phase(self):
        if self.phase == Game.PRE_FLOP:
            self.move_to_flop()
        elif self.phase == Game.FLOP:
            self.move_to_turn()
        elif self.phase == Game.TURN:
            self.move_to_river()
        elif self.phase == Game.RIVER:
            self.move_to_showdown()

    def move_to_flop(self):
        self.phase = Game.FLOP
        self.deal_flop()

    def deal_flop(self):
        self.community_cards = self.deck[:3]
        self.deck = self.deck[3:]

    def move_to_turn(self):
        self.phase = Game.TURN
        self.deal_turn_card()

    def deal_turn_card(self):
        self.community_cards.append(self.deck.pop(0))

    def move_to_river(self):
        self.phase = Game.RIVER
        self.deal_river_card()

    def deal_river_card(self):
        self.community_cards.append(self.deck.pop(0))

    def move_to_showdown(self):
        self.phase = Game.SHOWDOWN

    def execute_player_turn(self, action, bet_amount=0):
        print(f"Executing action: {action} with bet amount: {bet_amount}")
        if action in Game.VALID_ACTIONS:
            if action == 'fold':
                return 'opponent wins'
            if action == 'bet' and bet_amount > 0:
                print(f"Player bets: {bet_amount} chips")
            self.next_phase()
        else:
            raise ValueError(f"Invalid action: {action}")

    def get_winner(self):
        player_hand = self.combine_hands(self.player.cards)
        opponent_hand = self.combine_hands(self.opponent.cards)
        winner = self.poker_rules.determine_winner(player_hand, opponent_hand)
        return winner

    def combine_hands(self, player_cards):
        return player_cards + self.community_cards