from flask import Blueprint, render_template, redirect, request, url_for, abort, jsonify
from .models import Deck, Card, Image
from app.extensions.database import db
import logging

username = 'Dwight'

blueprint = Blueprint('deck_pages', __name__)

@blueprint.route('/')
def index():

    deck_count = Deck.query.count()
    first_deck = Deck.query.first()

    if deck_count == 0:
        return redirect(url_for('deck_pages.get_getStarted'))

    elif deck_count > 0:
        return redirect(url_for('deck_pages.get_noteDeck',  
        deck_id=first_deck.id, 
        deck_title=first_deck.title, 
        deck_color=first_deck.color))

@blueprint.get('/decks/<int:deck_id>/<deck_title>/<deck_color>')
def get_noteDeck(deck_id, deck_title, deck_color):

    decks = Deck.query.all()
    deck_count = Deck.query.count()
    current_deck = Deck.query.filter_by(id=deck_id).first()
    cards = Card.query.filter_by(deck_id=deck_id)
    deck_form_error = request.args.get('deck_form_error')
    update_deck = {'id': request.args.get('update_deck_id'), 'title': request.args.get('update_deck_title'), 'color': request.args.get('update_deck_color')}
    
    if current_deck == None:
        logging.warning("Url dosen't exist1")
        return redirect(url_for('deck_pages.index'))

    elif current_deck.title != deck_title or current_deck.color != deck_color:
        logging.warning("Url dosen't exist1")
        return abort(400)

    elif deck_count == 0:
        logging.warning(f"Url dosen't exist!")
        return abort(404)

    elif len(decks) > 0:

        return render_template('note-deck.html', 
        username=username, 
        decks=decks, 
        deck_id=deck_id, 
        deck_title=deck_title, 
        deck_color=deck_color, 
        cards=cards, 
        deck_form_error=deck_form_error, 
        current_deck = current_deck,
        update_deck = update_deck)

@blueprint.post('/decks/<int:deck_id>/<deck_title>/<deck_color>')
def post_noteDeck(deck_id, deck_title, deck_color):

    current_deck = Deck.query.filter_by(id=deck_id).first()

    if 'deck-form' in request.form:

        deck_id_data = request.form['id'] or None
        deck_title_data = request.form['title'] or None
        deck_color_data = request.form['color'] or None
        update_deck = {'id': request.args.get('update_deck_id'), 'title': request.args.get('update_deck_title'), 'color': request.args.get('update_deck_color')}

        if deck_title_data != None and deck_color_data != None and deck_id_data == None:
            new_deck = Deck(title=deck_title_data, color=deck_color_data)
            new_deck.save()

            return redirect(url_for('deck_pages.get_noteDeck',  
            deck_id=deck_id, 
            deck_title=deck_title, 
            deck_color=deck_color))
                
        elif deck_title_data != None and deck_color_data != None and deck_id_data != None:
            deck = Deck.query.filter_by(id = update_deck['id']).first()
            
            deck.title = request.form['title']
            deck.color = request.form['color']
            deck.save()

            return redirect(url_for('deck_pages.get_noteDeck',  
            deck_id=current_deck.id, 
            deck_title=current_deck.title, 
            deck_color=current_deck.color))

        elif deck_title_data != None or deck_color_data != None:

            error_message = "Please fill the deck title"
            return redirect(url_for('deck_pages.get_noteDeck',  
            deck_id=deck_id, 
            deck_title=deck_title, 
            deck_color=deck_color, 
            deck_form_error=error_message))


@blueprint.route('/delete-deck/<int:deck_id>/<int:current_deck_id>')
def deleteDeck(deck_id, current_deck_id):

    deck_count = Deck.query.count()
    first_deck = Deck.query.first()
    current_deck = Deck.query.filter_by(id = current_deck_id).first()
    deck = Deck.query.filter_by(id=deck_id).first()

    if deck == None:
        logging.warning("Tried to delete non existent deck.")
        return abort(400)

    elif deck != None:
        deck.delete()

    if request.referrer == url_for('deck_pages.get_noteDeck', deck_id=deck.id, deck_title=deck.title, deck_color=deck.color) and deck_count > 0:
        return redirect(url_for('deck_pages.get_noteDeck',  
        deck_id=first_deck.id, deck_title=first_deck.title, 
        deck_color=first_deck.color))

    elif request.referrer == url_for('deck_pages.get_noteDeck', deck_id=deck.id, deck_title=deck.title, deck_color=deck.color) and deck_count == 0:
        return redirect(url_for('deck_pages.get_get_started'))

    elif request.referrer != url_for('deck_pages.get_noteDeck', deck_id=deck.id, deck_title=deck.title, deck_color=deck.color):
        return redirect(url_for('deck_pages.get_noteDeck',  
        deck_id=current_deck.id, 
        deck_title=current_deck.title, 
        deck_color=current_deck.color))

@blueprint.route('/update-deck/<int:deck_id>/<int:current_deck_id>')
def updateDeck(deck_id, current_deck_id):

    current_deck = Deck.query.filter_by(id = current_deck_id).first()
    update_deck = Deck.query.filter_by(id=deck_id).first()
    
    return update_deck and redirect(url_for('deck_pages.get_noteDeck',  
    deck_id=current_deck.id, deck_title=current_deck.title,
    deck_color=current_deck.color, update_deck_id = update_deck.id, update_deck_title= update_deck.title, update_deck_color= update_deck.color))

@blueprint.get('/get-started')
def get_getStarted():

    deck_count = Deck.query.count()

    deck_form_error = request.args.get('deck_form_error')

    if deck_count == 0:
        return render_template('note-deck.html', 
        username=username, 
        decks='', 
        deck_id='#', 
        deck_title='Get-Started', 
        deck_color='#', 
        cards='',
        deck_form_error = deck_form_error,
        update_deck = None,)

    elif deck_count > 0:
        return abort(404)

@blueprint.post('/get-started')
def post_getStarted():

    deck_id_data = request.form['id'] or None
    deck_title_data = request.form['title'] or None
    deck_color_data = request.form['color'] or None
    
    if deck_title_data != None and deck_color_data != None and deck_id_data == None:
        new_deck = Deck(title=deck_title_data, color=deck_color_data)
        new_deck.save()

        return redirect(url_for('deck_pages.get_noteDeck',  
        deck_id=new_deck.id, 
        deck_title=new_deck.title, 
        deck_color=new_deck.color))
            
    elif deck_title_data != None or deck_color_data != None:

        error_message = "Please fill the deck title"
        return redirect(url_for('deck_pages.get_getStarted', deck_form_error=error_message))
