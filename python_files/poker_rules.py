import random
from deck import Deck

# Regole del Texas Hold'em Poker:

# 1. Setup del Gioco:
#    - Ogni giocatore riceve due carte coperte (hole cards).
#    - Cinque carte comuni vengono distribuite sul tavolo in tre fasi: il flop (tre carte), il turn (una carta) e il river (una carta).

# 2. Turni di Puntata:
#    - Pre-Flop: I giocatori ricevono le loro due carte coperte e iniziano il primo turno di puntata.
#    - Flop: Vengono distribuite tre carte comuni sul tavolo, seguite da un secondo turno di puntata.
#    - Turn: Viene distribuita una quarta carta comune, seguita da un terzo turno di puntata.
#    - River: Viene distribuita una quinta carta comune, seguita dall'ultimo turno di puntata.

# 3. Azioni di Puntata:
#    - Check: Passare il turno senza scommettere.
#    - Bet: Scommettere una certa quantità di chip.
#    - Call: Pareggiare la scommessa di un altro giocatore.
#    - Raise: Aumentare la scommessa.
#    - Fold: Abbandonare la mano.

# 4. Valutazione delle Mani:
#    - Coppia: Due carte dello stesso valore.
#    - Doppia Coppia: Due coppie di carte.
#    - Tris: Tre carte dello stesso valore.
#    - Scala: Cinque carte consecutive (ad esempio, 2-3-4-5-6).
#    - Colore: Cinque carte dello stesso seme.
#    - Full: Una coppia più un tris.
#    - Poker: Quattro carte dello stesso valore.
#    - Scala Colore: Scala dello stesso seme.
#    - Scala Reale: Scala dall'asso al dieci dello stesso seme.

# 5. Showdown:
#    - Dopo l'ultimo turno di puntata, i giocatori rimanenti mostrano le loro carte.
#    - Il giocatore con la migliore mano di cinque carte vince il piatto.

class PokerRules:
    def __init__(self):
        self.hand_rankings = {
            self.straight_flush: 9,
            self.four_of_a_kind: 8,
            self.full_house: 7,
            self.flush: 6,
            self.straight: 5,
            self.three_of_a_kind: 4,
            self.two_pairs: 3,
            self.pair: 2
        }

# Punti delle Mani nel Texas Hold'em Poker:
#    - Scala Colore (Straight Flush): 9 punti
#    - Poker (Four of a Kind): 8 punti
#    - Full (Full House): 7 punti
#    - Colore (Flush): 6 punti
#    - Scala (Straight): 5 punti
#    - Tris (Three of a Kind): 4 punti
#    - Doppia Coppia (Two Pairs): 3 punti
#    - Coppia (Pair): 2 punti

    def pair(self, hand):

        """Controlla se una mano ha una coppia"""
        
        values = [card['value'] for card in hand]
        return any(values.count(value) == 2 for value in values)

    def two_pairs(self, hand):

        """Controlla se una mano ha due coppie diverse"""

        values = [card['value'] for card in hand]
        pairs = [value for value in values if values.count(value) == 2]
        return len(set(pairs)) == 2

    def three_of_a_kind(self, hand):

        """Controlla se una mano ha un tris"""

        values = [card['value'] for card in hand]
        return any(values.count(value) == 3 for value in values)

    def straight(self, hand):

        """Controlla se una mano ha una scala"""

        card_values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        values = sorted(card_values.index(card['value']) for card in hand)
        return all(values[i] - values[i-1] == 1 for i in range(1, len(values))) or \
               (values[-1] == 12 and all(values[i] - values[i-1] == 1 for i in range(1, len(values)-1)))

    def flush(self, hand):

        """Controlla se una mano ha un colore"""

        suits = [card['seed'] for card in hand]
        return len(set(suits)) == 1

    def full_house(self, hand):

        """Controlla se una mano ha un full"""

        return self.three_of_a_kind(hand) and self.pair(hand)

    def four_of_a_kind(self, hand):

        """Controlla se una mano ha un poker"""

        values = [card['value'] for card in hand]
        return any(values.count(value) == 4 for value in values)

    def straight_flush(self, hand):

        """Controlla se una mano ha una scala colore"""

        return self.straight(hand) and self.flush(hand)

    def distribute_cards(self, deck):

        """Distribuisce due carte coperte a ciascun giocatore"""

        player_hand = [deck.pop(), deck.pop()]
        dealer_hand = [deck.pop(), deck.pop()]
        return player_hand, dealer_hand

    def check(self):

        """Questa funzione rappresenta l'azione 'check' nel poker"""

        print("Player checks.")
        pass

    def bet(self, chips):

        """Questa funzione rappresenta l'azione 'bet' nel poker"""

        print(f"Player bets {chips} chips.")
        return chips

    def call(self, amount):

        """Questa funzione rappresenta l'azione 'call' nel poker"""

        print(f"Player calls with {amount}.")
        return amount

    def raise_bet(self, initial_amount, raise_amount):

        """Questa funzione rappresenta l'azione 'raise' nel poker"""

        print(f"Player raises. The bet increases from {initial_amount} to {initial_amount + raise_amount}.")
        return initial_amount + raise_amount

    def fold(self):

        """Questa funzione rappresenta l'azione 'fold' nel poker"""

        print("Player folds.")
        pass

    def flop(self, deck):

        """Distribuisce il flop"""

        return [deck.pop(), deck.pop(), deck.pop()]

    def turn(self, deck):

        """Distribuisce la carta del turn"""

        return deck.pop()

    def river(self, deck):

        """Distribuisce la carta del river"""

        return deck.pop()

    def show_cards(self, player_hand, dealer_hand):

        """Mostra tutte le carte"""

        print("Player's cards: ", player_hand)
        print("Dealer's cards: ", dealer_hand)

    def determine_winner(self, player_hand, dealer_hand):

        """Determina il vincitore"""

        player_ranking = max((ranking for check_hand, ranking in self.hand_rankings.items() if check_hand(player_hand)), default=1)
        dealer_ranking = max((ranking for check_hand, ranking in self.hand_rankings.items() if check_hand(dealer_hand)), default=1)

        if player_ranking > dealer_ranking:
            return "Player wins!"
        elif dealer_ranking > player_ranking:
            return "Dealer wins!"
        else:
            return "It's a tie!"