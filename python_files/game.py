import random
import time

from player import BettingRound, Player, Dealer, Bot
from deck import Deck
from poker_rules import PokerRules

class TurnManager:
    def __init__(self, players):
        self.players = players
        self.current_turn = self.find_big_blind()

    def find_big_blind(self):
        for i, player in enumerate(self.players):
            if player.name == 'big_blind':
                return (i + 1) % len(self.players)
        return 0

    def next_turn(self):
        self.current_turn = (self.current_turn + 1) % len(self.players)
        print(f"È il turno di {self.players[self.current_turn].name}")

    def get_current_player(self):
        return self.players[self.current_turn]

class Game:
    PRE_FLOP = 'pre-flop'
    FLOP = 'flop'
    TURN = 'turn'
    RIVER = 'river'
    SHOWDOWN = 'showdown'

    VALID_ACTIONS = ['check', 'call', 'bet', 'raise', 'fold']

    def __init__(self, num_players=4):
        self.deck = Deck('deck.json').deck_data
        self.dealer = Dealer("dealer")
        self.players = self.create_players(num_players)
        self.community_cards = []
        self.turn_count = 0
        self.phase = Game.PRE_FLOP
        self.poker_rules = PokerRules()
        self.pot = 0
        self.small_blind, self.big_blind = self.set_blinds()
        self.players_actions = []
        self.blinds_info = {'small_blind': None, 'big_blind': None}
        self.turn_manager = TurnManager(self.players)
        self.setup_players()

    def create_players(self, num_players):
        players = [Player("player")]
        bots = [Bot(f"Bot{i+1}") for i in range(num_players - 1)]
        all_players = players + bots
        random.shuffle(all_players)
        return all_players

    def set_blinds(self):
        small_blind = random.randint(1, 5) * 5
        big_blind = small_blind * 2
        return small_blind, big_blind

    def setup_players(self):
        self.deal_hole_cards()
        self.post_blinds()
        self.remove_dealt_cards_from_deck(2 * len(self.players))

    def post_blinds(self):
        small_blind_player = self.players[0]
        big_blind_player = self.players[1]
        small_blind_player.name = 'small_blind'
        big_blind_player.name = 'big_blind'
        self.pot += small_blind_player.bet_chips(self.small_blind)
        self.pot += big_blind_player.bet_chips(self.big_blind)
        print(f"{small_blind_player.name} posts small blind: {self.small_blind} chips")
        print(f"{big_blind_player.name} posts big blind: {self.big_blind} chips")

    def deal_hole_cards(self):
        for player in self.players:
            player.cards = self.deck[:2]
            self.deck = self.deck[2:]

    def remove_dealt_cards_from_deck(self, num_cards):
        self.deck = self.deck[num_cards:]

    def move_to_flop(self):
        self.phase = Game.FLOP
        self.turn_manager.current_turn = self.turn_manager.find_big_blind()  # Avanza al giocatore alla sinistra del dealer per il flop
        self.deal_flop()

    def deal_flop(self):
        self.community_cards = self.deck[:3]
        self.remove_dealt_cards_from_deck(3)

    def move_to_turn(self):
        self.phase = Game.TURN
        self.turn_manager.current_turn = self.turn_manager.find_big_blind()  # Avanza al giocatore alla sinistra del dealer per il turn
        self.deal_turn_card()

    def deal_turn_card(self):
        self.community_cards.append(self.deck.pop(0))

    def move_to_river(self):
        self.phase = Game.RIVER
        self.turn_manager.current_turn = self.turn_manager.find_big_blind()  # Avanza al giocatore alla sinistra del dealer per il river
        self.deal_river_card()

    def deal_river_card(self):
        self.community_cards.append(self.deck.pop(0))

    def move_to_showdown(self):
        self.phase = Game.SHOWDOWN
        self.evaluate_hands()

    def execute_phase(self):
        print(f"Executing phase: {self.phase}")
        actions_taken = 0
        while actions_taken < len(self.players):
            current_player = self.turn_manager.get_current_player()
            print(f"Current turn: {current_player.name} ({type(current_player).__name__})")
            if isinstance(current_player, Bot):
                try:
                    action = current_player.make_decision(
                        {'community_cards': self.community_cards, 'players': self.players, 'current_bet': self.current_bet, 'pot': self.pot},  # Aggiungi current_bet e pot
                        BettingRound[self.phase.upper()]
                    )
                    print(f"Bot action: {current_player.name} -> {action}")
                    self.execute_turn(current_player, action)
                except KeyError as e:
                    print(f"Error: {e}")
                    break
            else:
                print(f"Waiting for action from {current_player.name}")
                break
            actions_taken += 1
            print(f"Actions taken: {actions_taken}, Total players: {len(self.players)}")
    
        if actions_taken >= len(self.players):
            self.next_phase()
            print(f"Advancing to next phase: {self.phase}")
    
    def execute_turn(self, player, action, bet_amount=0):
        print(f"Executing turn: {player.name} -> action: {action}, bet amount: {bet_amount}")
        message = f"{player.name} executes action: {action} with bet amount: {bet_amount}"
        if action in Game.VALID_ACTIONS:
            if action == 'fold':
                message = f"{player.name} folds"
                self.players.remove(player)
            elif action == 'bet' and bet_amount > 0:
                self.pot += player.bet_chips(bet_amount)
                message = f"{player.name} bets: {bet_amount} chips"
            elif action in ['call', 'raise']:
                # Logica per call e raise
                pass
            self.players_actions.append((player.name, action, bet_amount))
            self.turn_manager.next_turn()
        else:
            raise ValueError(f"Invalid action: {action}")
        return message

    def next_phase(self):
        if self.phase == Game.PRE_FLOP:
            self.move_to_flop()
        elif self.phase == Game.FLOP:
            self.move_to_turn()
        elif self.phase == Game.TURN:
            self.move_to_river()
        elif self.phase == Game.RIVER:
            self.move_to_showdown()
        print(f"Next phase: {self.phase}")

    def evaluate_hands(self):
        best_hands = {}
        for player in self.players:
            player_hand = self.combine_hands(player.cards)
            best_hands[player.name] = self.poker_rules.get_best_hand(player_hand)

        winner = max(best_hands, key=lambda name: self.poker_rules.calculate_hand_ranking(best_hands[name]))
        winner_hand = self.poker_rules.hand_name(best_hands[winner])
        winning_hand = best_hands[winner]
        self.winning_hand_explanation = self.poker_rules.get_hand_explanation(winning_hand)
        print(f"{winner} wins with {winner_hand} and wins {self.pot} chips!")

    def combine_hands(self, player_cards):
        return player_cards + self.community_cards

    def start_game(self):
        while self.phase != Game.SHOWDOWN:
            self.execute_phase()
        winner = self.get_winner()
        print(winner)

    def get_winner(self):
        best_hands = {}
        for player in self.players:
            player_hand = self.combine_hands(player.cards)
            best_hands[player.name] = self.poker_rules.get_best_hand(player_hand)

        winner = max(best_hands, key=lambda name: self.poker_rules.calculate_hand_ranking(best_hands[name]))
        winner_hand = self.poker_rules.hand_name(best_hands[winner])
        return f"{winner} wins with {winner_hand}!"

    def assign_turns(self):
        starting_player = random.choice(self.players)
        print(f"Starting player: {starting_player.name}")  # Debug
        self.current_turn = starting_player.name
        return self.current_turn

    def assign_blinds(self):
        players = self.players[:]
        random.shuffle(players)
        self.blinds_info['small_blind'] = players[0].name
        self.blinds_info['big_blind'] = players[1].name
        return self.blinds_info

    def generate_game_state_response(self):
        player_hand = self.format_hand(self.players[1].cards)
        dealer_hand = self.format_hand(self.players[2].cards) if self.phase == Game.SHOWDOWN else [{'value': 'back', 'suit': 'card_back'}] * 2
        community_cards = self.format_hand(self.community_cards)
        deck_card = {'value': 'back', 'suit': 'card_back'}
        winner = self.get_winner() if self.phase == Game.SHOWDOWN else None

        blinds_info = {
            'small_blind': self.players[0].name,
            'big_blind': self.players[1].name
        }

        blinds_messages = [
            f"{self.players[0].name} posts small blind: {self.small_blind} chips",
            f"{self.players[1].name} posts big blind: {self.big_blind} chips"
        ]

        return {
            'player_hand': player_hand,
            'dealer_hand': dealer_hand,
            'community_cards': community_cards,
            'deck_card': deck_card,
            'winner': winner,
            'phase': self.phase,
            'winning_hand': self.winning_hand_explanation if self.phase == Game.SHOWDOWN else None,
            'blinds_info': blinds_info,
            'blinds_messages': blinds_messages,
            'current_turn': self.players[self.turn_manager.current_turn].name
        }
    
    def format_hand(self, cards):
        return [{'value': card.value, 'suit': card.suit} for card in cards]