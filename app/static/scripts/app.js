var menuButton = document.getElementById('menu-button');

var gridContainer = document.getElementById('grid-container');
var backgroundOverlay = document.getElementById('overlay-background');

var deckNav = document.getElementById('deck-navigation');
var decks = document.getElementById('decks');
var deckActionButtons = document.querySelectorAll('.deck-action-button');
var noDecksMessage = document.getElementById('no-decks');

var cardCanvas = document.getElementById('card-canvas');
var deck = document.getElementById('deck');
var changeViewButton = document.getElementById('change-view-button');
var addCardButton = document.getElementById('add-card-button');
var noDeckMessage = document.getElementById('no-deck');

window.addEventListener('load', checkWindowWidth);
window.addEventListener('load', ifNoDecks);

window.addEventListener('resize', checkWindowWidth);

menuButton.addEventListener('click', toggleDeckNavigation);

deckActionButtons.forEach(function(deckActionButton) {

    var actionButtonsContainer = deckActionButton.parentElement.querySelector('.action-buttons-container');

    deckActionButton.addEventListener('click', function() {   
        
        if (window.getComputedStyle(actionButtonsContainer).display === "none") { 
            
            actionButtonsContainer.style.display = "flex";
            
        } else if (window.getComputedStyle(actionButtonsContainer).display === "flex") { 

            actionButtonsContainer.style.display = "none";   
        }
    });
});

window.addEventListener('click', function(event) {

    deckActionButtons.forEach(function(deckActionButton) {

        var actionButtonsContainer = deckActionButton.parentElement.querySelector('.action-buttons-container');
    
        if (!(event.target === actionButtonsContainer) && !(event.target.parentElement === actionButtonsContainer) && !(event.target === deckActionButton) && !(event.target.parentElement === deckActionButton)) {
            actionButtonsContainer.style.display = "none";
        }
    
    });
})

function ifNoDecks(){

    if (decks.innerHTML.trim() === "") {
        noDecksMessage.style.display = "flex";
        noDeckMessage.style.display = "flex";
        deck.style.display = "none";
    }
}

function checkWindowWidth() {

    if (window.innerWidth < 872) {

        gridContainer.style.gridTemplateAreas = '"header header" "card-canvas card-canvas"';
        deckNav.style.display = "none";
        deckNav.style.gridArea = "none";
        deckNav.style.position = "absolute";
        deckNav.style.marginTop = "65px";
        backgroundOverlay.style.display = "none";
        cardCanvas.style.width = "100vw";
        addCardButton.style.left = "32px";

    } else if (window.innerWidth > 872) {

        gridContainer.style.gridTemplateAreas = '"header header" "deck-nav card-canvas"';
        deckNav.style.display = "flex";
        deckNav.style.gridArea = "deck-nav";
        deckNav.style.position = "static";
        deckNav.style.marginTop = "0";
        cardCanvas.style.width = "calc(100vw - 272px)";
        addCardButton.style.left = "304px";

    }

    if (window.innerWidth < 400) {

        addCardButton.style.left = "16px";
    }

    if ((window.getComputedStyle(deckNav).getPropertyValue('display') === "flex") && (window.innerWidth < 968)) {

        changeViewButton.style.display = "none";

    } else if ((window.getComputedStyle(deckNav).getPropertyValue('display') === "none") && (window.innerWidth < 968)) {

        changeViewButton.style.display = "flex";

    } else if ((window.getComputedStyle(deckNav).getPropertyValue('display') === "flex") && (window.innerWidth > 968)) {

        changeViewButton.style.display = "flex";

    } else if ((window.getComputedStyle(deckNav).getPropertyValue('display') === "none") && (window.innerWidth > 968)) {

        changeViewButton.style.display = "flex";

    }

    if ((window.getComputedStyle(deckNav).getPropertyValue('display') === "none") && (window.innerWidth < 696)) {

        changeViewButton.style.display = "none";

    } else if ((window.getComputedStyle(deckNav).getPropertyValue('display') === "none") && (window.innerWidth > 696)) {

        changeViewButton.style.display = "flex";
    }
}

function toggleDeckNavigation() {

    if ((window.getComputedStyle(deckNav).getPropertyValue('display') === "flex") && (window.innerWidth < 872)) {

        deckNav.style.display = "none";
        backgroundOverlay.style.display = "none";
        cardCanvas.style.width = "100vw";

    } else if ((window.getComputedStyle(deckNav).getPropertyValue('display') === "flex") && (window.innerWidth > 872)) {

        deckNav.style.display = "none";
        backgroundOverlay.style.display = "none";
        cardCanvas.style.width = "100vw";
        addCardButton.style.left = "32px";

    } else if ((window.getComputedStyle(deckNav).getPropertyValue('display') === "none") && (window.innerWidth < 872)) {

        deckNav.style.display = "flex";
        backgroundOverlay.style.display = "block";
        backgroundOverlay.style.width = "calc(100vw - 272px)";
        cardCanvas.style.width = "100vw";

    } else if ((window.getComputedStyle(deckNav).getPropertyValue('display') === "none") && (window.innerWidth > 872)) {

        deckNav.style.display = "flex";
        cardCanvas.style.width = "calc(100vw - 272px)";
        addCardButton.style.left = "304px";

    }

    if ((window.getComputedStyle(deckNav).getPropertyValue('display') === "flex") && (window.innerWidth < 968)) {

        changeViewButton.style.display = "none";

    } else if ((window.getComputedStyle(deckNav).getPropertyValue('display') === "none") && (window.innerWidth < 968)) {

        changeViewButton.style.display = "flex";

    } else if ((window.getComputedStyle(deckNav).getPropertyValue('display') === "flex") && (window.innerWidth > 968)) {

        changeViewButton.style.display = "flex";

    } else if ((window.getComputedStyle(deckNav).getPropertyValue('display') === "none") && (window.innerWidth > 968)) {

        changeViewButton.style.display = "flex";

    }
}