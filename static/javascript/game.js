function createCardElement(card, isFaceDown=false) {
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
    img.src = `/static/card_images/${isFaceDown ? 'card_back.jpg' : `${suit}/${value}_${suit}.png`}`;
    img.alt = isFaceDown ? 'Card Back' : `${card.value} of ${card.suit}`;
    cardElement.appendChild(img);
    return cardElement;
}

function displayHand(hand, elementId, isFaceDown=false) {
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
    })
    .catch(error => {
        console.error('Errore:', error);
        alert('Si è verificato un errore durante l inizio del gioco. Riprova.');
    });
}

function executeAction(action) {
    console.log("Action executed:", action);
    fetch('/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
            'action': action,
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log("Received response:", data);
        // Aggiorna l'interfaccia utente con i dati ricevuti
        displayHand(data.player_hand, 'player-hand');
        displayHand(data.dealer_hand, 'dealer-hand', data.winner !== null); // Mostra le carte del dealer se il gioco è terminato
        displayHand(data.community_cards, 'community-cards');
        displayDeck(data.deck_card, 'deck');
        if (data.winner !== null) {
            showDealerCards(data.dealer_hand); // Mostra le carte del dealer
            document.getElementById('winner').innerHTML = `<div class="winner-message">${data.winner}</div>`; // Messaggio di vittoria
        } else {
            document.getElementById('winner').textContent = '';
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
    // Aggiungi la logica per piazzare una scommessa
    console.log("Piazza una scommessa");
}

function exitGame() {
    // Aggiungi un messaggio di conferma di uscita
    alert("Stai uscendo dal gioco. Grazie per aver giocato!");
    console.log("Esce dal gioco");
    //window.close(); // Chiude la finestra del browser
}