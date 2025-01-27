// Function to create an image element for a card
function createCardImage(card, isFaceDown = false) {
    const valueMap = {
        'A': '01',
        '2': '02',
        '3': '03',
        '4': '04',
        '5': '05',
        '6': '06',
        '7': '07',
        '8': '08',
        '9': '09',
        '10': '10',
        'J': '11',
        'Q': '12',
        'K': '13',
        'back': 'card_back'
    };
    const value = isFaceDown ? 'back' : valueMap[card.value];
    const suit = card.suit.toLowerCase();
    const img = document.createElement('img');
    img.src = `/static/card_images/${isFaceDown ? 'card_back.jpg' : `${suit}/${value}_${suit}.png`}`;
    img.alt = isFaceDown ? 'Card Back' : `${card.value} of ${card.suit}`;
    return img;
}

// Function to create a card element
function createCardElement(card, isFaceDown = false) {
    const cardElement = document.createElement('div');
    cardElement.classList.add('card');
    cardElement.appendChild(createCardImage(card, isFaceDown));
    return cardElement;
}

// Function to display a hand of cards
function displayHand(hand, elementId, isFaceDown = false) {
    const handElement = document.getElementById(elementId);
    handElement.innerHTML = ''; // Clear previous cards
    hand.forEach(card => {
        handElement.appendChild(createCardElement(card, isFaceDown));
    });
}

// Function to show the dealer's cards
function showDealerCards(dealerHand) {
    displayHand(dealerHand, 'dealer-hand', false); // Show dealer's cards
}

document.addEventListener('DOMContentLoaded', function () {
    const newGameButton = document.getElementById('newGame');
    const startGameButton = document.getElementById('startGame');
    const exitButton = document.getElementById('exit');
    const gameButtons = document.getElementById('gameButtons');
    const betMenu = document.getElementById('betMenu');
    const betRange = document.getElementById('betRange');
    const betValue = document.getElementById('betValue');
    const rulesButton = document.getElementById('rules');
    const rulesMenu = document.getElementById('rulesMenu');
    const placeBetButton = document.getElementById('placeBetButton');
    const toggleBetMenuButton = document.getElementById('toggleBetMenuButton');

    newGameButton.addEventListener('click', newGame);
    startGameButton.addEventListener('click', startGame);
    exitButton.addEventListener('click', exitGame);
    betRange.addEventListener('input', updateBetValue);
    rulesButton.addEventListener('click', toggleRulesMenu);
    placeBetButton.addEventListener('click', placeBet);
    toggleBetMenuButton.addEventListener('click', toggleBetMenu);

    const actionButtons = document.querySelectorAll('#gameButtons .button');
    actionButtons.forEach(button => {
        button.addEventListener('mouseover', showExplanation);
        button.addEventListener('mouseout', hideExplanation);
    });

    updateButtons('initial');
});

window.onload = function() {
    updateButtons('initial');
    // Hide all card areas until "New Game" is clicked
    document.getElementById('dealer-hand').style.display = 'none';
    document.getElementById('community-cards').style.display = 'none';
    document.getElementById('player-hand').style.display = 'none';
    document.getElementById('deck').style.display = 'none';

    // Update the display of the bet value
    betValue.innerHTML = betRange.value; // Display the default slider value

    betRange.oninput = function() {
        betValue.innerHTML = this.value;
    }
};

// Show an explanation when the mouse is over an action button
function showExplanation(event) {
    const message = event.target.getAttribute('data-tooltip');
    const explanationBox = document.getElementById('explanation-box');
    explanationBox.textContent = message;
    explanationBox.style.display = 'block';
    explanationBox.style.top = `${event.clientY + 10}px`;
    explanationBox.style.left = `${event.clientX + 10}px`;
}

// Hide the explanation when the mouse leaves the action button
function hideExplanation() {
    const explanationBox = document.getElementById('explanation-box');
    explanationBox.style.display = 'none';
}

// Update button visibility based on game state
function updateButtons(state) {
    const newGameButton = document.getElementById('newGame');
    const startGameButton = document.getElementById('startGame');
    const exitButton = document.getElementById('exit');
    const gameButtons = document.getElementById('gameButtons');

    if (state === 'initial') {
        newGameButton.style.display = 'block';
        startGameButton.style.display = 'none';
        gameButtons.style.display = 'none';
    } else if (state === 'readyToStart') {
        newGameButton.style.display = 'none';
        startGameButton.style.display = 'block';
        gameButtons.style.display = 'none';
    } else if (state === 'betting') {
        newGameButton.style.display = 'none';
        startGameButton.style.display = 'none';
        gameButtons.style.display = 'block';
    } else if (state === 'endGame') {
        newGameButton.style.display = 'block';
        startGameButton.style.display = 'none';
        gameButtons.style.display = 'none';
    }
}

function newGame() {
    console.log("New Game clicked");
    fetch('/new-game', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
    })
    .then(response => {
        console.log("Raw response status:", response.status);
        if (!response.ok) {
            throw new Error('Network response was not ok ' + response.statusText);
        }
        return response.json();
    })
    .then(data => {
        console.log("Received response:", data);
        document.getElementById('dealer-hand').style.display = 'none';
        document.getElementById('community-cards').style.display = 'none';
        document.getElementById('player-hand').style.display = 'none';
        document.getElementById('deck').style.display = 'none';
        document.getElementById('winner').textContent = '';
        document.getElementById('winner').style.display = 'none';

        updateButtons('readyToStart'); // Change button states
        displayHand([], 'player-hand');
        displayHand([], 'dealer-hand');
        displayHand([], 'community-cards');
        displayDeck({'value': 'back', 'suit': 'card_back'}, 'deck');
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while resetting the game. Please try again.');
    });
}

function startGame() {
    console.log("Start Game clicked");
    fetch('/start-game', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
    })
    .then(response => {
        console.log("Raw response status:", response.status);
        if (!response.ok) {
            throw new Error('Network response was not ok ' + response.statusText);
        }
        return response.json();
    })
    .then(data => {
        console.log("Received response:", data);
        document.getElementById('dealer-hand').style.display = 'flex';
        document.getElementById('community-cards').style.display = 'flex';
        document.getElementById('player-hand').style.display = 'flex';
        document.getElementById('deck').style.display = 'flex';
        document.getElementById('winner').textContent = '';
        document.getElementById('winner').style.display = 'none';

        updateButtons('betting');
        displayHand(data.player_hand, 'player-hand');
        displayHand(data.community_cards, 'community-cards');

        // Mostra le carte del dealer coperte fino alla fase di showdown
        if (data.phase === 'showdown') {
            displayHand(data.dealer_hand, 'dealer-hand', false);
        } else {
            displayHand(data.dealer_hand, 'dealer-hand', true);
        }

        displayDeck(data.deck_card, 'deck');
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while starting the game. Please try again.');
    });
}

function executeAction(action, betAmount = 0) {
    console.log("Action executed:", action);
    fetch('/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: new URLSearchParams({
            'action': action,
            'betAmount': betAmount
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log("Received response:", data);
        displayHand(data.player_hand, 'player-hand');
        displayHand(data.community_cards, 'community-cards');
        displayDeck(data.deck_card, 'deck');

        if (data.phase === 'showdown') {
            showDealerCards(data.dealer_hand);  // Mostra le carte del dealer solo nella fase di showdown
            document.getElementById('winner').textContent = data.winner;
            document.getElementById('winner').style.display = 'block';
            endGame();
        } else {
            displayHand(data.dealer_hand, 'dealer-hand', true);
            document.getElementById('winner').textContent = '';
            document.getElementById('winner').style.display = 'none';
        }

        if (data.phase === 'pre-flop') {
            showTurnMessage('Pre-Flop: Players receive their two hole cards.');
        } else if (data.phase === 'flop') {
            showTurnMessage('Flop: Three community cards are dealt.');
        } else if (data.phase === 'turn') {
            showTurnMessage('Turn: A fourth community card is dealt.');
        } else if (data.phase === 'river') {
            showTurnMessage('River: A fifth community card is dealt.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while executing the action. Please try again.');
    });
}

// Function to end the game and update the buttons
function endGame() {
    updateButtons('endGame');
}

// Update button visibility based on game state
function updateButtons(state) {
    const newGameButton = document.getElementById('newGame');
    const startGameButton = document.getElementById('startGame');
    const exitButton = document.getElementById('exit');
    const gameButtons = document.getElementById('gameButtons');

    if (state === 'initial') {
        newGameButton.style.display = 'block';
        startGameButton.style.display = 'none';
        gameButtons.style.display = 'none';
    } else if (state === 'readyToStart') {
        newGameButton.style.display = 'none';
        startGameButton.style.display = 'block';
        gameButtons.style.display = 'none';
    } else if (state === 'betting') {
        newGameButton.style.display = 'none';
        startGameButton.style.display = 'none';
        gameButtons.style.display = 'block';
    } else if (state === 'endGame') {
        newGameButton.style.display = 'block';
        startGameButton.style.display = 'none';
        gameButtons.style.display = 'none';
        exitButton.style.display = 'block'; // Ensure the exit button remains visible
    }
}

// Function to exit the game
function exitGame() {
    window.location.href = '/';
}

// Function to place a bet
function placeBet() {
    const betAmount = parseInt(betRange.value);
    const playerChips = getPlayerChips();
    const chipValues = {
        'white': 1,
        'red': 5,
        'blue': 10,
        'green': 25,
        'black': 100,
        'purple': 500,
        'yellow': 1000,
        'pink': 5000,
        'light blue': 10000
    };

    // Map the bet amount to the corresponding chip color and value
    const chipColors = Object.keys(chipValues);
    const minChipValue = Math.min(...Object.values(chipValues));
    const maxChipValue = Math.max(...Object.values(chipValues));

    if (betAmount < minChipValue || betAmount > playerChips) {
        alert(`You can only bet between $${minChipValue} and $${playerChips}`);
        return;
    }

    console.log("Placing a bet of " + betAmount + " chips");
    betMenu.style.display = 'none';

    const betMessage = document.createElement('div');
    betMessage.classList.add('bet-message');
    betMessage.textContent = `You have bet ${betAmount} chips`;
    document.body.appendChild(betMessage);

    setTimeout(() => {
        betMessage.remove();
    }, 3000);

    executeAction('bet', betAmount);
}

// Initialize the bet range and value on DOMContentLoaded
document.addEventListener('DOMContentLoaded', function () {
    const placeBetButton = document.getElementById('placeBetButton');
    placeBetButton.addEventListener('click', placeBet);

    const betRange = document.getElementById('betRange');
    const betValue = document.getElementById('betValue');
    const playerChips = getPlayerChips();

    // Set the minimum and maximum values for the bet range slider
    betRange.min = 1;
    betRange.max = playerChips;

    betRange.addEventListener('input', function() {
        betValue.innerHTML = `$${betRange.value}`;
    });
});

// Function to execute a game action
function executeAction(action, betAmount = 0) {
    console.log("Action executed:", action);
    fetch('/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: new URLSearchParams({
            'action': action,
            'betAmount': betAmount
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log("Received response:", data);
        displayHand(data.player_hand, 'player-hand');
        displayHand(data.community_cards, 'community-cards');
        displayDeck(data.deck_card, 'deck');

        if (data.phase === 'showdown') {
            showDealerCards(data.dealer_hand);  // Show dealer's cards only in showdown phase
            document.getElementById('winner').textContent = data.winner;
            document.getElementById('winner').style.display = 'block';
            endGame();
        } else {
            displayHand(data.dealer_hand, 'dealer-hand', true);
            document.getElementById('winner').textContent = '';
            document.getElementById('winner').style.display = 'none';
        }

        if (data.phase === 'pre-flop') {
            showTurnMessage('Pre-Flop: Players receive their two hole cards.');
        } else if (data.phase === 'flop') {
            showTurnMessage('Flop: Three community cards are dealt.');
        } else if (data.phase === 'turn') {
            showTurnMessage('Turn: A fourth community card is dealt.');
        } else if (data.phase === 'river') {
            showTurnMessage('River: A fifth community card is dealt.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while executing the action. Please try again.');
    });
}

// Initialize the bet range and value on DOMContentLoaded
document.addEventListener('DOMContentLoaded', function () {
    const placeBetButton = document.getElementById('placeBetButton');
    placeBetButton.addEventListener('click', placeBet);

    const betRange = document.getElementById('betRange');
    const betValue = document.getElementById('betValue');
    const playerChips = getPlayerChips();

    // Set the minimum and maximum values for the bet range slider
    betRange.min = 1;
    betRange.max = playerChips;

    betRange.addEventListener('input', function() {
        betValue.innerHTML = `$${betRange.value}`;
    });
});

document.addEventListener('DOMContentLoaded', function () {
    const placeBetButton = document.getElementById('placeBetButton');
    placeBetButton.addEventListener('click', placeBet);
});

document.addEventListener('DOMContentLoaded', function () {
    const placeBetButton = document.getElementById('placeBetButton');
    placeBetButton.addEventListener('click', placeBet);
});

function toggleRulesMenu() {
    const rulesMenu = document.getElementById('rulesMenu');
    if (rulesMenu.style.display === 'none') {
        rulesMenu.style.display = 'block';
    } else {
        rulesMenu.style.display = 'none';
    }
}

// Function to execute a game action
function executeAction(action, betAmount = 0) {
    console.log("Action executed:", action);
    fetch('/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: new URLSearchParams({
            'action': action,
            'betAmount': betAmount
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log("Received response:", data);
        displayHand(data.player_hand, 'player-hand');
        displayHand(data.community_cards, 'community-cards');
        displayDeck(data.deck_card, 'deck');

        if (data.phase === 'showdown') {
            showDealerCards(data.dealer_hand);
            document.getElementById('winner').textContent = data.winner;
            document.getElementById('winner').style.display = 'block';
            endGame();
        } else {
            displayHand(data.dealer_hand, 'dealer-hand', true);
            document.getElementById('winner').textContent = '';
            document.getElementById('winner').style.display = 'none';
        }

        if (data.phase === 'pre-flop') {
            showTurnMessage('Pre-Flop: Players receive their two hole cards.');
        } else if (data.phase === 'flop') {
            showTurnMessage('Flop: Three community cards are dealt.');
        } else if (data.phase === 'turn') {
            showTurnMessage('Turn: A fourth community card is dealt.');
        } else if (data.phase === 'river') {
            showTurnMessage('River: A fifth community card is dealt.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while executing the action. Please try again.');
    });
}

// Function to get the player's chips (example)
function getPlayerChips() {
    return 100000000000000000000000000000000000000000000000000000000000000; // Esempio di fiches. è da adattare con il casino
}

// Function to toggle the rules menu visibility
function toggleRulesMenu() {
    const rulesMenu = document.getElementById('rulesMenu');
    if (rulesMenu.style.display === 'none') {
        rulesMenu.style.display = 'block';
    } else {
        rulesMenu.style.display = 'none';
    }
}

// Function to show the turn message
function showTurnMessage(message) {
    const turnMessage = document.getElementById('turn-message');
    turnMessage.textContent = message;
    turnMessage.style.display = 'block';
    setTimeout(() => {
        turnMessage.style.display = 'none';
    }, 3000); // Show the message for 3 seconds
}

// Function to display the deck
function displayDeck(deckCard, elementId) {
    const deckElement = document.getElementById(elementId);
    deckElement.innerHTML = ''; // Clear previous deck
    deckElement.appendChild(createCardElement(deckCard, true)); // Deck cards are face down
}

// Function to start the background music
function playBackgroundMusic() {
    var backgroundMusic = document.getElementById('background-music');
    if (backgroundMusic.paused) {
        backgroundMusic.play();
    }
}

// Start the music when the page loads
window.addEventListener('load', playBackgroundMusic);

// Change the background music after the first track ends
var backgroundMusic = document.getElementById('background-music');
backgroundMusic.addEventListener('ended', function() {
    if (backgroundMusic.src.includes('welcome_to_new_orleans.mp3')) {
        backgroundMusic.src = '/static/music/two_cigarettes_please.mp3';
    } else {
        backgroundMusic.src = '/static/music/welcome_to_new_orleans.mp3';
    }
    backgroundMusic.play();
});