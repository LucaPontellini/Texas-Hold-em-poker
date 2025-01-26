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
    }

    %% game.py
    class Game {
        +__init__(self): none
        +setup_players(self): none
        +next_phase(self): none
        +execute_player_turn(self, action, bet_amount=0): None | Literal['opponent wins']
        +get_winner(self): Literal['Player wins!'] | Literal['Dealer wins!'] | Literal['It\'s a tie!']
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
        +distribute_cards(self, deck): tuple
        +pair(self, hand): bool
        +two_pairs(self, hand): bool
        +three_of_a_kind(self, hand): bool
        +straight(self, hand): bool
        +flush(self, hand): bool
        +full_house(self, hand): bool
        +four_of_a_kind(self, hand): bool
        +straight_flush(self, hand): bool
        +determine_winner(self, player_hand, opponent_hand): Literal['Player wins!'] | Literal['Dealer wins!'] | Literal['It\'s a tie!']
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
```


Note:

To access the online functionalities of this poker game, use Flask as a server within the texas_hold_em_poker.py file.<br>
This file not only manages web-based interactions but also initiates the game, serving as the central hub for the system's dynamic operations.