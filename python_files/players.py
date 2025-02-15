from .deck import Card, Deck
from .poker_rules import PokerRules
from enum import Enum
import random

class Player:
    def __init__(self, name: str):
        self.name = name
        self.cards = []
        self.aggressiveness = 0
        self.chips = 1000000000 #è da modificare per il mio casino perchè tocca integrarlo con il cassiere e l'account del giocatore
        self.has_acted = False
        self.current_bet = 0
        self.poker_rules = PokerRules()

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
        if amount <= 0:
            print(f"{self.name} ha tentato di scommettere un importo non valido: {amount}")
            return 0
        if amount <= self.chips:
            self.chips -= amount
            self.current_bet += amount
            return amount
        print(f"{self.name} non ha abbastanza fiches per scommettere {amount}. Fiches disponibili: {self.chips}")
        return 0

    def get_chips(self):
        return self.chips

    def add_chips(self, amount):
        self.chips += amount

    def reset_has_acted(self):
        self.has_acted = False
        print(f"{self.name} has_acted reset to {self.has_acted}")

    def set_has_acted(self):
        self.has_acted = True
        print(f"{self.name} has set has_acted to True")

    def evaluate_hand(self, community_cards):
            all_cards = self.cards + community_cards
            return self.poker_rules.calculate_hand_ranking(all_cards)

class Dealer(Player):
    def __init__(self, name: str = "Dealer", deck=None):
        super().__init__(name)
        self.deck = deck if deck else Deck()

    def shuffle_deck(self):
        self.deck.shuffle()

    def deal_hole_cards(self, players):
        for player in players:
            player.add_card(self.deck.draw_card())
            player.add_card(self.deck.draw_card())

    def deal_community_cards(self, game_state, number_of_cards):
        for _ in range(number_of_cards):
            game_state['community_cards'].append(self.deck.draw_card())

    def determine_winner(self, players, game_state):
        # Logica per determinare il vincitore basata sulla forza della mano
        best_hand_strength = 0
        winner = None
        for player in players:
            hand_strength = player.evaluate_hand(game_state['community_cards'])
            if hand_strength > best_hand_strength:
                best_hand_strength = hand_strength
                winner = player
        return winner

    def distribute_winnings(self, winner, game_state):
        winner.add_chips(game_state['pot'])
        game_state['pot'] = 0

class BettingRound(Enum):
    PRE_FLOP = 1
    FLOP = 2
    TURN = 3
    RIVER = 4

class BotType(Enum):
    AGGRESSIVE = 1 # Giocatore aggressivo che punta frequentemente e cerca di dominare il tavolo.
    CONSERVATIVE = 2 # Giocatore conservatore che gioca solo mani forti e punta raramente.
    BLUFFER = 3 # Giocatore bluffer che punta e rilancia frequentemente con mani deboli per ingannare gli avversari.
    TIGHT = 4 # Giocatore chiuso che gioca pochissime mani, solo quelle molto forti.
    LOOSE = 5 # Giocatore aperto che gioca molte mani, incluse molte mani speculative.
    PASSIVE = 6 # Giocatore passivo che rilancia raramente e preferisce chiamare e fare check.
    MANIAC = 7 # Giocatore maniaco che gioca estremamente aggressivo, rilanciando quasi sempre.
    CALLING_STATION = 8 # Giocatore che chiama frequentemente ma rilancia raramente, anche con mani forti.

class Bot(Player):
    def __init__(self, name: str, bot_type: BotType):
        super().__init__(name)
        self.poker_rules = PokerRules()
        self.aggressiveness = random.uniform(0.1, 0.9)
        self.bot_type = bot_type
        self.current_bet = 0
        self.actions = []

    def record_action(self, action, bet_amount):
        self.actions.append({'action': action, 'bet_amount': bet_amount})

    def get_actions(self):
        return self.actions

    def make_decision(self, game_state, betting_round: BettingRound):
        hand_strength = self.evaluate_hand(game_state['community_cards'])
        pot_odds = self.calculate_pot_odds(game_state)
        opponent_behavior = self.analyze_opponent_behavior(game_state)
        table_position = self.evaluate_table_position(game_state)

        print(f"Bot {self.name}: hand_strength={hand_strength}, pot_odds={pot_odds}, opponent_behavior={opponent_behavior}, table_position={table_position}, betting_round={betting_round}")

        if betting_round == BettingRound.PRE_FLOP:
            decision, bet_amount = self.pre_flop_decision(hand_strength, pot_odds, opponent_behavior, table_position)
        else:
            decision, bet_amount = self.post_flop_decision(hand_strength, game_state, pot_odds, opponent_behavior, table_position)

        if decision in ['bet', 'raise'] and bet_amount <= 0:
            decision = 'fold'

        print(f"Bot {self.name}: decision={decision}, bet_amount={bet_amount}")

        self.record_action(decision, bet_amount)

        return decision, bet_amount

    def pre_flop_decision(self, hand_strength, pot_odds, opponent_behavior, table_position):
        bet_amount = random.randint(10, 100)
        if self.bot_type == BotType.AGGRESSIVE:
            if hand_strength >= 3 or pot_odds >= 1.0:
                self.increase_aggressiveness()
                return "raise", bet_amount
            elif random.random() < 0.3:
                return "bet", bet_amount
        elif self.bot_type == BotType.CONSERVATIVE:
            if hand_strength >= 5 or pot_odds >= 1.5:
                return "call", bet_amount
            elif random.random() < 0.2:
                return "raise", bet_amount
        elif self.bot_type == BotType.BLUFFER:
            if random.random() < 0.4:
                return "raise", bet_amount
        elif self.bot_type == BotType.TIGHT:
            if hand_strength >= 6 or pot_odds >= 2.0:
                return "call", bet_amount
        elif self.bot_type == BotType.LOOSE:
            if hand_strength >= 2 or pot_odds >= 1.0:
                self.increase_aggressiveness()
                return "raise", bet_amount
            elif random.random() < 0.5:
                return "call", bet_amount
        elif self.bot_type == BotType.PASSIVE:
            if hand_strength >= 4 or pot_odds >= 1.5:
                return "call", bet_amount
            return "check", 0
        elif self.bot_type == BotType.MANIAC:
            self.increase_aggressiveness()
            return "raise", bet_amount
        elif self.bot_type == BotType.CALLING_STATION:
            return "call", bet_amount

        return "fold", bet_amount

    def post_flop_decision(self, hand_strength, game_state, pot_odds, opponent_behavior, table_position):
        bet_amount = random.randint(10, 100)
        if self.bot_type == BotType.AGGRESSIVE:
            if hand_strength >= 4 or pot_odds >= 1.5:
                self.increase_aggressiveness()
                return "raise", bet_amount
            elif random.random() < 0.4:
                return "bet", bet_amount
        elif self.bot_type == BotType.CONSERVATIVE:
            if hand_strength >= 6 or pot_odds >= 2.0:
                return "call", bet_amount
            elif random.random() < 0.3:
                return "raise", bet_amount
        elif self.bot_type == BotType.BLUFFER:
            if random.random() < 0.5:
                return "raise", bet_amount
        elif self.bot_type == BotType.TIGHT:
            if hand_strength >= 6 or pot_odds >= 2.0:
                return "call", bet_amount
        elif self.bot_type == BotType.LOOSE:
            if hand_strength >= 2 or pot_odds >= 1.0:
                self.increase_aggressiveness()
                return "raise", bet_amount
            elif random.random() < 0.5:
                return "call", bet_amount
        elif self.bot_type == BotType.PASSIVE:
            if hand_strength >= 4 or pot_odds >= 1.5:
                return "call", bet_amount
            return "check", 0
        elif self.bot_type == BotType.MANIAC:
            self.increase_aggressiveness()
            return "raise", bet_amount
        elif self.bot_type == BotType.CALLING_STATION:
            return "call", bet_amount

        return "check", 0

    def evaluate_hand(self, community_cards):
        all_cards = self.cards + community_cards
        return self.poker_rules.calculate_hand_ranking(all_cards)

    def calculate_pot_odds(self, game_state):
        current_bet = game_state['current_bet']
        total_pot = game_state['pot']
        if current_bet > 0:
            return total_pot / current_bet
        return 0

    def analyze_opponent_behavior(self, game_state):
        behavior_score = 0
        for player in game_state['players']:
            aggressiveness = player['aggressiveness'] if isinstance(player, dict) else player.aggressiveness
            if aggressiveness > 0:
                behavior_score += 1
        return behavior_score
    
    def evaluate_table_position(self, game_state):
        current_player_index = game_state['players'].index(self)
        dealer_index = game_state['dealer_index']
        num_players = len(game_state['players'])
        relative_position = (current_player_index - dealer_index) % num_players

        if relative_position == 1:
            return 'small blind'
        elif relative_position == 2:
            return 'big blind'
        elif relative_position <= num_players // 3:
            return 'early'
        elif relative_position <= (2 * num_players) // 3:
            return 'middle'
        else:
            return 'late'