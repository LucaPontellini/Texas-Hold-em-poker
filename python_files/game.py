import random
from flask import request
from player import BotType, Player, Dealer, Bot, BettingRound
from deck import Deck, Card
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
        return self.get_current_player()

    def get_current_player(self):
        return self.players[self.current_turn]

    def send_turn_to_flask(self):
        current_player = self.get_current_player()
        data = {'current_turn': current_player.name}
        try:
            response = request.post('http://localhost:5000/advance-turn', json=data)
            if response.status_code == 200:
                print("Turn information sent successfully")
            else:
                print(f"Failed to send turn information: {response.status_code}")
        except request.exceptions.RequestException as e:
            print(f"Error sending turn information: {e}")

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
        self.current_bet = 0
        self.small_blind, self.big_blind = self.set_blinds()
        self.players_actions = []
        self.blinds_info = {'small_blind': None, 'big_blind': None}
        self.turn_manager = TurnManager(self.players)

    def create_players(self, num_players):
        players = [Player("player")]
        bot_types = [BotType.AGGRESSIVE, BotType.CONSERVATIVE, BotType.BLUFFER]
        bots = [Bot(f"Bot{i+1}", random.choice(bot_types)) for i in range(num_players - 1)]
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
        print(f"Deck after dealing hole cards: {len(self.deck)}")  # Debugging

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
        print(f"Deck after dealing hole cards: {len(self.deck)}")

    def move_to_flop(self):
        self.phase = Game.FLOP
        self.turn_manager.current_turn = self.turn_manager.find_big_blind()
        self.deal_flop()

    def deal_flop(self):
        self.community_cards = self.deck[:3]
        self.deck = self.deck[3:]

    def move_to_turn(self):
        self.phase = Game.TURN
        self.turn_manager.current_turn = self.turn_manager.find_big_blind()
        self.deal_turn_card()

    def deal_turn_card(self):
        self.community_cards.append(self.deck.pop(0))

    def move_to_river(self):
        self.phase = Game.RIVER
        self.turn_manager.current_turn = self.turn_manager.find_big_blind()
        self.deal_river_card()

    def deal_river_card(self):
        self.community_cards.append(self.deck.pop(0))

    def move_to_showdown(self):
        self.phase = Game.SHOWDOWN
        self.evaluate_hands()

    def execute_turn(self, player, action, bet_amount=0):
        print(f"Executing turn: {player.name} -> action: {action}, bet amount: {bet_amount}")
        message = f"{player.name} executes action: {action} with bet amount: {bet_amount}"
        if action in Game.VALID_ACTIONS:
            if action == 'fold':
                message = f"{player.name} folds"
                self.players.remove(player)
            elif action == 'bet' and bet_amount > 0:
                self.pot += player.bet_chips(bet_amount)
                self.current_bet = bet_amount
                message = f"{player.name} bets: {bet_amount} chips"
            elif action == 'raise' and bet_amount > 0:
                self.pot += player.bet_chips(bet_amount)
                self.current_bet += bet_amount
                message = f"{player.name} raises: {bet_amount} chips"
            elif action == 'call':
                self.pot += player.bet_chips(self.current_bet)
                message = f"{player.name} calls: {self.current_bet} chips"
            elif action == 'check':
                message = f"{player.name} checks"
            self.players_actions.append((player.name, action, bet_amount))

            all_cards = self.combine_hands(player.cards)
            player_hand_strength = self.poker_rules.calculate_hand_ranking(all_cards)
            print(f"Player {player.name}'s hand strength: {player_hand_strength}")

        self.turn_manager.next_turn()  # Avanza al turno successivo
        return message

    def execute_phase(self):
        current_player = self.turn_manager.get_current_player()
        if isinstance(current_player, Bot):
            action, bet_amount = current_player.make_decision(self.generate_game_state_response(), self.phase)
            self.execute_turn(current_player, action, bet_amount)
        self.turn_manager.next_turn()  # Move to the next turn, whether it's a Bot or a Human

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
        all_cards = []
        for card in player_cards + self.community_cards:
            if isinstance(card, dict):
                all_cards.append(Card(card['value'], card['suit']))
            else:
                all_cards.append(card)
        return all_cards

    def start_game(self):
        while self.phase != Game.SHOWDOWN:
            self.execute_phase()
            self.check_phase_end()
        winner = self.get_winner()
        print(winner)

    def check_phase_end(self):
        if self.turn_manager.current_turn == 0:  # Avanza la fase dopo il turno del big blind
            self.next_phase()

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
        print(f"Starting player: {starting_player.name}")
        self.current_turn = starting_player.name
        return self.current_turn

    def assign_blinds(self):
        players = self.players[:]
        random.shuffle(players)
        self.blinds_info['small_blind'] = players[0].name
        self.blinds_info['big_blind'] = players[1].name
        return self.blinds_info

    def generate_game_state_response(self):
        try:
            player_index = next(i for i, p in enumerate(self.players) if p.name == 'player')
            player_hand = self.format_hand(self.players[player_index].cards)
        except StopIteration:
            player_hand = []  # Gestisce il caso in cui non esista un giocatore con il nome 'player'

        dealer_hand = self.format_hand(self.dealer.cards) if self.phase == Game.SHOWDOWN else [{'value': 'back', 'suit': 'card_back'}] * 2
        community_cards = self.format_hand(self.community_cards)
        deck_card = {'value': 'back', 'suit': 'card_back'}
        winner = self.get_winner() if self.phase == Game.SHOWDOWN else None

        blinds_info = {}
        blinds_messages = []

        if len(self.players) > 1:
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
            'current_turn': self.players[self.turn_manager.current_turn].name,
            'pot': self.pot,
            'current_bet': self.current_bet,
            'players': self.players
        }

    def format_hand(self, cards):
        return [{'value': card.value, 'suit': card.suit} for card in cards]

if __name__ == "__main__":
    game = Game(num_players=4)
    game.setup_players()
    game.start_game()
    response = game.generate_game_state_response()
    print(response)