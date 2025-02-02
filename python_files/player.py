import random
from deck import Card
from poker_rules import PokerRules
from enum import Enum

# Classe che rappresenta un giocatore
class Player:
    def __init__(self, name: str):
        self.name = name
        self.cards = []
        self.aggressiveness = 0
        self.chips = 1000000000  # Ogni giocatore parte con 1000000000 fiches

    def add_card(self, card: Card):
        if card not in self.cards:
            self.cards.append(card)

    def remove_card(self, card: Card):
        if card in self.cards:
            self.cards.remove(card)

    def has_card(self, card: Card) -> bool:
        return card in self.cards

    def increase_aggressiveness(self):
        self.aggressiveness += 1

    def bet_chips(self, amount):
        if amount <= self.chips:
            self.chips -= amount
            return amount
        return 0

    def get_chips(self):
        return self.chips

    def add_chips(self, amount):
        self.chips += amount

# Classe che rappresenta un dealer
class Dealer(Player):
    def __init__(self, name: str = "Dealer"):
        super().__init__(name)

# Enumerazione delle fasi del gioco di puntata
class BettingRound(Enum):
    PRE_FLOP = 1
    FLOP = 2
    TURN = 3
    RIVER = 4

# Classe che rappresenta un bot (giocatore automatico)
class Bot(Player):
    def __init__(self, name: str):
        super().__init__(name)
        self.poker_rules = PokerRules()
        self.aggressiveness = random.uniform(0.1, 0.9)

    def make_decision(self, game_state, betting_round: BettingRound):
        hand_strength = self.evaluate_hand(game_state['community_cards'])
        pot_odds = self.calculate_pot_odds(game_state)
        opponent_behavior = self.analyze_opponent_behavior(game_state)
    
        print(f"Bot {self.name}: hand_strength={hand_strength}, pot_odds={pot_odds}, opponent_behavior={opponent_behavior}, betting_round={betting_round}")  # Debug
    
        if betting_round == BettingRound.PRE_FLOP:
            decision = self.pre_flop_decision(hand_strength, pot_odds, opponent_behavior)
        else:
            decision = self.post_flop_decision(hand_strength, game_state, pot_odds, opponent_behavior)
    
        print(f"Bot {self.name}: decision={decision}")  # Debug
        return decision

    def pre_flop_decision(self, hand_strength, pot_odds, opponent_behavior):
        if hand_strength >= 5 or pot_odds >= 1.5:
            self.increase_aggressiveness()
            return "raise"
        elif hand_strength >= 3 or pot_odds >= 1.0:
            return "call"
        else:
            return "fold"

    def post_flop_decision(self, hand_strength, game_state, pot_odds, opponent_behavior):
        aggressive_players = self.count_aggressive_players(game_state)

        if hand_strength >= 6 or pot_odds >= 2.0:
            self.increase_aggressiveness()
            return "raise"
        elif hand_strength >= 4 or pot_odds >= 1.5:
            return "call"
        else:
            return "check"

    def evaluate_hand(self, community_cards):
        all_cards = self.cards + community_cards

        if self.poker_rules.full_house(all_cards):
            return 7
        elif self.poker_rules.flush(all_cards):
            return 6
        elif self.poker_rules.straight(all_cards):
            return 5
        elif self.poker_rules.three_of_a_kind(all_cards):
            return 4
        elif self.poker_rules.two_pairs(all_cards):
            return 3
        elif self.poker_rules.pair(all_cards):
            return 2
        else:
            return 1

    def calculate_pot_odds(self, game_state):
        current_bet = game_state['current_bet']
        total_pot = game_state['pot']
        if current_bet > 0:
            return total_pot / current_bet
        return 0

    def count_aggressive_players(self, game_state):
        count = 0
        for player in game_state['players']:
            if player.aggressiveness > 0:
                count += 1
        return count

    def analyze_opponent_behavior(self, game_state):
        behavior_score = 0
        for player in game_state['players']:
            if player.aggressiveness > 0:
                behavior_score += 1
        return behavior_score

    def increase_aggressiveness(self):
        self.aggressiveness += random.uniform(0.05, 0.1)