var menuButton = document.getElementById('menu-button');
var gridContainer = document.getElementById('grid-container');
var backgroundOverlay = document.getElementById('overlay-background');
var deckNav = document.getElementById('deck-navigation');
var decks = document.getElementById('decks');
var deckActionButtons = document.querySelectorAll('.deck-action-button');
var noDecksMessage = document.getElementById('no-decks');
var noCardsMessage = document.getElementById('no-cards');
var cardCanvas = document.getElementById('card-canvas');
var deck = document.getElementById('deck');
var changeViewButton = document.getElementById('change-view-button');
var addCardButton = document.getElementById('add-card-button');
var noDeckMessage = document.getElementById('no-deck');
var cards = document.getElementsByClassName('card');
var cardActionButtons = document.querySelectorAll('.card-action-button');
var cardForm = document.getElementById('card-form');
var closeCardFormButton = document.getElementById('close-card-form-button');
var grid = document.getElementById('cards-container');
var gridRowGap = parseInt(window.getComputedStyle(grid).getPropertyValue('grid-row-gap'));
var gridRowHeight = parseInt(window.getComputedStyle(grid).getPropertyValue('grid-auto-rows'));
var cardImageInput = document.getElementById('image-input-button');
var cardImageContainer = document.getElementsByClassName('card-image-container');
var cardImage = document.getElementById('preview-image');
var cardCloseImageButton = document.getElementById('close-image-button');
var cardTitle = document.getElementById('card-form-header');
var cardContent = document.getElementById('card-form-content');
var cardTitleArea = document.getElementsByClassName('card-title editable')[0];
var cardTextArea = document.getElementsByClassName('card-textarea editable')[0];
var cardActionButton = document.getElementsByClassName('card-action-button'); //5
var cardActionButtonContainer = document.getElementsByClassName('card-action-buttons-container');
var boldButton = document.getElementById('bold-button');
var underlineButton = document.getElementById('underline-button');
var italicButton = document.getElementById('italic-button');
var listButton = document.getElementById('list-button');
var regenGridOnElementResize = new ResizeObserver(generateGrid);

window.addEventListener('load', checkWindowWidth);
window.addEventListener('load', checkColumnCount);
window.addEventListener('load', generateGrid);
window.addEventListener('load', ifNoDecks);
window.addEventListener('load', ifNoCards);

window.addEventListener('resize', checkWindowWidth);
window.addEventListener('resize', checkColumnCount);
window.addEventListener('resize', generateGrid);

menuButton.addEventListener('click', toggleDeckNavigation);
menuButton.addEventListener('click', generateGrid);

addCardButton.addEventListener('click', openCardForm);
addCardButton.addEventListener('click', generateGrid);

closeCardFormButton.addEventListener('click', closeCardForm);
closeCardFormButton.addEventListener('click', generateGrid);

changeViewButton.addEventListener('click', toggleView);
changeViewButton.addEventListener('click', generateGrid);

changeViewButton.addEventListener('click', toggleView);
changeViewButton.addEventListener('click', generateGrid);

cardTitleArea.addEventListener('input', plainText);

boldButton.addEventListener('click', function () { document.execCommand('bold'); cardTextArea.focus();});
underlineButton.addEventListener('click', function () { document.execCommand('underline'); cardTextArea.focus();});
italicButton.addEventListener('click', function () { document.execCommand('italic'); cardTextArea.focus();});
listButton.addEventListener('click', function () { document.execCommand('insertUnorderedList'); cardTextArea.focus();});
cardImageInput.addEventListener('change', loadImage);

cardCloseImageButton.addEventListener('click', closeImage);

deckActionButtons.forEach(function(deckActionButton) {

    var actionButtonsContainer = deckActionButton.parentElement.querySelector('.deck-action-buttons-container');

    deckActionButton.addEventListener('click', function() {   
        
        if (window.getComputedStyle(actionButtonsContainer).display === "none") { 
            
            actionButtonsContainer.style.display = "flex";
            
        } else if (window.getComputedStyle(actionButtonsContainer).display === "flex") { 

            actionButtonsContainer.style.display = "none";   
        }
    });
});

cardActionButtons.forEach(function(cardActionButton) {

    var actionButtonsContainer = cardActionButton.parentElement.querySelector('.card-action-buttons-container');

    cardActionButton.addEventListener('click', function() {   
        
        if (window.getComputedStyle(actionButtonsContainer).display === "none") { 
            
            actionButtonsContainer.style.display = "flex";
            
        } else if (window.getComputedStyle(actionButtonsContainer).display === "flex") { 

            actionButtonsContainer.style.display = "none";   
        }
    });
});

window.addEventListener('click', function(event) {

    deckActionButtons.forEach(function(deckActionButton) {

        var actionButtonsContainer = deckActionButton.parentElement.querySelector('.deck-action-buttons-container');
    
        if (!(event.target === actionButtonsContainer) && !(event.target.parentElement === actionButtonsContainer) && !(event.target === deckActionButton) && !(event.target.parentElement === deckActionButton)) {
            actionButtonsContainer.style.display = "none";
        }
    
    });

    cardActionButtons.forEach(function(cardActionButton) {

        var actionButtonsContainer = cardActionButton.parentElement.querySelector('.card-action-buttons-container');
    
        if (!(event.target === actionButtonsContainer) && !(event.target.parentElement === actionButtonsContainer) && !(event.target === cardActionButton) && !(event.target.parentElement === cardActionButton)) {
            actionButtonsContainer.style.display = "none";
        }
    
    });
})

for (var index = 0; index < cards.length; index++) {
    regenGridOnElementResize.observe(cardImageContainer[index]);
}

regenGridOnElementResize.observe(cardTitle);
regenGridOnElementResize.observe(cardContent);


function ifNoDecks(){

    if (decks.childElementCount === 0) {
        noDecksMessage.style.display = "flex";
        noDeckMessage.style.display = "flex";
        deck.style.display = "none";
    }
}

function ifNoCards(){

    if (grid.childElementCount === 1) {
        noCardsMessage.style.display = "flex";
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

function resizeGridCards() {

    for (var index = 0; index < cards.length; index++) {

        var gridRowSpan = Math.ceil((cards[index].getBoundingClientRect().height + gridRowGap) / (gridRowHeight + gridRowGap));

        cards[index].style.gridRowEnd = 'span ' + gridRowSpan;
        cards[index].style.height = 'auto';
    }
}

function resetGridCardsHeight() {

    for (var index = 0; index < cards.length; index++) {
        cards[index].style.height = 'fit-content';
    }
}

function generateGrid() {
    resetGridCardsHeight();
    resizeGridCards();
}

function checkColumnCount() {

    var columnCount = window.getComputedStyle(grid).getPropertyValue("grid-template-columns").split(" ").length;

    if (columnCount === 1) {

        changeViewButton.querySelector('i').style.backgroundImage = "url('/static/assets/Grid-View-Icon.svg')";
        changeViewButton.querySelector('span').innerHTML = "Grid";

    } else if (columnCount > 1) {

        changeViewButton.querySelector('i').style.backgroundImage = "url('/static/assets/List-View-Icon.svg')";
        changeViewButton.querySelector('span').innerHTML = "List";
    }
}

function openCardForm() {
    
    cardForm.style.display = "flex";
    noCardsMessage.style.display = "none";
}

function closeCardForm() {

    cardForm.style.display = "none";
    ifNoCards();
}

function toggleView() {

    var columnCount = window.getComputedStyle(grid).getPropertyValue("grid-template-columns").split(" ").length;

    if (columnCount > 1) {

        deck.style.maxWidth = "616px";
        grid.style.gridTemplateColumns = "100%";

        checkColumnCount();

    } else if (columnCount === 1) {

        deck.style.maxWidth = "none";
        grid.style.gridTemplateColumns = "repeat(auto-fill, minmax(300px, 1fr))";

        checkColumnCount();
    }
}

function plainText() {

    cardTitleArea.innerHTML = cardTitleArea.innerHTML.replace(/(<([^>]+)>)/gi, "");
    var textSelected = window.getSelection();
    var selectionRange = document.createRange();

    textSelected.removeAllRanges();
    selectionRange.selectNodeContents(cardTitleArea);
    selectionRange.collapse(false);
    textSelected.addRange(selectionRange);
    cardTitleArea.focus();
}

function loadImage() {

    cardImage.style.display = "block";

    var file = cardImageInput.files[0];

    if (file) {
        cardImage.src = URL.createObjectURL(file);
        cardCloseImageButton.style.display = "block";
    }

}

function closeImage() {

    cardImageInput.value = null;
    cardImage.src = "";
    cardImage.style.display = "none";
    cardCloseImageButton.style.display = "none";
}