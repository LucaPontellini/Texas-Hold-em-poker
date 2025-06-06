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

// Funzione per mostrare il mazzo
function displayDeck(deckCard, elementId) {
    const deckElement = document.getElementById(elementId);
    deckElement.innerHTML = ''; // Cancella il mazzo precedente
    deckElement.appendChild(createCardElement(deckCard, true)); // Le carte del mazzo sono coperte
}

// Funzione per aggiornare il valore della puntata
function updateBetValue() {
    const betRange = document.getElementById('betRange');
    const betValue = document.getElementById('betValue');
    betValue.innerHTML = betRange.value;
}

// Funzione per piazzare una scommessa
function placeBet() {
    const betRange = document.getElementById('betRange');
    const betAmount = parseInt(betRange.value);
    const playerChips = getPlayerChips();  // Chiamata a getPlayerChips

    // Verifica se l'importo della scommessa è valido
    if (betAmount < 1 || betAmount > playerChips) {
        alert(`Puoi scommettere solo tra $1 e $${playerChips}`);
        return;
    }

    console.log("Piazzando una scommessa di " + betAmount + " fiches");
    document.getElementById('betMenu').style.display = 'none'; // Nasconde il menu delle scommesse

    const betMessage = document.createElement('div');
    betMessage.classList.add('bet-message');
    betMessage.textContent = `Hai scommesso ${betAmount} fiches`;
    document.body.appendChild(betMessage);

    setTimeout(() => {
        betMessage.remove();
    }, 3000);

    executeAction('bet', betAmount);
}

function getPlayerChips() {
    // Supponiamo che i gettoni del giocatore siano memorizzati in un elemento con ID 'player-chips'
    const playerChipsElement = document.getElementById('player-chips');
    return parseInt(playerChipsElement.textContent, 10) || 0;
}

let isRequestPending = false;

function executeAction(action, betAmount = 0) {
    if (isRequestPending) {
        console.warn('Azione già in corso. Attendi la risposta.');
        return;
    }

    isRequestPending = true;
    console.log('Esecuzione azione:', action, 'con betAmount:', betAmount);
    fetch('/action', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: new URLSearchParams({
            'action': action,
            'betAmount': betAmount
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log("Azione eseguita:", data);
        displayHand(data.player_hand, 'player-hand');
        displayHand(data.community_cards, 'community-cards');
        displayDeck(data.deck_card, 'deck');
        updateButtons('betting', data.current_turn, data.blinds_info);
        showTurnMessage(data.message);

        if (data.winning_hand) {
            illuminateWinningHand(data.winning_hand);
            showWinningExplanation(data.winning_hand);
        }

        if (data.phase !== "showdown") {
            advanceTurn();
        }
    })
    .catch(error => {
        console.error('Errore:', error);
        alert('Si è verificato un errore durante l\'esecuzione dell\'azione. Per favore, riprova.');
    })
    .finally(() => {
        isRequestPending = false; // Permetti nuove richieste
    });
}

function showTurnMessage(message) {
    const turnMessageElement = document.getElementById('turn-message');
    turnMessageElement.textContent = message;
    turnMessageElement.style.display = 'block';
}

// Funzione per mostrare/nascondere il menu delle regole
function toggleRulesMenu() {
    const rulesMenu = document.getElementById('rulesMenu');
    if (rulesMenu.style.display === 'none') {
        rulesMenu.style.display = 'block';
    } else {
        rulesMenu.style.display = 'none';
    }
}

// Funzione per mostrare/nascondere il menu delle scommesse
function toggleBetMenu() {
    const betMenu = document.getElementById('betMenu');
    if (betMenu.style.display === 'none' || betMenu.style.display === '') {
        betMenu.style.display = 'block';
    } else {
        betMenu.style.display = 'none';
    }
}

// Funzione per mostrare la spiegazione
function showExplanation(event) {
    const message = event.target.getAttribute('data-tooltip');
    const explanationBox = document.getElementById('explanation-box');
    explanationBox.textContent = message;
    explanationBox.style.display = 'block';
    explanationBox.style.top = `${event.clientY + 10}px`;
    explanationBox.style.left = `${event.clientX + 10}px`;
}

// Funzione per nascondere la spiegazione
function hideExplanation() {
    const explanationBox = document.getElementById('explanation-box');
    explanationBox.style.display = 'none';
}

// Funzione per aggiornare lo stato dei pulsanti
function updateButtons(state, currentTurn, blindsInfo) {
    const newGameButton = document.getElementById('newGame');
    const startGameButton = document.getElementById('startGame');
    const exitButton = document.getElementById('exit');
    const gameButtons = document.getElementById('gameButtons');
    const turnInfo = document.getElementById('turn-info');  
    const deck = document.querySelector('.deck');  
    const gameButtonArray = Array.from(gameButtons.getElementsByTagName('button'));
    const playerName = 'player';  // Sostituisci con il nome del giocatore reale

    if (state === 'initial') {
        newGameButton.style.display = 'block';
        startGameButton.style.display = 'none';
        gameButtons.style.display = 'none';
        exitButton.style.display = 'block';
        document.getElementById('rules').style.display = 'block';
        turnInfo.style.display = 'none';  
        deck.style.display = 'none';  
    } else if (state === 'readyToStart') {
        newGameButton.style.display = 'none';
        startGameButton.style.display = 'block';
        gameButtons.style.display = 'none';
        turnInfo.style.display = 'block';  
        deck.style.display = 'block';  
    } else if (state === 'betting') {
        newGameButton.style.display = 'none';
        startGameButton.style.display = 'none';
        gameButtons.style.display = 'block';
    } else if (state === 'endGame') {
        newGameButton.style.display = 'block';
        startGameButton.style.display = 'none';
        gameButtons.style.display = 'none';
        exitButton.style.display = 'block';
    }

    const currentTurnIsPlayer = (currentTurn === 'player');
    gameButtonArray.forEach(button => {
        if (button.id !== 'newGame' && button.id !== 'startGame' && button.id !== 'exit') {
            button.disabled = !currentTurnIsPlayer;
            button.style.backgroundColor = currentTurnIsPlayer ? '#4CAF50' : '#D3D3D3';
            button.style.color = currentTurnIsPlayer ? 'white' : '#888';
        }
    });    

    if (blindsInfo) {  
        let turnMessage = `È il turno di: ${currentTurn}`;
        if (blindsInfo.small_blind === currentTurn) {
            turnMessage += ' (Small Blind)';
        }
        if (blindsInfo.big_blind === currentTurn) {
            turnMessage += ' (Big Blind)';
        }
        turnInfo.textContent = turnMessage;
    }
}

function highlightCurrentPlayerTurn(currentTurn) {
    const turnInfoElement = document.getElementById('turn-info');
    if (turnInfoElement) {
        turnInfoElement.style.backgroundColor = currentTurn === 'player' ? '#FFD700' : 'transparent'; // Evidenzia il turno del giocatore
    }
}

function updateGameState(gameState) {
    console.log("Stato aggiornato:", gameState); // Debugging dettagliato
    const currentTurnElement = document.getElementById('currentTurn');
    if (currentTurnElement) {
        currentTurnElement.innerText = `Turno corrente: ${gameState.current_turn}`;
    }
    highlightCurrentPlayerTurn(gameState.current_turn);
}

function logMessage(type, message) {
    const logPrefix = `[${new Date().toISOString()}] ${type.toUpperCase()}:`;
    console.log(`${logPrefix} ${message}`);
}

// Utilizzo:
logMessage('info', 'Gioco avviato con successo.');
logMessage('error', 'Si è verificato un errore durante l\'esecuzione dell\'azione.');

function newGame() {
    fetch('/new-game', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: new URLSearchParams()
    })
    .then(response => response.json())
    .then(data => {
        console.log("Dati ricevuti da /new-game:", data);
        document.getElementById('player-hand').innerHTML = '';
        document.getElementById('community-cards').innerHTML = '';
        document.getElementById('deck').innerHTML = '';
        document.getElementById('winner').textContent = '';
        document.getElementById('winner').style.display = 'none';
        document.getElementById('blinds-info').innerHTML = '';
        updateButtons('readyToStart', data.current_turn, data.blinds_info);
    })
    .catch(error => {
        console.error('Errore nel reimpostare il gioco:', error);
        alert('Si è verificato un errore durante il reset del gioco.');
    });
}

function startGame() {
    console.log('Invio richiesta POST a /start-game');
    fetch('/start-game', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: new URLSearchParams()
    })
    .then(response => response.json())
    .then(data => {
        console.log("Dati ricevuti da /start-game:", data);
        updateGameState(data);
    })
    .catch(error => {
        console.error('Errore nell\'avviare la partita:', error);
        alert('Si è verificato un errore durante l\'avvio della partita.');
    });
}

// Funzione per uscire dal gioco
function exitGame() {
    window.location.href = '/';
}

function advanceTurn() {
    console.log('Avanzamento del turno...');
    fetch('/advance-turn', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
    })
    .then(response => response.json())
    .then(data => {
        console.log("Dati ricevuti da /advance-turn:", data);
        updateGameState(data);

        if (data.current_turn.startsWith("Bot")) {
            executeBotTurn(10);
        } else {
            updateButtons('betting', data.current_turn, data.blinds_info);
        }
    })
    .catch(error => {
        console.error('Errore durante l\'avanzamento del turno:', error);
        alert('Si è verificato un errore durante l\'avanzamento del turno.');
    });
}

function executeBotTurn(maxActions = 10) {
    if (maxActions <= 0) {
        console.error('Limite massimo di azioni bot raggiunto. Terminazione del ciclo.');
        alert('Il limite massimo di azioni bot è stato raggiunto. Verifica il funzionamento del gioco.');
        return;
    }

    fetch('/execute-bot-turn', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
    })
    .then(response => response.json())
    .then(data => {
        console.log("Bot ha eseguito il turno:", data);
        updateGameState(data);

        if (data.current_turn.startsWith("Bot")) {
            executeBotTurn(maxActions - 1);
        } else {
            updateButtons('betting', data.current_turn, data.blinds_info);
        }
    })
    .catch(error => {
        console.error('Errore durante il turno del bot:', error);
        alert('Si è verificato un errore durante il turno del bot. Per favore, riprova.');
    });
}


// Funzione per illuminare la mano vincente
function illuminateWinningHand(winningHand) {
    winningHand.forEach(card => {
        const cardElements = document.querySelectorAll(`.card img[alt='${card.value} of ${card.suit}']`);
        cardElements.forEach(element => {
            element.parentElement.classList.add('winning-card');
        });
    });
}

// Funzione per mostrare la spiegazione della mano vincente
function showWinningExplanation(explanation) {
    const explanationBox = document.createElement('div');
    explanationBox.classList.add('winner-message');
    explanationBox.textContent = explanation;
    document.body.appendChild(explanationBox);
    setTimeout(() => {
        explanationBox.style.display = 'none';
    }, 10000); // Mostra la spiegazione per 10 secondi
}

// Chiamata iniziale per impostare lo stato dei pulsanti
updateButtons('initial', '', {});

// Funzione per avviare la musica di sottofondo
function playBackgroundMusic() {
    console.log("Tentativo di riprodurre la musica di sottofondo...");
    var backgroundMusic = document.getElementById('background-music');
    if (backgroundMusic.paused) {
        backgroundMusic.play().then(() => {
            console.log("Musica di sottofondo avviata.");
        }).catch((error) => {
            console.error("Errore durante la riproduzione della musica:", error);
            alert("Per favore, abilita la riproduzione automatica dell'audio nel tuo browser.");
        });
    }
}

// Avvia la musica quando la pagina è stata completamente caricata e analizzata
document.addEventListener('DOMContentLoaded', playBackgroundMusic);

// Cambia la musica di sottofondo dopo che il primo brano finisce
var backgroundMusic = document.getElementById('background-music');
backgroundMusic.addEventListener('ended', function() {
    if (backgroundMusic.src.includes('welcome_to_new_orleans.mp3')) {
        backgroundMusic.src = '/static/music/two_cigarettes_please.mp3';
    } else {
        backgroundMusic.src = '/static/music/welcome_to_new_orleans.mp3';
    }
    backgroundMusic.play().then(() => {
        console.log("Musica cambiata e avviata.");
    }).catch((error) => {
        console.error("Errore durante il cambio di musica:", error);
    });
});

// Aggiungi anche il listener per il pulsante Exit per ulteriore debug
document.getElementById('exit').addEventListener('click', function() {
    console.log("Pulsante Exit premuto");
});

// Gestione della scritta "Deck" sulla carta del mazzo
document.addEventListener("DOMContentLoaded", function() {
    const deckImage = document.querySelector(".deck img");
    const deckLabel = document.querySelector(".deck-label");

    if (deckImage && deckLabel) {
        deckImage.addEventListener("load", function() {
            deckLabel.style.display = "block";
        });

        deckImage.addEventListener("error", function() {
            deckLabel.style.display = "none";
        });

        // Assumi che l'immagine card_back.jpg sia già caricata
        if (deckImage.complete) {
            deckLabel.style.display = "block";
        }
    }
});