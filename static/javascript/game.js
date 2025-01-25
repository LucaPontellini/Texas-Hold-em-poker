function createCardElement(card) {
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
    const value = valueMap[card.value];
    const suit = card.suit.toLowerCase();
    const img = document.createElement('img');
    if (value === 'card_back') {
        img.src = `/static/card_images/card_back.jpg`;
    } else {
        img.src = `/static/card_images/${suit}/${value}_${suit}.png`;
    }
    img.alt = `${card.value} of ${card.suit}`;
    cardElement.appendChild(img);
    return cardElement;
}

function displayHand(hand, elementId) {
    const handElement = document.getElementById(elementId);
    handElement.innerHTML = ''; // Pulisce le carte precedenti
    hand.forEach(card => {
        handElement.appendChild(createCardElement(card));
    });
}

function executeAction(action) {
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
        // Aggiorna l'interfaccia utente con i dati ricevuti
        displayHand(data.player_hand, 'player-hand');
        displayHand(data.dealer_hand, 'dealer-hand');
        displayHand(data.community_cards, 'community-cards');
        displayDeck(data.deck_card, 'deck');
        document.getElementById('winner').textContent = data.winner || '';
    })
    .catch(error => {
        console.error('Errore:', error);
        alert('Si è verificato un errore durante l esecuzione dell azione. Riprova.');
    });
}

function displayDeck(deckCard, elementId) {
    const deckElement = document.getElementById(elementId);
    deckElement.innerHTML = ''; // Pulisce il mazzo precedente
    deckElement.appendChild(createCardElement(deckCard));
}

// Inizializza le mani quando la pagina viene caricata
window.onload = function() {
    fetch('/')
    .then(response => response.json())
    .then(data => {
        displayHand(data.player_hand, 'player-hand');
        displayHand(data.dealer_hand, 'dealer-hand');
        displayHand(data.community_cards, 'community-cards');
        displayDeck(data.deck_card, 'deck');
    })
    .catch(error => {
        console.error('Errore:', error);
        alert('Si è verificato un errore durante il caricamento delle carte. Riprova.');
    });
};