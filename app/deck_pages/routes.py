from flask import Blueprint, render_template, redirect, url_for
from app.dummydata import username, decks

blueprint = Blueprint('deck_pages', __name__)

@blueprint.route('/')
def index():
    if len(decks) == 0:
        return redirect(url_for('deck_pages.noteDeck', deck = "get-started"))
    elif len(decks) > 0:
        return redirect(url_for('deck_pages.noteDeck', deck = decks[0]["deck_title"]))

@blueprint.route('/decks/<deck>')
def noteDeck(deck):
    return render_template('note-deck.html', deck_title = deck, decks = decks, username = username)