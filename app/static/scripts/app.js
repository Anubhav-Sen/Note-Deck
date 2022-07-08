var menuButton = document.getElementById('menu-button');
var profileMenuButton = document.getElementById('profile-menu-button');
var profileMenu = document.getElementById('profile-menu');
var gridContainer = document.getElementById('grid-container');
var backgroundOverlay = document.getElementById('overlay-background');
var deckNav = document.getElementById('deck-navigation');
var decks = document.getElementById('decks');
var deckActionButtons = document.querySelectorAll('.deck-action-button');
var updateDeckFormOverlay = document.getElementById('update-deck-form-background');
var updateDeckForm = document.getElementById('update-deck-form-container');
var updateDeckFormCloseButton = document.getElementById('update-deck-form-close-button');
var noDecksMessage = document.getElementById('no-decks');
var noCardsMessage = document.getElementById('no-cards');
var noResultsMessage = document.getElementById('no-results');
var cardCanvas = document.getElementById('card-canvas');
var deck = document.getElementById('deck');
var changeViewButton = document.getElementById('change-view-button');
var addCardButton = document.getElementById('add-card-button');
var noDeckMessage = document.getElementById('no-deck');
var searchedDecksContainer = document.getElementById('searched-decks-container');
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
var cardTitleInput = document.getElementById('card-title-input');
var cardTitleArea = document.getElementsByClassName('card-title editable')[0];
var cardContentInput = document.getElementById('card-content-input');
var cardTextArea = document.getElementsByClassName('card-textarea editable')[0];
var cardActionButton = document.getElementsByClassName('card-action-button');
var cardActionButtonContainer = document.getElementsByClassName('card-action-buttons-container');
var boldButton = document.getElementById('bold-button');
var underlineButton = document.getElementById('underline-button');
var italicButton = document.getElementById('italic-button');
var listButton = document.getElementById('list-button');
var regenGridOnElementResize = new ResizeObserver(generateGrid);
var meta = document.createElement('meta');

meta.name = 'viewport';
meta.content = 'width=device-width,height=' + window.innerHeight + ', initial-scale=1.0';
document.getElementsByTagName('head')[0].appendChild(meta);

window.addEventListener('load', checkWindowWidth);
window.addEventListener('load', checkColumnCount);
window.addEventListener('load', generateGrid);
window.addEventListener('load', ifNoDecks);
window.addEventListener('load', ifNoCards);
window.addEventListener('load', ifNoResults);
window.addEventListener('load', ifDeckEditing);
window.addEventListener('load', ifCardEditing);

window.addEventListener('resize', checkWindowWidth);
window.addEventListener('resize', checkColumnCount);
window.addEventListener('resize', generateGrid);
window.addEventListener('resize', displaceUpdateDeckForm)
window.addEventListener('resize', setCardCanvasHeight)

menuButton.addEventListener('click', toggleDeckNavigation);
menuButton.addEventListener('click', generateGrid);

profileMenuButton.addEventListener('click', toggleProfileMenu);

changeViewButton.addEventListener('click', toggleView);
changeViewButton.addEventListener('click', generateGrid);

deckActionButtons.forEach(function (deckActionButton) {

    var actionButtonsContainer = deckActionButton.parentElement.querySelector('.deck-action-buttons-container');

    deckActionButton.addEventListener('click', function () {

        if (window.getComputedStyle(actionButtonsContainer).display === "none") {

            actionButtonsContainer.style.display = "flex";

        } else if (window.getComputedStyle(actionButtonsContainer).display === "flex") {

            actionButtonsContainer.style.display = "none";
        }
    });
});

cardActionButtons.forEach(function (cardActionButton) {

    var actionButtonsContainer = cardActionButton.parentElement.querySelector('.card-action-buttons-container');

    cardActionButton.addEventListener('click', function () {

        if (window.getComputedStyle(actionButtonsContainer).display === "none") {

            actionButtonsContainer.style.display = "flex";

        } else if (window.getComputedStyle(actionButtonsContainer).display === "flex") {

            actionButtonsContainer.style.display = "none";
        }
    });
});

window.addEventListener('click', function (event) {

    deckActionButtons.forEach(function (deckActionButton) {

        var actionButtonsContainer = deckActionButton.parentElement.querySelector('.deck-action-buttons-container');

        if (!(event.target === actionButtonsContainer) && !(event.target.parentElement === actionButtonsContainer) && !(event.target === deckActionButton) && !(event.target.parentElement === deckActionButton)) {
            actionButtonsContainer.style.display = "none";
        }

    });

    cardActionButtons.forEach(function (cardActionButton) {

        var actionButtonsContainer = cardActionButton.parentElement.querySelector('.card-action-buttons-container');

        if (!(event.target === actionButtonsContainer) && !(event.target.parentElement === actionButtonsContainer) && !(event.target === cardActionButton) && !(event.target.parentElement === cardActionButton)) {
            actionButtonsContainer.style.display = "none";
        }

    });

    if (!(event.target === profileMenu) && !(event.target.parentElement === profileMenu) && !(event.target === profileMenuButton) && !(event.target.parentElement === profileMenuButton)) {

        profileMenu.style.display = "none";
    }

    if (!(event.target === deckNav) && !(deckNav.contains(event.target)) && !(event.target === menuButton) && !(event.target.parentElement === menuButton) && (window.innerWidth < 872)) {

        deckNav.style.display = "none";
        backgroundOverlay.style.display = "none";

    }

    if (!(event.target === updateDeckForm) && !(updateDeckForm.contains(event.target))) {

        updateDeckFormOverlay.style.display = "none";
        closeUpdateDeckForm()
    }

})

for (var index = 0; index < cards.length; index++) {
    regenGridOnElementResize.observe(cardImageContainer[index]);
}

addCardButton.addEventListener('click', openCardForm);
addCardButton.addEventListener('click', generateGrid);

closeCardFormButton.addEventListener('click', closeCardForm);
closeCardFormButton.addEventListener('click', generateGrid);

updateDeckFormCloseButton.addEventListener('click', closeUpdateDeckForm);

cardTitleArea.addEventListener('input', updateCardTitleInput);
cardTextArea.addEventListener('input', updateCardContentInput);

boldButton.addEventListener('click', function () { document.execCommand('bold'); cardTextArea.focus(); });
underlineButton.addEventListener('click', function () { document.execCommand('underline'); cardTextArea.focus(); });
italicButton.addEventListener('click', function () { document.execCommand('italic'); cardTextArea.focus(); });
listButton.addEventListener('click', function () { document.execCommand('insertUnorderedList'); cardTextArea.focus(); });

cardImageInput.addEventListener('change', loadImage);
cardCloseImageButton.addEventListener('click', closeImage);

regenGridOnElementResize.observe(cardTitle);
regenGridOnElementResize.observe(cardContent);

function updateCardTitleInput() {
    cardTitleInput.value = cardTitleArea.innerHTML.replace(/(<([^>]+)>)/gi, "");
}

function updateCardContentInput() {
    cardContentInput.value = cardTextArea.innerHTML;
}

function ifNoDecks() {

    if (decks.childElementCount === 0) {
        noDecksMessage.style.display = "flex";
        noDeckMessage.style.display = "flex";
        deck.style.display = "none";
    }
}

function ifNoCards() {

    if (grid.childElementCount === 1) {
        noCardsMessage.style.display = "flex";
    }
}

function ifNoResults() {

    if ((grid.childElementCount === 0) && (searchedDecksContainer.childElementCount === 0)) {
        noResultsMessage.style.display = "flex";
    }
}

function ifDeckEditing() {

    deckIdInput = document.getElementById('deck-id');
    deckFormError = document.getElementById('deck-form-error');
    updateDeckFormError = document.getElementById('update-deck-form-error');
    updateDeckFormTitleInput = document.querySelector('#update-deck-form-container input[type="text"]');

    if (deckIdInput.value.trim() != "") {
        updateDeckFormOverlay.style.display = "grid";
        updateDeckFormTitleInput.setSelectionRange(updateDeckFormTitleInput.value.length, updateDeckFormTitleInput.value.length)

        displaceUpdateDeckForm()
        updateDeckFormTitleInput.focus()
    }

    if ((deckIdInput.value.trim() != "") && (updateDeckFormError)) {
        updateDeckFormOverlay.style.display = "grid";
        updateDeckFormTitleInput.value = "";

        displaceUpdateDeckForm()
        updateDeckFormTitleInput.focus()
    }

    if ((deckFormError) && (window.innerWidth < 872)) {
        deckNav.style.display = "flex";
        backgroundOverlay.style.display = "block";
        backgroundOverlay.style.width = "calc(100vw - 272px)"
    }
}

function ifCardEditing() {

    cardIdInput = document.getElementById('card-id');

    if (cardIdInput.value.trim() != "") {
        cardForm.style.display = "flex";
    }
}

function checkWindowWidth() {

    if ((window.innerWidth < 872) && (document.querySelector('#deck-input-form input[type=text]') != document.activeElement)) {

        gridContainer.style.gridTemplateAreas = '"header header" "card-canvas card-canvas"';
        deckNav.style.display = "none";
        deckNav.style.gridArea = "none";
        deckNav.style.position = "absolute";
        deckNav.style.marginTop = "65px";
        backgroundOverlay.style.display = "none";
        cardCanvas.style.width = "100vw";

        if (addCardButton) {
            addCardButton.style.left = "32px";
        }

    } else if ((window.innerWidth < 872) && (document.querySelector('#deck-input-form input[type=text]') == document.activeElement)) {

        gridContainer.style.gridTemplateAreas = '"header header" "card-canvas card-canvas"';
        deckNav.style.display = "flex";
        deckNav.style.gridArea = "none";
        deckNav.style.position = "absolute";
        deckNav.style.marginTop = "65px";
        backgroundOverlay.style.display = "block";
        backgroundOverlay.style.width = "calc(100vw - 272px)";
        cardCanvas.style.width = "100vw";

        if (addCardButton) {
            addCardButton.style.left = "32px";
        }

    } else if (window.innerWidth > 872) {

        gridContainer.style.gridTemplateAreas = '"header header" "deck-nav card-canvas"';
        deckNav.style.display = "flex";
        deckNav.style.gridArea = "deck-nav";
        deckNav.style.position = "static";
        deckNav.style.marginTop = "0";  
        backgroundOverlay.style.display = "none";
        cardCanvas.style.width = "calc(100vw - 272px)";

        if (addCardButton) {
            addCardButton.style.left = "304px";
        }
    }

    if (window.innerWidth < 400) {

        if (addCardButton) {
            addCardButton.style.left = "16px";
        }
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

        if (addCardButton) {
            addCardButton.style.left = "32px";
        }

    } else if ((window.getComputedStyle(deckNav).getPropertyValue('display') === "none") && (window.innerWidth < 872)) {

        deckNav.style.display = "flex";
        backgroundOverlay.style.display = "block";
        backgroundOverlay.style.width = "calc(100vw - 272px)";
        cardCanvas.style.width = "100vw";

    } else if ((window.getComputedStyle(deckNav).getPropertyValue('display') === "none") && (window.innerWidth > 872)) {

        deckNav.style.display = "flex";
        cardCanvas.style.width = "calc(100vw - 272px)";

        if (addCardButton) {
            addCardButton.style.left = "304px";
        }

    }

    if ((window.getComputedStyle(deckNav).getPropertyValue('display') === "flex") && (window.innerWidth < 968) && (window.innerWidth > 872)) {

        changeViewButton.style.display = "none";

    } else if ((window.getComputedStyle(deckNav).getPropertyValue('display') === "none") && (window.innerWidth < 968) && (window.innerWidth > 872)) {

        changeViewButton.style.display = "flex";

    } else if ((window.getComputedStyle(deckNav).getPropertyValue('display') === "flex") && (window.innerWidth > 968)) {

        changeViewButton.style.display = "flex";

    } else if ((window.getComputedStyle(deckNav).getPropertyValue('display') === "none") && (window.innerWidth > 968)) {

        changeViewButton.style.display = "flex";

    }
}

function toggleProfileMenu() {

    if (window.getComputedStyle(profileMenu).getPropertyValue('display') === "none") {

        profileMenu.style.display = "flex"

    } else if (window.getComputedStyle(profileMenu).getPropertyValue('display') === "flex") {

        profileMenu.style.display = "none"

    }
}

function setCardCanvasHeight() {
    cardCanvas.style.height = "" + (window.innerHeight - 64) + "px";
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
    noCardsMessage.style.display = "none"
    cardTitleArea.focus();
}

function closeCardForm() {

    cardFormInputs = document.querySelectorAll("#card-input-form input");

    cardForm.style.display = "none";

    cardTitleArea.innerHTML = "";
    cardTextArea.innerHTML = "";

    cardFormInputs.forEach(function (input) {
        input.value = "";
    });

    ifNoCards();
}

function closeUpdateDeckForm() {

    updateDeckFormInputs = document.querySelectorAll("#update-deck-form input");

    updateDeckFormOverlay.style.display = "none";

    updateDeckFormInputs.forEach(function (input) {
        input.value = "";
    });
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

function displaceUpdateDeckForm() {

    updateDeckForm.style.top = "" + (((window.innerHeight - 64)/2) - (updateDeckForm.getBoundingClientRect().height/2)) + "px";

}