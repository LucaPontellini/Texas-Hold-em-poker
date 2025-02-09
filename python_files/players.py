import random
from .deck import Card
from .poker_rules import PokerRules
from enum import Enum

# Classe che rappresenta un giocatore
class Player:
    def __init__(self, name: str):
        self.name = name
        self.cards = []
        self.aggressiveness = 0
        self.chips = 1000000000  # Ogni giocatore parte con 1000000000 fiches
        self.has_acted = False
        self.current_bet = 0

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
            self.current_bet += amount  # Tiene traccia della scommessa corrente
            return amount
        return 0

    def get_chips(self):
        return self.chips

    def add_chips(self, amount):
        self.chips += amount

    def reset_has_acted(self):
        self.has_acted = False
        print(f"{self.name} has_acted reset to {self.has_acted}")  # Log di debug

    def set_has_acted(self):
        self.has_acted = True
        print(f"{self.name} has set has_acted to True")  # Log di debug

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

# Tipi di Stili di Gioco dei Bot
class BotType(Enum):
    AGGRESSIVE = 1
    CONSERVATIVE = 2
    BLUFFER = 3

# Classe che rappresenta un bot (giocatore automatico)
class Bot(Player):
    def __init__(self, name: str, bot_type: BotType):
        super().__init__(name)
        self.poker_rules = PokerRules()
        self.aggressiveness = random.uniform(0.1, 0.9)
        self.bot_type = bot_type
        self.current_bet = 0

    def make_decision(self, game_state, betting_round: BettingRound):
        hand_strength = self.evaluate_hand(game_state['community_cards'])
        pot_odds = self.calculate_pot_odds(game_state)
        opponent_behavior = self.analyze_opponent_behavior(game_state)

        print(f"Bot {self.name}: hand_strength={hand_strength}, pot_odds={pot_odds}, opponent_behavior={opponent_behavior}, betting_round={betting_round}")

        if betting_round == BettingRound.PRE_FLOP:
            decision, bet_amount = self.pre_flop_decision(hand_strength, pot_odds, opponent_behavior)
        else:
            decision, bet_amount = self.post_flop_decision(hand_strength, game_state, pot_odds, opponent_behavior)

        if decision in ['bet', 'raise'] and bet_amount <= 0:
            decision = 'fold'  # Folda se bet_amount non è valido per puntata o rilancio

        print(f"Bot {self.name}: decision={decision}, bet_amount={bet_amount}")

        return decision, bet_amount

    def pre_flop_decision(self, hand_strength, pot_odds, opponent_behavior):
        bet_amount = random.randint(10, 100)
        if self.bot_type == BotType.AGGRESSIVE:
            if hand_strength >= 3 or pot_odds >= 1.0:
                self.increase_aggressiveness()
                return "raise", bet_amount
            elif random.random() < 0.3:
                return "bet", bet_amount  # Aggiunge più "bet" nelle decisioni
        elif self.bot_type == BotType.CONSERVATIVE:
            if hand_strength >= 5 or pot_odds >= 1.5:
                return "call", bet_amount
            elif random.random() < 0.2:
                return "raise", bet_amount  # Rende i bot conservatori un po' più aggressivi
        elif self.bot_type == BotType.BLUFFER:
            if random.random() < 0.4:  # 40% chance di bluffing
                return "raise", bet_amount
        return "fold", bet_amount

    def post_flop_decision(self, hand_strength, game_state, pot_odds, opponent_behavior):
        bet_amount = random.randint(10, 100)
        if self.bot_type == BotType.AGGRESSIVE:
            if hand_strength >= 4 or pot_odds >= 1.5:
                self.increase_aggressiveness()
                return "raise", bet_amount
            elif random.random() < 0.4:
                return "bet", bet_amount  # Aggiunge più "bet" nelle decisioni
        elif self.bot_type == BotType.CONSERVATIVE:
            if hand_strength >= 6 or pot_odds >= 2.0:
                return "call", bet_amount
            elif random.random() < 0.3:
                return "raise", bet_amount  # Rende i bot conservatori un po' più aggressivi
        elif self.bot_type == BotType.BLUFFER:
            if random.random() < 0.5:  # 50% chance di bluffing
                return "raise", bet_amount
        return "check", 0  # Imposta bet_amount a 0 per check

    def evaluate_hand(self, community_cards):
        all_cards = self.cards + community_cards
        if not all_cards:
            return 0  # Nessuna carta, forza della mano è 0

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
            aggressiveness = player['aggressiveness'] if isinstance(player, dict) else player.aggressiveness
            if aggressiveness > 0:
                behavior_score += 1
        return behavior_score

    def increase_aggressiveness(self):
        self.aggressiveness += random.uniform(0.05, 0.1)