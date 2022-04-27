from flask import Blueprint, render_template, redirect, url_for, abort
from app.dummydata import username, decks, cards

blueprint = Blueprint('deck_pages', __name__)

@blueprint.route('/')
def index():
    if len(decks) == 0:
        return redirect(url_for('deck_pages.getStarted'))
    elif len(decks) > 0:
        return redirect(url_for('deck_pages.noteDeck', deck = decks[0]["deck_title"], deck_id = decks[0]["deck_id"], color = decks[0]["deck_color"]))

@blueprint.route('/decks/<deck>/<deck_id>/<color>')
def noteDeck(deck, deck_id, color):

    cardlist = []

    if len(decks) == 0:
        return abort(404)
    elif len(decks) > 0:
        for card in cards: 
            if card["deck_id"] == deck_id:
                cardlist.append(card)
                
        return render_template('note-deck.html', page_title = deck, decks = decks, deck_id = deck_id, username = username, color = color, cards = cardlist)

@blueprint.route('/get-started')
def getStarted():
    return render_template('note-deck.html', page_title = "Get-started", decks = decks, deck_id = "#", username = username, color = "#", cards = "")

