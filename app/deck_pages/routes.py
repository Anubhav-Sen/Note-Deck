from flask import Blueprint, render_template, redirect, url_for, abort
from app.dummydata import username, decks

blueprint = Blueprint('deck_pages', __name__)

@blueprint.route('/')
def index():
    if len(decks) == 0:
        return redirect(url_for('deck_pages.getStarted'))
    elif len(decks) > 0:
        return redirect(url_for('deck_pages.noteDeck', deck = decks[0]["deck_title"], color = decks[0]["deck_color"]))

@blueprint.route('/decks/<deck>/<color>')
def noteDeck(deck, color):
    if len(decks) == 0:
        return abort(404)
    elif len(decks) > 0:
        return render_template('note-deck.html', page_title = deck, decks = decks, username = username, color = color)

@blueprint.route('/get-started')
def getStarted():
    return render_template('note-deck.html', page_title = "Get-started", decks = decks, username = username, color = "#")

