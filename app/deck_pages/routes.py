from flask import Blueprint, render_template, redirect, url_for, abort
from .models import Deck, Card, Image
import logging

username = 'Dwight'
cards = []

blueprint = Blueprint('deck_pages', __name__)

@blueprint.route('/')
def index():

    deck_count = Deck.query.count()
    first_deck = Deck.query.first()
    
    if deck_count == 0:
        return redirect(url_for('deck_pages.getStarted'))

    elif deck_count > 0:
        return redirect(url_for('deck_pages.noteDeck',  deck_id = first_deck.id , deck_title = first_deck.title, deck_color = first_deck.color))


@blueprint.route('/decks/<deck_id>/<deck_title>/<deck_color>')
def noteDeck(deck_id, deck_title, deck_color):
    
    decks = Deck.query.all()
    deck_count = Deck.query.count()
    cards = Card.query.filter_by(deck_id = deck_id)
    images = Image.query.all()

    if deck_count == 0:
        logging.warning(f"{deck_title} dosen't exist!")
        return abort(404)

    elif len(decks) > 0:
        return render_template('note-deck.html', username = username, decks = decks, deck_id = deck_id, deck_title = deck_title, deck_color = deck_color, cards = cards, images = images)

@blueprint.route('/get-started')
def getStarted():
    
    deck_count = Deck.query.count()

    if deck_count == 0:
        return render_template('note-deck.html', username = username, decks = '', deck_id = '#', deck_title = 'Get-Started', deck_color = '#', cards = '', images='')

    elif deck_count > 0:
        return abort(404)