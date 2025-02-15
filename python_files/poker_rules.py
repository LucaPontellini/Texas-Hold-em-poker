from itertools import combinations
class PokerRules:
    def __init__(self):
        self.hand_rankings = self.define_hand_rankings()

    # Definisce le classifiche delle mani nel Texas Hold'em Poker
    def define_hand_rankings(self):
        return {
            'royal_flush': 10,  # Scala reale (Royal Flush)
            'straight_flush': 9,  # Scala colore (Straight Flush)
            'four_of_a_kind': 8,  # Poker (Four of a Kind)
            'full_house': 7,  # Full (Full House)
            'flush': 6,  # Colore (Flush)
            'straight': 5,  # Scala (Straight)
            'three_of_a_kind': 4,  # Tris (Three of a Kind)
            'two_pairs': 3,  # Doppia coppia (Two Pairs)
            'pair': 2,  # Coppia (Pair)
            'high_card': 1  # Carta alta (High Card)
        }

    # Estrae i valori delle carte
    def extract_values(self, hand):
        values = []
        for card in hand:
            if isinstance(card, dict):
                values.append(card['value'])
            else:
                values.append(card.value)
        return values

    # Estrae i semi delle carte
    def extract_suits(self, hand):
        suits = []
        for card in hand:
            if isinstance(card, dict):
                suits.append(card['suit'])
            else:
                suits.append(card.suit)
        return suits

    # Verifica se la mano è una scala reale (Royal Flush)
    def royal_flush(self, hand):
        card_values = ['10', 'J', 'Q', 'K', 'A']
        return self.straight_flush(hand) and all(card.value in card_values for card in hand) and len(set(self.extract_suits(hand))) == 1

    # Verifica se la mano è una scala colore (Straight Flush)
    def straight_flush(self, hand):
        return self.straight(hand) and self.flush(hand)
    
    # Verifica se la mano è un poker (Four of a Kind)
    def four_of_a_kind(self, hand):
        values = self.extract_values(hand)
        return any(values.count(value) == 4 for value in values)
    
    # Verifica se la mano è un full (Full House)
    def full_house(self, hand):
        values = self.extract_values(hand)
        three_of_a_kind = self.three_of_a_kind(hand)
        two_of_a_kind = any(values.count(value) == 2 for value in values)
        return three_of_a_kind and two_of_a_kind
    
    # Verifica se la mano è un colore (Flush)
    def flush(self, hand):
        suits = self.extract_suits(hand)
        return len(set(suits)) == 1
    
    # Verifica se la mano è una scala (Straight)
    def straight(self, hand):
        card_values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
        indices = [card_values[value] for value in self.extract_values(hand)]
        indices = sorted(set(indices))
    
        if len(indices) < 5:
            return False
    
        for i in range(len(indices) - 4):
            if indices[i:i + 5] == list(range(indices[i], indices[i] + 5)):
                return True
    
        return indices[-5:] == [2, 3, 4, 5, 14]  # Caso speciale: l'Asso può essere basso in una scala (A, 2, 3, 4, 5)

    # Verifica se la mano è un tris (Three of a Kind)
    def three_of_a_kind(self, hand):
        values = self.extract_values(hand)
        return any(values.count(value) == 3 for value in values)

    # Verifica se la mano è una doppia coppia (Two Pairs)
    def two_pairs(self, hand):
        values = self.extract_values(hand)
        pairs = [value for value in set(values) if values.count(value) == 2]
        return len(pairs) == 2

    # Verifica se la mano è una coppia (Pair)
    def pair(self, hand):
        values = self.extract_values(hand)
        return any(values.count(value) == 2 for value in values)
    
    # Verifica se la mano è una carta alta (High Card)
    def high_card(self, hand):
        return True

    # Calcola il punteggio di una mano
    def calculate_hand_ranking(self, hand):
        if self.royal_flush(hand):
            return self.hand_rankings['royal_flush']
        elif self.straight_flush(hand):
            return self.hand_rankings['straight_flush']
        elif self.four_of_a_kind(hand):
            return self.hand_rankings['four_of_a_kind']
        elif self.full_house(hand):
            return self.hand_rankings['full_house']
        elif self.flush(hand):
            return self.hand_rankings['flush']
        elif self.straight(hand):
            return self.hand_rankings['straight']
        elif self.three_of_a_kind(hand):
            return self.hand_rankings['three_of_a_kind']
        elif self.two_pairs(hand):
            return self.hand_rankings['two_pairs']
        elif self.pair(hand):
            return self.hand_rankings['pair']
        else:
            return self.hand_rankings['high_card']

    # Determina il vincitore tra due mani di giocatori
    def determine_winner(self, player_hand, opponent_hand, community_cards, player_name="Giocatore", opponent_name="Bot1"):
        player_best_hand = self.get_best_hand(player_hand + community_cards)
        opponent_best_hand = self.get_best_hand(opponent_hand + community_cards)
        player_ranking = self.calculate_hand_ranking(player_best_hand)
        opponent_ranking = self.calculate_hand_ranking(opponent_best_hand)
        
        result = self.compare_hand_rankings(player_ranking, opponent_ranking)
        player_hand_name = self.hand_name(player_best_hand)
        opponent_hand_name = self.hand_name(opponent_best_hand)
        
        if result == "win":
            return f"{player_name} wins with {player_hand_name} worth {player_ranking} points against {opponent_name}'s {opponent_hand_name} worth {opponent_ranking} points!"
        elif result == "lose":
            return f"{opponent_name} wins with {opponent_hand_name} worth {opponent_ranking} points against {player_name}'s {player_hand_name} worth {player_ranking} points!"
        else:
            return f"It's a tie! Both {player_name} and {opponent_name} have {player_hand_name} worth {player_ranking} points."

    # Ottiene la migliore mano tra le carte fornite
    def get_best_hand(self, cards):
        best_hand = None
        highest_ranking = 0
        all_combinations = list(combinations(cards, 5))

        for hand in all_combinations:
            hand_ranking = self.calculate_hand_ranking(hand)
            if hand_ranking > highest_ranking:
                highest_ranking = hand_ranking
                best_hand = hand

        return best_hand

    # Calcola il punteggio di una mano
    def calculate_hand_ranking(self, hand):
        for ranking, points in self.hand_rankings.items():
            if getattr(self, ranking)(hand):
                return points
        return self.hand_rankings['high_card']

    # Confronta i punteggi di due mani
    def compare_hand_rankings(self, player_ranking, opponent_ranking):
        if player_ranking > opponent_ranking:
            return "win"
        elif opponent_ranking > player_ranking:
            return "lose"
        else:
            return "tie"

    # Ottiene il nome della combinazione di una mano
    def hand_name(self, hand):
        for ranking in self.hand_rankings.keys():
            if getattr(self, ranking)(hand):
                return ranking.replace('_', ' ').title()
        return "High Card"
    
    # Fornisce una spiegazione della combinazione di una mano
    def get_hand_explanation(self, hand):
        if self.royal_flush(hand):
            return ("Hand: Royal Flush\n"
                    "The highest straight flush, consisting of the ace, king, queen, jack and ten all of the same suit.\n"
                    "Worth 10 points.")
        elif self.straight_flush(hand):
            return ("Hand: Straight Flush\n"
                    "Five consecutive cards of the same suit.\n"
                    "Worth 9 points.")
        elif self.four_of_a_kind(hand):
            return ("Hand: Four of a Kind\n"
                    "Four cards of the same rank.\n"
                    "Worth 8 points.")
        elif self.full_house(hand):
            return ("Hand: Full House\n"
                    "Three of a kind combined with a pair.\n"
                    "Worth 7 points.")
        elif self.flush(hand):
            return ("Hand: Flush\n"
                    "Five cards of the same suit, not in sequence.\n"
                    "Worth 6 points.")
        elif self.straight(hand):
            return ("Hand: Straight\n"
                    "Five consecutive cards of different suits.\n"
                    "Worth 5 points.")
        elif self.three_of_a_kind(hand):
            return ("Hand: Three of a Kind\n"
                    "Three cards of the same rank.\n"
                    "Worth 4 points.")
        elif self.two_pairs(hand):
            return ("Hand: Two Pairs\n"
                    "Two different pairs.\n"
                    "Worth 3 points.")
        elif self.pair(hand):
            return ("Hand: Pair\n"
                    "Two cards of the same rank.\n"
                    "Worth 2 points.")
        else:
            return ("Hand: High Card\n"
                    "None of the above combinations.\n"
                    "Worth 1 point.")