// Funzione per creare un elemento immagine per una carta
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

// Funzione per creare un elemento carta
function createCardElement(card, isFaceDown = false) {
    const cardElement = document.createElement('div');
    cardElement.classList.add('card');
    cardElement.appendChild(createCardImage(card, isFaceDown));
    return cardElement;
}

// Funzione per mostrare una mano di carte
function displayHand(hand, elementId, isFaceDown = false) {
    const handElement = document.getElementById(elementId);
    handElement.innerHTML = ''; // Cancella le carte precedenti
    hand.forEach(card => {
        handElement.appendChild(createCardElement(card, isFaceDown));
    });
}

// Funzione per aggiornare il valore della puntata
function updateBetValue() {
    const betRange = document.getElementById('betRange');
    const betValue = document.getElementById('betValue');
    betValue.innerHTML = betRange.value;
}

// Funzione per eseguire un'azione di gioco
function executeAction(action, betAmount = 0) {
    console.log("Azione eseguita:", action);
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
        console.log("Risposta ricevuta:", data);
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
            showTurnMessage('Pre-Flop: I giocatori ricevono le due carte coperte.');
        } else if (data.phase === 'flop') {
            showTurnMessage('Flop: Vengono distribuite tre carte comuni.');
        } else if (data.phase === 'turn') {
            showTurnMessage('Turn: Viene distribuita la quarta carta comune.');
        } else if (data.phase === 'river') {
            showTurnMessage('River: Viene distribuita la quinta carta comune.');
        }
    })
    .catch(error => {
        console.error('Errore:', error);
        alert('Si è verificato un errore durante l\'esecuzione dell\'azione. Per favore, riprova.');
    });
}

// Funzione per mostrare il mazzo
function displayDeck(deckCard, elementId) {
    const deckElement = document.getElementById(elementId);
    deckElement.innerHTML = ''; // Cancella il mazzo precedente
    deckElement.appendChild(createCardElement(deckCard, true)); // Le carte del mazzo sono coperte
}

// Funzione per piazzare una scommessa
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

    // Mappa l'importo della scommessa al colore e al valore corrispondenti delle fiches
    const chipColors = Object.keys(chipValues);
    const minChipValue = Math.min(...Object.values(chipValues));
    const maxChipValue = Math.max(...Object.values(chipValues));

    if (betAmount < minChipValue || betAmount > playerChips) {
        alert(`Puoi scommettere solo tra $${minChipValue} e $${playerChips}`);
        return;
    }

    console.log("Piazzando una scommessa di " + betAmount + " fiches");
    betMenu.style.display = 'none';

    const betMessage = document.createElement('div');
    betMessage.classList.add('bet-message');
    betMessage.textContent = `Hai scommesso ${betAmount} fiches`;
    document.body.appendChild(betMessage);

    setTimeout(() => {
        betMessage.remove();
    }, 3000);

    executeAction('bet', betAmount);
}

// Funzione per ottenere le fiches del giocatore (esempio)
function getPlayerChips() {
    return 1000000000; // Esempio di fiches iniziali.
}

// Altre funzioni...
function toggleRulesMenu() {
    const rulesMenu = document.getElementById('rulesMenu');
    if (rulesMenu.style.display === 'none') {
        rulesMenu.style.display = 'block';
    } else {
        rulesMenu.style.display = 'none';
    }
}

function showExplanation(event) {
    const message = event.target.getAttribute('data-tooltip');
    const explanationBox = document.getElementById('explanation-box');
    explanationBox.textContent = message;
    explanationBox.style.display = 'block';
    explanationBox.style.top = `${event.clientY + 10}px`;
    explanationBox.style.left = `${event.clientX + 10}px`;
}

function hideExplanation() {
    const explanationBox = document.getElementById('explanation-box');
    explanationBox.style.display = 'none';
}

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
        exitButton.style.display = 'block'; // Assicura che il pulsante di uscita rimanga visibile
    }
}

function exitGame() {
    window.location.href = '/';
}

// Funzione per avviare la musica di sottofondo
function playBackgroundMusic() {
    var backgroundMusic = document.getElementById('background-music');
    if (backgroundMusic.paused) {
        backgroundMusic.play();
    }
}

// Avvia la musica quando la pagina viene caricata
window.addEventListener('load', playBackgroundMusic);

// Cambia la musica di sottofondo dopo che il primo brano finisce
var backgroundMusic = document.getElementById('background-music');
backgroundMusic.addEventListener('ended', function() {
    if (backgroundMusic.src.includes('welcome_to_new_orleans.mp3')) {
        backgroundMusic.src = '/static/music/two_cigarettes_please.mp3';
    } else {
        backgroundMusic.src = '/static/music/welcome_to_new_orleans.mp3';
    }
    backgroundMusic.play();
});