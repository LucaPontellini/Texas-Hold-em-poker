```mermaid

    classDiagram
    %% deck.py
    class Card {
        +__init__(self, seed: str, value: str): none
        +__repr__(self): str
        +__eq__(self, other: object): bool
    }

    class Deck {
        +__init__(self, deck_file_path): none
        +load_deck(self, deck_file_path): list[Card]
        +create_cards(self, deck): list[Card]
    }

    %% game.py
    class Game {
        +PRE_FLOP: str
        +FLOP: str
        +TURN: str
        +RIVER: str
        +SHOWDOWN: str
        +VALID_ACTIONS: list[str]
        +__init__(self): none
        +setup_players(self): none
        +deal_hole_cards(self): none
        +remove_dealt_cards_from_deck(self): none
        +next_phase(self): none
        +move_to_flop(self): none
        +deal_flop(self): none
        +move_to_turn(self): none
        +deal_turn_card(self): none
        +move_to_river(self): none
        +deal_river_card(self): none
        +move_to_showdown(self): none
        +execute_player_turn(self, action: str, bet_amount=0): None | Literal['opponent wins']
        +get_winner(self): Literal['Player wins!'] | Literal['Dealer wins!'] | Literal['It\'s a tie!']
        +combine_hands(self, player_cards: list[Card]): list[Card]
    }

    %% player.py
    class Player {
        +__init__(self, name: str): none
        +add_card(self, card: Card): none
        +remove_card(self, card: Card): none
        +has_card(self, card: Card): bool
    }

    %% poker_rules.py
    class PokerRules {
        +__init__(self): none
        +define_hand_rankings(self): dict
        +distribute_cards(self, deck): tuple
        +extract_values(self, hand): list[str]
        +extract_suits(self, hand): list[str]
        +extract_indices(self, hand): list[int]
        +royal_flush(self, hand): bool
        +straight_flush(self, hand): bool
        +four_of_a_kind(self, hand): bool
        +full_house(self, hand): bool
        +flush(self, hand): bool
        +straight(self, hand): bool
        +three_of_a_kind(self, hand): bool
        +two_pairs(self, hand): bool
        +pair(self, hand): bool
        +determine_winner(self, player_hand: list[Card], opponent_hand: list[Card]): Literal['Player wins!'] | Literal['Dealer wins!'] | Literal['It\'s a tie!']
        +calculate_hand_ranking(self, hand: list[Card]): int
        +compare_hand_rankings(self, player_ranking: int, opponent_ranking: int): Literal['Player wins!'] | Literal['Dealer wins!'] | Literal['It\'s a tie!']
    }

    %% app.py
    class FlaskApp {
        +__init__(self): none
        +index(self): str
        +handle_post_request(self, action: str, bet_amount: int): dict
        +generate_game_state_response(self): dict
        +format_hand(self, cards: list[Card]): list[dict]
        +start_game(self): dict
        +new_game(self): dict
        +home_poker(self): str
    }

    %% Relationships
    Game "1" --> "1" Deck : uses
    Game "1" --> "2..*" Player : uses
    Game "1" --> "1" PokerRules : uses
    Deck "1" --> "52" Card : contains
    Player "0..*" --> "1" Card : has
    PokerRules "1" --> "1" Deck : uses
    PokerRules "1" --> "2..*" Player : uses
    PokerRules "0..*" --> "1" Card : evaluates
    FlaskApp "1" --> "1" Game : uses
```


Note:

To access the online functionalities of this poker game, use Flask as a server within the texas_hold_em_poker.py file.<br>
This file not only manages web-based interactions but also initiates the game, serving as the central hub for the system's dynamic operations.