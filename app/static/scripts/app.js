var images = document.querySelectorAll('img');
var deckActionButtons = document.querySelectorAll('.deck-action-button');
var decks = document.getElementById('decks');
var noDecksMessage = document.getElementById('no-decks');

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

if (decks.innerHTML.trim() === "") {
    noDecksMessage.style.display = "flex";
}