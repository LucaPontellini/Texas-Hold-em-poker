function createCardElement(card, isFaceDown = false) {
    const cardElement = document.createElement('div');
    cardElement.classList.add('card');
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
    img.src = `/static/card_images/${isFaceDown ? 'card_back.jpg' : ${suit}/${value}_${suit}.png}`;
    img.alt = isFaceDown ? 'Card Back' : ${card.value} of ${card.suit};
    cardElement.appendChild(img);
    return cardElement;
}

function displayHand(hand, elementId, isFaceDown = false) {
    const handElement = document.getElementById(elementId);
    handElement.innerHTML = ''; // Pulisce le carte precedenti
    hand.forEach(card => {
        handElement.appendChild(createCardElement(card, isFaceDown));
    });
}

function showDealerCards(dealerHand) {
    displayHand(dealerHand, 'dealer-hand', false); // Mostra le carte del dealer
}

window.onload = function() {
    // Non visualizzare alcuna carta fino a quando non si preme "New Game"
    document.getElementById('dealer-hand').style.display = 'none';
    document.getElementById('community-cards').style.display = 'none';
    document.getElementById('player-hand').style.display = 'none';
    document.getElementById('deck').style.display = 'none';

    // Aggiorna il valore della puntata
    var betRange = document.getElementById("betRange");
    var betValue = document.getElementById("betValue");
    betValue.innerHTML = betRange.value; // Display the default slider value

    betRange.oninput = function() {
        betValue.innerHTML = this.value;
    }

    // Mostra solo i pulsanti iniziali
    updateButtons('initial');
};

function newGame() {
    console.log("New Game clicked");
    fetch('/new-game', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        }
    })
    .then(response => response.json())
    .then(data => {
        console.log("Received response:", data);
        // Visualizzare il mazzo e l'area delle carte dopo aver premuto "New Game"
        document.getElementById('dealer-hand').style.display = 'flex';
        document.getElementById('community-cards').style.display = 'flex';
        document.getElementById('player-hand').style.display = 'flex';
        document.getElementById('deck').style.display = 'flex';
        document.getElementById('winner').textContent = '';
        document.getElementById('winner').style.display = 'none'; // Nasconde il messaggio di vittoria

        // Mostra i pulsanti di puntata
        updateButtons('betting');

        // Reimposta le mani e le carte comunitarie
        displayHand([], 'player-hand');
        displayHand([], 'dealer-hand');
        displayHand([], 'community-cards');
        displayDeck({'value': 'back', 'suit': 'card_back'}, 'deck');
    })
    .catch(error => {
        console.error('Errore:', error);
        alert('Si è verificato un errore durante l inizio della nuova partita. Riprova.');
    });
}

function startGame() {
    console.log("Start Game clicked");
    fetch('/start-game', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        }
    })
    .then(response => response.json())
    .then(data => {
        console.log("Received response:", data);
        // Aggiorna l'interfaccia utente con i dati ricevuti
        displayHand(data.player_hand, 'player-hand');
        displayHand(data.dealer_hand, 'dealer-hand', true); // Il dealer vede le sue carte coperte
        displayHand(data.community_cards, 'community-cards');
        displayDeck(data.deck_card, 'deck');
        document.getElementById('winner').textContent = data.winner || '';
        document.getElementById('winner').style.display = data.winner ? 'block' : 'none'; // Mostra il messaggio di vittoria solo se c'è un vincitore
    })
    .catch(error => {
        console.error('Errore:', error);
        alert('Si è verificato un errore durante l inizio del gioco. Riprova.');
    });
}

function showTurnMessage(message) {
    const turnMessageElement = document.getElementById('turn-message');
    turnMessageElement.textContent = message;
    turnMessageElement.style.display = 'block';
    setTimeout(() => {
        turnMessageElement.style.display = 'none';
    }, 3000); // Il messaggio scompare dopo 3 secondi
}

function executeAction(action, betAmount = 0) {
    console.log("Action executed:", action);
    fetch('/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
            'action': action,
            'betAmount': betAmount
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log("Received response:", data);
        // Aggiorna l'interfaccia utente con i dati ricevuti
        displayHand(data.player_hand, 'player-hand');
        displayHand(data.community_cards, 'community-cards');
        displayDeck(data.deck_card, 'deck');
        
        if (data.phase === 'showdown') {
            showDealerCards(data.dealer_hand); // Mostra le carte del dealer solo durante lo showdown
            document.getElementById('winner').textContent = data.winner; // Imposta il testo del messaggio di vittoria
            document.getElementById('winner').style.display = 'block'; // Mostra il messaggio di vittoria
        } else {
            displayHand(data.dealer_hand, 'dealer-hand', true); // Mostra le carte del dealer coperte
            document.getElementById('winner').textContent = '';
            document.getElementById('winner').style.display = 'none'; // Nasconde il messaggio di vittoria
        }

        // Mostra il messaggio del turno
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
        console.error('Errore:', error);
        alert('Si è verificato un errore durante l esecuzione dell azione. Riprova.');
    });
}

function displayDeck(deckCard, elementId) {
    const deckElement = document.getElementById(elementId);
    deckElement.innerHTML = ''; // Pulisce il mazzo precedente
    deckElement.appendChild(createCardElement(deckCard, true)); // Le carte del mazzo sono coperte
}

function placeBet() {
    const betAmount = parseInt(document.getElementById("betRange").value);
    const playerChips = getPlayerChips(); // Funzione che restituisce il numero di fiches del giocatore

    if (betAmount > playerChips) {
        alert("You cannot bet more chips than you have!");
        return;
    }

    console.log("Placing a bet of " + betAmount + " chips");
    document.getElementById("betMenu").style.display = "none"; // Nasconde il menu delle fiches dopo la scommessa
    
    // Mostra il messaggio di scommessa
    var betMessage = document.createElement('div');
    betMessage.classList.add('bet-message');
    betMessage.textContent = You have bet ${betAmount} chips;
    document.body.appendChild(betMessage);
    
    // Rimuove il messaggio dopo 3 secondi
    setTimeout(() => {
        betMessage.remove();
    }, 3000);
    
    // Aggiungi la logica per piazzare una scommessa
    executeAction('bet', betAmount);
}

function getPlayerChips() {
    // Implementa questa funzione per restituire il numero di fiches del giocatore
    // Ad esempio, potresti ottenere questo valore dal server o da una variabile globale
    return 100; // Esempio: restituisce 100 fiches
}

function toggleBetMenu() {
    var betMenu = document.getElementById("betMenu");
    if (betMenu.style.display === "none") {
        betMenu.style.display = "block";
    } else {
        betMenu.style.display = "none";
    }
}

function toggleRulesMenu() {
    var rulesMenu = document.getElementById("rulesMenu");
    if (rulesMenu.style.display === "none") {
        rulesMenu.style.display = "block";
    } else {
        rulesMenu.style.display = "none";
    }
}

function exitGame() {
    // Aggiungi un messaggio di conferma di uscita
    alert("Stai uscendo dal gioco. Grazie per aver giocato!");
    console.log("Esce dal gioco");
    //window.close(); // Chiude la finestra del browser
}

function updateButtons(state) {
    const buttons = {
        'start': document.querySelector('button[onclick="startGame()"]'),
        'newGame': document.querySelector('button[onclick="newGame()"]'),
        'exit': document.querySelector('button[onclick="exitGame()"]'),
        'rules': document.querySelector('button[onclick="toggleRulesMenu()"]'),
        'betMenu': document.querySelector('button[onclick="toggleBetMenu()"]'),
        'check': document.querySelector('button[onclick="executeAction(\'check\')"]'),
        'bet': document.querySelector('button[onclick="executeAction(\'bet\')"]'),
        'call': document.querySelector('button[onclick="executeAction(\'call\')"]'),
        'raise': document.querySelector('button[onclick="executeAction(\'raise\')"]'),
        'fold': document.querySelector('button[onclick="executeAction(\'fold\')"]')
    };
    
    if (state === 'initial') {
        buttons.start.style.display = 'block';
        buttons.newGame.style.display = 'block';
        buttons.exit.style.display = 'block';
        buttons.rules.style.display = 'block';
        buttons.betMenu.style.display = 'none';
        buttons.check.style.display = 'none';
        buttons.bet.style.display = 'none';
        buttons.call.style.display = 'none';
        buttons.raise.style.display = 'none';
        buttons.fold.style.display = 'none';
    } else if (state === 'betting') {
        buttons.betMenu.style.display = 'block';
        buttons.check.style.display = 'block';
        buttons.bet.style.display = 'block';
        buttons.call.style.display = 'block';
        buttons.raise.style.display = 'block';
        buttons.fold.style.display = 'block';
    }
}

// Funzione per avviare la musica
function playBackgroundMusic() {
    var backgroundMusic = document.getElementById('background-music');
    if (backgroundMusic.paused) {
        backgroundMusic.play();
    }
}

// Avvia la musica quando la pagina viene caricata
window.addEventListener('load', playBackgroundMusic);

// Cambia la musica di sottofondo dopo che la prima traccia è finita
var backgroundMusic = document.getElementById('background-music');
backgroundMusic.addEventListener('ended', function() {
    if (backgroundMusic.src.includes('welcome_to_new_orleans.mp3')) {
        backgroundMusic.src = '/static/music/two_cigarettes_please.mp3';
    } else {
        backgroundMusic.src = '/static/music/welcome_to_new_orleans.mp3';
    }
    backgroundMusic.play();
});