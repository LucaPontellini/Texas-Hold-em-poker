import random
from venv import logger
import requests

from .players import BotType, Player, Dealer, Bot, BettingRound
from .deck import Deck, Card
from .poker_rules import PokerRules

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
        print(f"Advancing to the next turn: {self.players[self.current_turn].name}'s turn")
        return self.get_current_player()

    def get_current_player(self):
        return self.players[self.current_turn]

    def send_turn_to_flask(self):
        current_player = self.get_current_player()
        data = {'current_turn': current_player.name}
        print(f"Sending turn to Flask: {data}")  # Aggiungi un log per il debug
        try:
            response = requests.post('http://localhost:5000/advance-turn', json=data)
            if response.status_code == 200:
                print("Turn information sent successfully")
            else:
                print(f"Failed to send turn information: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Error sending turn information: {e}")

class Game:
    PRE_FLOP = 'pre-flop'
    FLOP = 'flop'
    TURN = 'turn'
    RIVER = 'river'
    SHOWDOWN = 'showdown'

    VALID_ACTIONS = ['check', 'call', 'bet', 'raise', 'fold']

    def __init__(self):
        num_players = random.randint(2, 10)
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
        self.rotate_blinds()
        small_blind_player = self.players[0]
        big_blind_player = self.players[1]
        small_blind_player.name = 'small_blind'
        big_blind_player.name = 'big_blind'
        self.pot += small_blind_player.bet_chips(self.small_blind)
        self.pot += big_blind_player.bet_chips(self.big_blind)
        print(f"{small_blind_player.name} posts small blind: {self.small_blind} chips")
        print(f"{big_blind_player.name} posts big blind: {self.big_blind} chips")

    def rotate_blinds(self):
        self.players.append(self.players.pop(0))

    def deal_hole_cards(self):
        for player in self.players:
            player.cards = self.deck[:2]
            self.deck = self.deck[2:]
        print(f"Deck after dealing hole cards: {len(self.deck)}")

    def move_to_flop(self):
        self.phase = Game.FLOP
        self.turn_manager.current_turn = self.turn_manager.find_big_blind()
        self.deal_flop()
        print("Moving to the Flop phase")  # Log di debug per monitorare il passaggio di fase

    def deal_flop(self):
        self.community_cards = self.deck[:3]
        self.deck = self.deck[3:]
        print("Dealt Flop: ", self.community_cards)  # Log di debug per le carte comuni

    def move_to_turn(self):
        self.phase = Game.TURN
        self.turn_manager.current_turn = self.turn_manager.find_big_blind()
        self.deal_turn_card()
        print("Moving to the Turn phase")  # Log di debug per monitorare il passaggio di fase

    def deal_turn_card(self):
        self.community_cards.append(self.deck.pop(0))
        print("Dealt Turn Card: ", self.community_cards[-1])  # Log di debug per la quarta carta comune

    def move_to_river(self):
        self.phase = Game.RIVER
        self.turn_manager.current_turn = self.turn_manager.find_big_blind()
        self.deal_river_card()
        print("Moving to the River phase")  # Log di debug per monitorare il passaggio di fase

    def deal_river_card(self):
        self.community_cards.append(self.deck.pop(0))
        print("Dealt River Card: ", self.community_cards[-1])  # Log di debug per la quinta carta comune

    def move_to_showdown(self):
        self.phase = Game.SHOWDOWN
        self.evaluate_hands()
        print("Moving to the Showdown phase")  # Log di debug per monitorare il passaggio di fase

    def execute_phase(self):
        current_player = self.turn_manager.get_current_player()
        current_player_name = current_player.name if not isinstance(current_player, dict) else current_player['name']

        print(f"Executing phase for player: {current_player_name}")

        if isinstance(current_player, Bot):
            action, bet_amount = current_player.make_decision(self.generate_game_state_response(), self.phase)
            print(f"Bot {current_player_name}: decision={action}, bet_amount={bet_amount}")
            self.execute_turn(current_player, action, bet_amount)
        else:
            print(f"Player {current_player_name} is making a decision.")
            self.turn_manager.send_turn_to_flask()

        if self.check_phase_end():
            self.next_phase()  # Passa alla fase successiva se la fase corrente è finita

        self.turn_manager.next_turn()
        print(f"New turn: {self.turn_manager.current_turn}")
        self.update_client_state()  # Invia lo stato del gioco al client

    def start_game(self):
        while self.phase != Game.SHOWDOWN:
            self.execute_phase()
            if self.check_phase_end():
                self.next_phase()
        winner = self.get_winner()
        print(winner)

    def update_client_state(self):
        response = self.generate_game_state_response()
        try:
            logger.info("Updating client state: %s", response)  # Log per il debug
            requests.post('http://localhost:5000/update-state', json=response)
        except requests.exceptions.RequestException as e:
            logger.error(f"Error updating client state: {e}")

    def execute_turn(self, player, action, bet_amount=0):
        print("Executing turn:", player.name, "-> action:", action, "bet amount:", bet_amount)  # Debugging

        if action in ['string bet', 'angle shooting', 'collusion']:
            print(f"Invalid action: {action} by {player['name']}")
            return

        player_name = player['name'] if isinstance(player, dict) else player.name
        print(f"Executing turn: {player_name} -> action: {action}, bet amount: {bet_amount}")

        if action in Game.VALID_ACTIONS:
            player_obj = next((p for p in self.players if p.name == player_name), None)
            if player_obj:
                player_obj.set_has_acted()

            if action == 'fold':
                message = f"{player_name} folds"
                if player_obj:
                    self.players.remove(player_obj)

            elif action == 'bet' and bet_amount > 0:
                if player_obj:
                    self.pot += player_obj.bet_chips(bet_amount)
                    self.current_bet = bet_amount
                    message = f"{player_name} bets: {bet_amount} chips"

            elif action == 'raise' and bet_amount > 0:
                if player_obj:
                    raise_amount = bet_amount - self.current_bet
                    self.pot += player_obj.bet_chips(raise_amount)
                    self.current_bet += raise_amount
                    message = f"{player_name} raises: {raise_amount} chips"

            elif action == 'call':
                if player_obj:
                    self.pot += player_obj.bet_chips(self.current_bet - player_obj.current_bet)
                    player_obj.current_bet = self.current_bet
                    message = f"{player_name} calls: {self.current_bet} chips"

            elif action == 'check':
                message = f"{player_name} checks"

            self.players_actions.append((player_name, action, bet_amount))

            if player_obj:
                all_cards = self.combine_hands(player_obj.cards)
                player_hand_strength = self.poker_rules.calculate_hand_ranking(all_cards)
                print(f"Player {player_name}'s hand strength: {player_hand_strength}")

        print(f"Turn completed: {player_name} -> action: {action}, pot: {self.pot}, current_bet: {self.current_bet}")

        if self.check_phase_end():  # Verifica se la fase è finita dopo il turno
            self.next_phase()       # Passa alla fase successiva se la fase corrente è finita

        self.turn_manager.next_turn()  # Avanza al turno successivo
        print(f"New turn: {self.turn_manager.current_turn}")
        return message

    def check_phase_end(self):
        print("Checking if all players have acted:")
        for player in self.players:
            print(f"Player {player.name} has_acted: {player.has_acted}")

        if len(self.players) == 1:  # Se rimane solo un giocatore, vince automaticamente
            print(f"Only one player remaining: {self.players[0].name}")
            self.phase = Game.SHOWDOWN
            return True

        if self.all_players_acted():
            print("All players have acted. Moving to the next phase.")
            return True
        else:
            print("Not all players have acted yet.")
            return False

    def all_players_acted(self):
        result = all(player.has_acted for player in self.players)
        print(f"all_players_acted: {result} (Players: {[player.name for player in self.players]})")  # Log di debug
        for player in self.players:
            print(f"{player.name} has_acted: {player.has_acted}")
        return result

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
            if self.check_phase_end():
                self.next_phase()
        winner = self.get_winner()
        print(winner)

    def next_phase(self):
        if self.phase == Game.PRE_FLOP:
            self.move_to_flop()
        elif self.phase == Game.FLOP:
            self.move_to_turn()
        elif self.phase == Game.TURN:
            self.move_to_river()
        elif self.phase == Game.RIVER:
            self.move_to_showdown()

        # Reset dello stato has_acted di tutti i giocatori dopo ogni fase
        for player in self.players:
            player.reset_has_acted()

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
    
    def get_bot_actions(self):
        bot_actions = []
        for player in self.players:
            if isinstance(player, Bot):
                bot_actions.extend(player.get_actions())
        return bot_actions

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

        players_info = [
            {
                'name': player.name,
                'chips': player.chips,
                'aggressiveness': getattr(player, 'aggressiveness', None)
            } for player in self.players
        ]

        bot_actions = self.get_bot_actions()  # Assicurati di avere una funzione che raccoglie le azioni dei bot

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
            'players': players_info,
            'bot_actions': bot_actions
        }

    def format_hand(self, cards):
        return [{'value': card.value, 'suit': card.suit} for card in cards]

if __name__ == "__main__":
    game = Game()
    game.setup_players()
    game.start_game()
    response = game.generate_game_state_response()
    print(response)