"""
Questo file contiene una suite di test unitaria per verificare le funzionalità principali del gioco di Texas Hold'em Poker. 
I test coprono diverse aree, tra cui:

- Creazione e gestione del mazzo di carte (`Deck`).
- Funzionalità del singolo giocatore (`Player`).
- Decisioni del bot giocatore (`Bot`).
- Regole del poker (`PokerRules`).
- Gestione dei turni (`TurnManager`).
- Fasi del gioco (`Game`).

La suite di test utilizza il framework `unittest` per eseguire i test e verificare che tutte le componenti del gioco funzionino correttamente.
"""

import sys
import os
import unittest
from pathlib import Path

# Aggiunge il percorso principale del progetto al percorso di ricerca dei moduli
sys.path.append(str(Path(__file__).resolve().parents[1]))

from python_files.deck import Card, Deck
from python_files.players import Player, Bot, BotType, Dealer, BettingRound
from python_files.poker_rules import PokerRules
from python_files.game import TurnManager, Game

class TestGameFunctions(unittest.TestCase):

    def setUp(self):
        self.game = Game()
        self.game.setup_players()

    def test_initial_setup(self):
        self.assertGreaterEqual(len(self.game.players), 2)  # Verifica che ci siano almeno 2 giocatori
        self.assertLessEqual(len(self.game.players), 10)    # Verifica che ci siano al massimo 10 giocatori
        self.assertTrue(all(isinstance(player, (Player, Bot)) for player in self.game.players))

    def test_deck_creation(self):
        deck = Deck("deck.json")
        self.assertEqual(len(deck.deck_data), 52)

    def test_card_creation(self):
        card = Card("Hearts", "A")
        self.assertEqual(card.suit, "Hearts")
        self.assertEqual(card.value, "A")

    def test_shuffle_deck(self):
        deck = Deck("deck.json")
        original_deck = deck.deck_data.copy()
        deck.shuffle()
        self.assertNotEqual(deck.deck_data, original_deck)
        self.assertEqual(set(map(str, deck.deck_data)), set(map(str, original_deck)))

    def test_draw_card(self):
        deck = Deck("deck.json")
        initial_size = len(deck.deck_data)
        card = deck.draw_card()
        self.assertIsNotNone(card)
        self.assertEqual(len(deck.deck_data), initial_size - 1)

    def test_add_remove_card(self):
        player = Player("Giocatore")
        card = Card("Hearts", "A")
        player.add_card(card)
        self.assertTrue(player.has_card(card))
        player.remove_card(card)
        self.assertFalse(player.has_card(card))

    def test_bot_decision(self):
        bot = Bot("Bot1", BotType.AGGRESSIVE)
        game_state = {
            'community_cards': [Card("Hearts", "2"), Card("Clubs", "5"), Card("Diamonds", "10")],
            'current_bet': 100,
            'pot': 500,
            'players': [bot],
            'dealer_index': 0  # Assicurati che questa chiave sia presente
        }
        decision, bet_amount = bot.make_decision(game_state, BettingRound.PRE_FLOP)
        self.assertIn(decision, ['fold', 'call', 'raise'])


    def test_poker_hand_ranking(self):
        rules = PokerRules()
        hand = [Card("Hearts", "10"), Card("Hearts", "J"), Card("Hearts", "Q"), Card("Hearts", "K"), Card("Hearts", "A")]
        self.assertTrue(rules.royal_flush(hand))

    def test_turn_manager(self):
        players = [Player('small_blind'), Player('big_blind'), Player('player1'), Player('player2')]
        turn_manager = TurnManager(players)
        self.assertEqual(turn_manager.current_turn, 2)

    def test_game_phases(self):
        self.game.setup_players()
        self.game.move_to_flop()
        self.assertEqual(len(self.game.community_cards), 3)
        self.game.move_to_turn()
        self.assertEqual(len(self.game.community_cards), 4)
        self.game.move_to_river()
        self.assertEqual(len(self.game.community_cards), 5)
        self.assertEqual(self.game.phase, 'river')
        self.game.move_to_showdown()
        self.assertEqual(self.game.phase, 'showdown')

if __name__ == '__main__':
    unittest.main()