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

    def distribute_cards(self, deck):
        player_cards = deck[:2]
        opponent_cards = deck[2:4]
        return player_cards, opponent_cards

    def pair(self, hand):
        values = [card.value for card in hand]
        return any(values.count(value) == 2 for value in values)

    def two_pairs(self, hand):
        values = [card.value for card in hand]
        pairs = [value for value in values if values.count(value) == 2]
        return len(set(pairs)) == 2

    def three_of_a_kind(self, hand):
        values = [card.value for card in hand]
        return any(values.count(value) == 3 for value in values)

    def straight(self, hand):
        card_values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        values = sorted(card_values.index(card.value) for card in hand)
        return all(values[i] - values[i-1] == 1 for i in range(1, len(values))) or \
               (values[-1] == 12 and all(values[i] - values[i-1] == 1 for i in range(1, len(values)-1)))

    def flush(self, hand):
        suits = [card.suit for card in hand]
        return len(set(suits)) == 1

    def full_house(self, hand):
        return self.three_of_a_kind(hand) and self.pair(hand)

    def four_of_a_kind(self, hand):
        values = [card.value for card in hand]
        return any(values.count(value) == 4 for value in values)

    def straight_flush(self, hand):
        return self.straight(hand) and self.flush(hand)

    def determine_winner(self, player_hand, opponent_hand):
        player_ranking = max((ranking for check_hand, ranking in self.hand_rankings.items() if check_hand(player_hand)), default=1)
        opponent_ranking = max((ranking for check_hand, ranking in self.hand_rankings.items() if check_hand(opponent_hand)), default=1)

        if player_ranking > opponent_ranking:
            return "Player wins!"
        elif opponent_ranking > player_ranking:
            return "Dealer wins!"
        else:
            return "It's a tie!"