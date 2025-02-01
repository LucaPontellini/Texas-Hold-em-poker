from deck import Card
from enum import Enum
from poker_rules import PokerRules

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

    # Metodo per prendere decisioni basate sullo stato del gioco e sulla fase di puntata
    def make_decision(self, game_state, betting_round: BettingRound):
        # Valutazione della forza della mano del bot
        hand_strength = self.evaluate_hand(game_state['community_cards'])

        # Decidere in base alla fase del gioco
        if betting_round == BettingRound.PRE_FLOP:
            return self.pre_flop_decision(hand_strength)
        elif betting_round == BettingRound.FLOP:
            return self.post_flop_decision(hand_strength, game_state)
        elif betting_round == BettingRound.TURN:
            return self.post_flop_decision(hand_strength, game_state)
        elif betting_round == BettingRound.RIVER:
            return self.post_flop_decision(hand_strength, game_state)

    # Metodo per prendere decisioni pre-flop
    def pre_flop_decision(self, hand_strength):
        if hand_strength >= 2:  # Ha almeno una coppia
            self.increase_aggressiveness()  # Incrementa l'aggressività del bot
            return "raise"
        else:
            return "fold"

    # Metodo per prendere decisioni post-flop
    def post_flop_decision(self, hand_strength, game_state):
        # Conta i giocatori aggressivi
        aggressive_players = self.count_aggressive_players(game_state)

        if hand_strength >= 6:  # Ha almeno un Flush
            self.increase_aggressiveness()  # Incrementa l'aggressività del bot
            return "raise"
        elif hand_strength >= 4 and aggressive_players < 2:  # Ha almeno un Tris e pochi giocatori aggressivi
            return "call"
        else:
            return "fold"

    # Metodo per valutare la forza della mano del bot
    def evaluate_hand(self, community_cards):
        # Combina le carte del bot con le carte comuni
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

    def count_aggressive_players(self, game_state):
        count = 0
        for player in game_state['players']:
            if player.aggressiveness > 0:
                count += 1
        return count