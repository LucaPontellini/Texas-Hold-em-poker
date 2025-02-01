import random
from flask import request
from deck import Deck, Card
from player import Player, Bot, Dealer
from poker_rules import PokerRules

# Classe che rappresenta una partita di Texas Hold'em Poker
class Game:
    PRE_FLOP = 'pre-flop'
    FLOP = 'flop'
    TURN = 'turn'
    RIVER = 'river'
    SHOWDOWN = 'showdown'

    # Azioni valide durante il gioco
    VALID_ACTIONS = ['check', 'call', 'bet', 'raise', 'fold']

    def __init__(self, num_players=4):
        # Inizializzazione del mazzo di carte, dei giocatori, delle carte comuni e delle regole del poker
        self.deck = Deck('deck.json').deck_data
        self.dealer = Dealer("dealer")
        self.players = self.create_players(num_players)
        self.community_cards = []
        self.turn_count = 0
        self.phase = Game.PRE_FLOP
        self.poker_rules = PokerRules()
        self.pot = 0
        self.small_blind, self.big_blind = self.set_blinds()  # Randomizzazione dei blinds
        self.setup_players()

    # Creazione dei giocatori e dei bot con randomizzazione delle posizioni
    def create_players(self, num_players):
        players = [Player("player")]  # Aggiunge il giocatore umano
        bots = [Bot(f"Bot{i+1}") for i in range(num_players - 1)]  # Crea i bot
        all_players = players + bots
        random.shuffle(all_players)  # Randomizza la disposizione dei giocatori
        return all_players

    # Impostazione dei blinds con valori casuali
    def set_blinds(self):
        small_blind = random.randint(1, 5) * 5
        big_blind = small_blind * 2
        return small_blind, big_blind

    # Impostazione dei giocatori con i blinds
    def setup_players(self):
        self.deal_hole_cards()
        self.post_blinds()
        self.remove_dealt_cards_from_deck(2 * len(self.players))

    # Aggiunta della logica per i blinds
    def post_blinds(self):
        small_blind_player = self.players[0]
        big_blind_player = self.players[1]
        self.pot += small_blind_player.bet_chips(self.small_blind)
        self.pot += big_blind_player.bet_chips(self.big_blind)
        print(f"{small_blind_player.name} posts small blind: {self.small_blind} chips")
        print(f"{big_blind_player.name} posts big blind: {self.big_blind} chips")

    # Distribuisce le carte iniziali (hole cards) ai giocatori
    def deal_hole_cards(self):
        for player in self.players:
            player.cards = self.deck[:2]
            self.deck = self.deck[2:]

    # Rimuove le carte distribuite dal mazzo
    def remove_dealt_cards_from_deck(self, num_cards):
        self.deck = self.deck[num_cards:]

    # Passa alla fase successiva del gioco
    def next_phase(self):
        if self.phase == Game.PRE_FLOP:
            self.move_to_flop()
        elif self.phase == Game.FLOP:
            self.move_to_turn()
        elif self.phase == Game.TURN:
            self.move_to_river()
        elif self.phase == Game.RIVER:
            self.move_to_showdown()

    # Passa alla fase del flop e distribuisce le prime tre carte comuni
    def move_to_flop(self):
        self.phase = Game.FLOP
        self.deal_flop()

    # Distribuisce le prime tre carte comuni (flop)
    def deal_flop(self):
        self.community_cards = self.deck[:3]
        self.remove_dealt_cards_from_deck(3)  # Rimuove le 3 carte del flop

    # Passa alla fase del turn e distribuisce la quarta carta comune
    def move_to_turn(self):
        self.phase = Game.TURN
        self.deal_turn_card()

    # Distribuisce la quarta carta comune (turn)
    def deal_turn_card(self):
        self.community_cards.append(self.deck.pop(0))

    # Passa alla fase del river e distribuisce la quinta carta comune
    def move_to_river(self):
        self.phase = Game.RIVER
        self.deal_river_card()

    # Distribuisce la quinta carta comune (river)
    def deal_river_card(self):
        self.community_cards.append(self.deck.pop(0))

    # Passa alla fase dello showdown, dove le carte vengono rivelate
    def move_to_showdown(self):
        self.phase = Game.SHOWDOWN
        self.evaluate_hands()

    # Esegue il turno di ciascun giocatore o bot in senso orario
    def execute_turn(self, player, action, bet_amount=0):
        print(f"{player.name} executes action: {action} with bet amount: {bet_amount}")
        if action in Game.VALID_ACTIONS:
            if action == 'fold':
                print(f"{player.name} folds")
                return f'{player.name} folds'
            if action == 'bet' and bet_amount > 0:
                self.pot += player.bet_chips(bet_amount)
                print(f"{player.name} bets: {bet_amount} chips")
            self.next_phase()
        else:
            raise ValueError(f"Invalid action: {action}")

    # Esegue tutti i turni dei giocatori per la fase attuale
    def execute_phase(self):
        for player in self.players:
            if isinstance(player, Bot):
                action = player.make_decision({'community_cards': self.community_cards, 'players': self.players}, self.phase)
                self.execute_turn(player, action)
            else:
                # Gestisce le azioni del giocatore umano
                action = request.form.get("action")
                bet_amount = int(request.form.get("betAmount", 0))
                if action in Game.VALID_ACTIONS:
                    self.execute_turn(player, action, bet_amount)
        self.next_phase()

    # Metodo per valutare le mani dei giocatori alla fine del gioco
    def evaluate_hands(self):
        best_hands = {}
        for player in self.players:
            player_hand = self.combine_hands(player.cards)
            best_hands[player.name] = self.poker_rules.get_best_hand(player_hand)

        # Trova il giocatore con la mano migliore
        winner = max(best_hands, key=lambda name: self.poker_rules.calculate_hand_ranking(best_hands[name]))
        winner_hand = self.poker_rules.hand_name(best_hands[winner])
        print(f"{winner} wins with {winner_hand} and wins {self.pot} chips!")

    # Combina le carte del giocatore con le carte comuni per formare una mano
    def combine_hands(self, player_cards):
        return player_cards + self.community_cards

    # Metodo per iniziare il gioco
    def start_game(self):
        while self.phase != Game.SHOWDOWN:
            self.execute_phase()
        winner = self.get_winner()
        print(winner)

    # Metodo per determinare il vincitore del gioco
    def get_winner(self):
        best_hands = {}
        for player in self.players:
            player_hand = self.combine_hands(player.cards)
            best_hands[player.name] = self.poker_rules.get_best_hand(player_hand)

        # Trova il giocatore con la mano migliore
        winner = max(best_hands, key=lambda name: self.poker_rules.calculate_hand_ranking(best_hands[name]))
        winner_hand = self.poker_rules.hand_name(best_hands[winner])
        return f"{winner} wins with {winner_hand}!"