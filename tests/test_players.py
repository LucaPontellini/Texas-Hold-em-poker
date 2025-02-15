import pytest
import sys
import random
from pathlib import Path

# Aggiunge il percorso principale del progetto al percorso di ricerca dei moduli
sys.path.append(str(Path(__file__).resolve().parents[1]))

from python_files.players import Player, Bot, BotType, BettingRound, Dealer
from python_files.deck import Deck, Card
from python_files.poker_rules import PokerRules

def test_deck_initialization():
    deck = Deck()
    assert len(deck.deck_data) == 52, "Il mazzo dovrebbe contenere 52 carte."

def test_dealer_shuffle_deck():
    deck = Deck()
    dealer = Dealer(deck=deck)
    initial_deck = deck.deck_data.copy()
    dealer.shuffle_deck()
    assert initial_deck != deck.deck_data, "Il mazzo dovrebbe essere mescolato."

def test_dealer_deal_hole_cards():
    deck = Deck()
    dealer = Dealer(deck=deck)
    players = [Player("Player1"), Player("Player2")]
    dealer.deal_hole_cards(players)
    for player in players:
        assert len(player.cards) == 2, f"{player.name} dovrebbe avere 2 carte."

def test_dealer_deal_community_cards():
    deck = Deck()
    dealer = Dealer(deck=deck)
    game_state = {'community_cards': []}
    dealer.deal_community_cards(game_state, 3)
    assert len(game_state['community_cards']) == 3, "Dovrebbero esserci 3 carte comunitarie."

def test_player_evaluate_hand():
    player = Player("Player1")
    player.add_card(Card("Hearts", "10"))
    player.add_card(Card("Hearts", "J"))
    community_cards = [Card("Hearts", "Q"), Card("Hearts", "K"), Card("Hearts", "A")]
    player.poker_rules = PokerRules()
    assert player.evaluate_hand(community_cards) == 10, "Il giocatore dovrebbe avere una scala reale."

def test_bot_make_decision():
    deck = Deck()
    bot = Bot("Bot1", BotType.AGGRESSIVE)
    bot.add_card(Card("Hearts", "10"))
    bot.add_card(Card("Hearts", "J"))
    game_state = {
        'players': [bot],
        'community_cards': [Card("Hearts", "Q"), Card("Hearts", "K"), Card("Hearts", "A")],
        'current_bet': 10,
        'pot': 50,
        'dealer_index': 0
    }
    decision, bet_amount = bot.make_decision(game_state, BettingRound.PRE_FLOP)
    assert decision in ["raise", "bet"], "Il bot aggressivo dovrebbe rilanciare o scommettere."
    assert bet_amount > 0, "L'importo della puntata dovrebbe essere maggiore di 0."

def test_gameplay():
    # Creazione del mazzo di carte
    deck = Deck()
    dealer = Dealer(deck=deck)  # Creazione del dealer con il mazzo

    # Creazione del giocatore umano
    human_player = Player("TestPlayer")

    # Creazione dei bot
    bot1 = Bot("Bot1 (Aggressive)", BotType.AGGRESSIVE)
    bot2 = Bot("Bot2 (Conservative)", BotType.CONSERVATIVE)
    bot3 = Bot("Bot3 (Bluffer)", BotType.BLUFFER)
    bot4 = Bot("Bot4 (Tight)", BotType.TIGHT)
    bot5 = Bot("Bot5 (Loose)", BotType.LOOSE)
    bot6 = Bot("Bot6 (Passive)", BotType.PASSIVE)
    bot7 = Bot("Bot7 (Maniac)", BotType.MANIAC)
    bot8 = Bot("Bot8 (Calling Station)", BotType.CALLING_STATION)

    # Lista di tutti i giocatori
    players = [human_player, bot1, bot2, bot3, bot4, bot5, bot6, bot7, bot8]

    # Assegnazione del dealer (che non gioca)
    dealer_index = random.randint(0, len(players) - 1)
    game_state = {
        'players': players,
        'dealer_index': dealer_index,
        'community_cards': [],
        'current_bet': 0,
        'pot': 0
    }

    # Mescola il mazzo
    dealer.shuffle_deck()
    
    # Distribuzione delle carte ai giocatori
    dealer.deal_hole_cards(players)

    # Inizio della partita
    for round_number in range(1, 5):
        betting_round = BettingRound(round_number)

        for player in players[:]:  # Usa una copia della lista per evitare modifiche durante l'iterazione
            if player == human_player:
                action = "check"  # Scegliamo un'azione di test
                bet_amount = 0
                if action in ['bet', 'raise']:
                    bet_amount = player.bet_chips(10)  # Scommettiamo 10 fiches per il test
                elif action == 'call':
                    if game_state['current_bet'] > player.current_bet:
                        bet_amount = game_state['current_bet'] - player.current_bet
                        player.bet_chips(bet_amount)
                    else:
                        action = 'check'
                        bet_amount = 0
                elif action == 'check':
                    bet_amount = 0
                elif action == 'fold':
                    bet_amount = 0
                    players.remove(player)
                decision = action
                player.set_has_acted()
            else:
                decision, bet_amount = player.make_decision(game_state, betting_round)
                if decision in ['bet', 'raise']:
                    player.bet_chips(bet_amount)
                player.set_has_acted()

            game_state['pot'] += player.current_bet
            player.current_bet = 0
            player.reset_has_acted()

        # Distribuzione delle carte comunitarie in base al round di puntata
        if round_number == 2:  # FLOP
            dealer.deal_community_cards(game_state, 3)
        elif round_number == 3:  # TURN
            dealer.deal_community_cards(game_state, 1)
        elif round_number == 4:  # RIVER
            dealer.deal_community_cards(game_state, 1)

    # Fine della partita - determinazione del vincitore e distribuzione delle vincite
    winner = dealer.determine_winner(players, game_state)
    dealer.distribute_winnings(winner, game_state)

    # Verifica che ci sia un vincitore
    assert winner is not None, "Dovrebbe esserci un vincitore alla fine del gioco."
    assert winner.get_chips() > 0, "Il vincitore dovrebbe avere fiches."