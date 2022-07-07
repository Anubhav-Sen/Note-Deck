from flask import Blueprint, render_template, redirect, request, url_for, abort
from .models import Deck, Card, Image
from app.extensions.database import db
import logging
import base64
from sqlalchemy import and_, or_
from flask_login import login_required, current_user

blueprint = Blueprint('deck_pages', __name__)

@blueprint.route('/')
def index():

    if current_user.is_authenticated:

        deck_count = Deck.query.filter_by(user_id = current_user.id).count()
        first_deck = Deck.query.filter_by(user_id = current_user.id).first()
        
        if deck_count == 0:
            return redirect(url_for('deck_pages.get_getStarted'))
            
        elif deck_count > 0:
            return redirect(url_for('deck_pages.get_noteDeck',  
            deck_id=first_deck.id, 
            deck_title=first_deck.title, 
            deck_color=first_deck.color))

    else:

        return redirect(url_for('users.get_login'))

@blueprint.get('/decks/<int:deck_id>/<deck_title>/<deck_color>')
@login_required
def get_noteDeck(deck_id, deck_title, deck_color):

    decks = Deck.query.filter_by(user_id = current_user.id).all()
    deck_count = Deck.query.filter_by(user_id = current_user.id).count()
    current_deck = Deck.query.filter_by(id=deck_id).first()
    cards = Card.query.filter_by(deck_id=deck_id).order_by(Card.date_created.desc())
    deck_form_error = request.args.get('deck_form_error')
    update_deck_form_error = request.args.get('update_deck_form_error')
    update_deck_id = request.args.get('update_deck_id')
    update_deck = Deck.query.filter_by(id = update_deck_id).first()
    update_card_id = request.args.get('update_card_id')
    update_card = Card.query.filter_by(id = update_card_id).first()
    update_card_image_id = request.args.get('update_card_image_id')
    update_card_image = Image.query.filter_by(id = update_card_image_id).first()

    if current_deck == None:
        logging.warning("Url dosen't exist1")
        return redirect(url_for('deck_pages.index'))

    elif current_deck.title != deck_title or current_deck.color != deck_color:
        logging.warning("Url dosen't exist!")
        return abort(400)

    elif deck_count == 0:
        logging.warning(f"Url dosen't exist!")
        return abort(404)

    elif current_deck.user_id != current_user.id:
        logging.warning("Tried to access another users deck.")
        return abort(401)

    elif len(decks) > 0 and current_deck.user_id == current_user.id:

        return render_template('note-deck.html',  
        decks=decks, 
        deck_id=deck_id, 
        deck_title=deck_title, 
        deck_color=deck_color, 
        cards=cards, 
        deck_form_error=deck_form_error,
        update_deck_form_error=update_deck_form_error,
        current_deck = current_deck,
        update_deck = update_deck,
        update_card = update_card,
        update_card_image = update_card_image)

@blueprint.post('/decks/<int:deck_id>/<deck_title>/<deck_color>')
@login_required
def post_noteDeck(deck_id, deck_title, deck_color):

    current_deck = Deck.query.filter_by(id=deck_id).first()

    if 'deck-form' in request.form:

        deck_title_data = request.form['title'] or None
        deck_color_data = request.form['color'] or None
                
        if deck_title_data != None and deck_color_data != None:
            new_deck = Deck(title=deck_title_data, color=deck_color_data, user_id=current_user.id)
            new_deck.save()

            return redirect(url_for('deck_pages.get_noteDeck',  
            deck_id=new_deck.id, 
            deck_title=new_deck.title, 
            deck_color=new_deck.color))

        elif deck_title_data == None or deck_color_data == None:

            error_message = "*please give your deck a title"
            return redirect(url_for('deck_pages.get_noteDeck',  
            deck_id=deck_id, 
            deck_title=deck_title, 
            deck_color=deck_color, 
            deck_form_error=error_message))

    elif 'update-deck-form' in request.form:

        deck_id_data = request.form['id'] or None
        deck_title_data = request.form['title'] or None
        deck_color_data = request.form['color'] or None
        update_deck_id = request.args.get('update_deck_id')
                                
        if deck_title_data != None and deck_color_data != None and deck_id_data != None:
            update_deck = Deck.query.filter_by(id = update_deck_id).first()
            
            update_deck.title = request.form['title']
            update_deck.color = request.form['color']
            update_deck.save()  

            return redirect(url_for('deck_pages.get_noteDeck',  
            deck_id=current_deck.id, 
            deck_title=current_deck.title, 
            deck_color=current_deck.color))

        elif deck_title_data == None or deck_color_data == None: 

            error_message = "*please give your deck a title"
            return redirect(url_for('deck_pages.get_noteDeck',  
            deck_id=deck_id, 
            deck_title=deck_title, 
            deck_color=deck_color, 
            update_deck_id = deck_id_data,
            update_deck_form_error=error_message))
    
    elif 'card-form' in request.form:
        
        card_id_data = request.form['id'] or None
        card_image_data = request.files['image']
        card_title_data = request.form['title'] or None
        card_content_data = request.form['content'] or None
        update_card_id = request.args.get('update_card_id')
        update_card_image_id = request.args.get('update_card_image_id')

        if card_title_data == None and card_image_data.filename == "" and card_content_data == None:
            return redirect(url_for('deck_pages.get_noteDeck',  
            deck_id=deck_id, 
            deck_title=deck_title, 
            deck_color=deck_color))
    
        elif card_id_data == None:
            new_card = Card(title=card_title_data, content=card_content_data, deck_id=current_deck.id)
            new_card.save()

            if card_image_data.filename:
                card_image_base64 = base64.b64encode(card_image_data.read()).decode('utf8')
                new_card_image = Image(data = card_image_base64, extention = card_image_data.mimetype, card_id = new_card.id)
                new_card_image.save()

            return redirect(url_for('deck_pages.get_noteDeck',  
            deck_id=deck_id, 
            deck_title=deck_title, 
            deck_color=deck_color))

        elif card_id_data != None:
            update_card = Card.query.filter_by(id = update_card_id).first()
            update_image = Image.query.filter_by(id = update_card_image_id).first() or None
            
            update_card.title = request.form['title']
            update_card.content = request.form['content']
            update_card.save()

            if card_image_data.filename and update_image:
                update_image.data = base64.b64encode(request.files['image'].read()).decode('utf8')
                update_image.extention = request.files['image'].mimetype
                update_image.save()

            elif card_image_data.filename:
                card_image_base64 = base64.b64encode(card_image_data.read()).decode('utf8')
                new_card_image = Image(data = card_image_base64, extention = card_image_data.mimetype, card_id = update_card_id)
                new_card_image.save()
                
            return redirect(url_for('deck_pages.get_noteDeck',  
            deck_id=deck_id, 
            deck_title=deck_title, 
            deck_color=deck_color))

    elif 'search-form' in request.form:
        search_term = request.form['search-term'].strip() or None

        if search_term != None:
            return redirect(url_for('deck_pages.get_search', current_deck_id = current_deck.id, search_term = search_term)) 
        
        elif search_term == None:
            return redirect(url_for('deck_pages.get_noteDeck',  
            deck_id=deck_id, 
            deck_title=deck_title, 
            deck_color=deck_color))

@blueprint.route('/delete-deck/<int:deck_id>/<int:current_deck_id>')
@login_required
def deleteDeck(deck_id, current_deck_id):

    deck_count = Deck.query.filter_by(user_id = current_user.id).count()
    first_deck = Deck.query.filter_by(user_id = current_user.id).first()
    current_deck = Deck.query.filter_by(id = current_deck_id).first()
    deck = Deck.query.filter_by(id=deck_id).first()

    if deck == None:
        logging.warning("Tried to delete non existent deck.")
        return abort(400)

    elif deck != None:
        
        if deck.user_id == current_user.id:
            deck.delete()

        else:
            logging.warning("Tried to delete another users deck.")
            return abort(401)

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

@blueprint.route('/delete-card/<int:card_id>/<int:current_deck_id>')
@login_required
def deleteCard(card_id, current_deck_id):
    
    current_deck = Deck.query.filter_by(id = current_deck_id).first()
    deck_ids = []
    
    for deck_id in db.session.query(Deck.id).filter(Deck.user_id == current_user.id).all():
        deck_ids.append(deck_id[0])

    card = Card.query.filter_by(id=card_id).first()
 
    if card == None:
        logging.warning("Tried to delete non existent card.")
        return abort(400)

    elif card != None:

        if card.deck_id in deck_ids:
            card.delete()

        else:
            logging.warning("Tried to delete another users card.")
            return abort(401)

    return redirect(url_for('deck_pages.get_noteDeck',  
        deck_id=current_deck.id, 
        deck_title=current_deck.title, 
        deck_color=current_deck.color))

@blueprint.route('/update-deck/<int:deck_id>/<int:current_deck_id>')
@login_required
def updateDeck(deck_id, current_deck_id):

    current_deck = Deck.query.filter_by(id = current_deck_id).first()
    update_deck = Deck.query.filter_by(id=deck_id).first()

    if update_deck == None:
        logging.warning("Tried to update non existent deck.")
        return abort(400)
    
    elif update_deck.user_id != current_user.id:
        logging.warning("Tried to update another users deck.")
        return abort(401)
    
    return redirect(url_for('deck_pages.get_noteDeck',  
    deck_id=current_deck.id, 
    deck_title=current_deck.title,
    deck_color=current_deck.color, 
    update_deck_id = update_deck.id))

@blueprint.route('/update-card/<int:card_id>/<int:current_deck_id>')
@login_required
def updateCard(card_id, current_deck_id):
    
    current_deck = Deck.query.filter_by(id = current_deck_id).first()
    deck_ids = []
    
    for deck_id in db.session.query(Deck.id).filter(Deck.user_id == current_user.id).all():
        deck_ids.append(deck_id[0])
    
    update_card = Card.query.filter_by(id=card_id).first()
    update_card_image = Image.query.filter_by(card_id = card_id).first()

    if update_card == None:
        logging.warning("Tried to update non existent card.")
        return abort(400)

    elif update_card.deck_id not in deck_ids:
        logging.warning("Tried to update another users card.")
        return abort(401)

    if update_card_image:
        return redirect(url_for('deck_pages.get_noteDeck',  
        deck_id=current_deck.id, 
        deck_title=current_deck.title,
        deck_color=current_deck.color, 
        update_card_id = update_card.id,
        update_card_image_id = update_card_image.id))
    
    elif not update_card_image:
        return redirect(url_for('deck_pages.get_noteDeck',  
        deck_id=current_deck.id, 
        deck_title=current_deck.title,
        deck_color=current_deck.color, 
        update_card_id = update_card.id))


@blueprint.get('/search/<int:current_deck_id>/<search_term>')
@login_required
def get_search(current_deck_id, search_term):

    search_term = search_term
    decks = Deck.query.filter_by(user_id = current_user.id).all()
    searched_decks = Deck.query.filter(Deck.title.like(f"%{search_term}%")).order_by(Deck.date_created.desc()).all()
    deck_ids = []
    
    for deck_id in db.session.query(Deck.id).filter(Deck.user_id == current_user.id).all():
        deck_ids.append(deck_id[0])
    
    cards = Card.query.filter(and_((Card.deck_id.in_(deck_ids)), (or_(Card.title.like(f"%{search_term}%"), Card.content.like(f"%{search_term}%"))))).order_by(Card.date_created.desc()).all()
    current_deck = Deck.query.filter_by(id = current_deck_id).first()
    deck_form_error = request.args.get('deck_form_error')
    update_deck_form_error = request.args.get('update_deck_form_error')
    update_deck_id = request.args.get('update_deck_id')
    update_deck = Deck.query.filter_by(id = update_deck_id).first()
    update_card_id = request.args.get('update_card_id') 
    update_card = Card.query.filter_by(id = update_card_id).first()
    update_card_image_id = request.args.get('update_card_image_id')
    update_card_image = Image.query.filter_by(id = update_card_image_id).first()

    if current_deck.user_id != current_user.id:
        logging.warning("User another users deck id.")
        return abort(401)
 
    return render_template('note-deck-search.html',  
        decks=decks,
        searched_decks = searched_decks,
        deck_id='#', 
        search_term = search_term,
        search_title=f'Search "{search_term}"', 
        deck_color='#',
        current_deck=current_deck, 
        cards=cards, 
        deck_form_error=deck_form_error,
        update_deck_form_error=update_deck_form_error,
        update_deck = update_deck,
        update_card = update_card,
        update_card_image = update_card_image)  


@blueprint.post('/search/<int:current_deck_id>/<search_term>')
@login_required
def post_search(current_deck_id, search_term):

    current_deck = Deck.query.filter_by(id=current_deck_id).first()

    if 'deck-form' in request.form:

        deck_title_data = request.form['title'] or None
        deck_color_data = request.form['color'] or None
                
        if deck_title_data != None and deck_color_data != None:
            new_deck = Deck(title=deck_title_data, color=deck_color_data, user_id=current_user.id)
            new_deck.save()

            return redirect(url_for('deck_pages.get_noteDeck',  
            deck_id=new_deck.id, 
            deck_title=new_deck.title, 
            deck_color=new_deck.color))

        elif deck_title_data == None or deck_color_data == None:

            error_message = "*please give your deck a title"
            return redirect(url_for('deck_pages.get_noteDeck',  
            deck_id=current_deck.id, 
            deck_title=current_deck.title, 
            deck_color=current_deck.color, 
            deck_form_error=error_message))

    elif 'update-deck-form' in request.form:

        deck_id_data = request.form['id'] or None
        deck_title_data = request.form['title'] or None
        deck_color_data = request.form['color'] or None
        update_deck_id = request.args.get('update_deck_id')
                                
        if deck_title_data != None and deck_color_data != None and deck_id_data != None:
            update_deck = Deck.query.filter_by(id = update_deck_id).first()
            
            update_deck.title = request.form['title']
            update_deck.color = request.form['color']
            update_deck.save()

            return redirect(url_for('deck_pages.get_noteDeck',  
            deck_id=current_deck.id, 
            deck_title=current_deck.title, 
            deck_color=current_deck.color))

        elif deck_title_data == None or deck_color_data == None: 

            error_message = "*please give your deck a title"
            return redirect(url_for('deck_pages.get_noteDeck',  
            deck_id=current_deck.id, 
            deck_title=current_deck.title, 
            deck_color=current_deck.color, 
            update_deck_id = deck_id_data,
            update_deck_form_error=error_message))  

    elif 'search-form' in request.form:
        search_term = request.form['search-term'].strip() or None

        print(search_term)

        if search_term != None:
            return redirect(url_for('deck_pages.get_search', current_deck_id = current_deck.id, search_term = search_term)) 
        
        elif search_term == None:
            return redirect(url_for('deck_pages.get_noteDeck',  
            deck_id=current_deck.id, 
            deck_title=current_deck.title, 
            deck_color=current_deck.color))

@blueprint.get('/get-started')
@login_required
def get_getStarted():

    deck_count = Deck.query.filter_by(user_id = current_user.id).count()

    deck_form_error = request.args.get('deck_form_error')   

    if deck_count == 0:
        return render_template('note-deck.html', 
        decks='', 
        deck_id='#', 
        deck_title='Get-Started', 
        deck_color='#', 
        cards='',
        deck_form_error=deck_form_error,
        update_deck = None,
        update_card = None,
        update_card_image = None)

    elif deck_count > 0:
        return abort(404)

@blueprint.post('/get-started')
@login_required
def post_getStarted():

    deck_title_data = request.form['title'] or None
    deck_color_data = request.form['color'] or None
    
    if deck_title_data != None and deck_color_data != None:
        new_deck = Deck(title=deck_title_data, color=deck_color_data, user_id=current_user.id)
        new_deck.save()

        return redirect(url_for('deck_pages.get_noteDeck',  
        deck_id=new_deck.id, 
        deck_title=new_deck.title, 
        deck_color=new_deck.color))
            
    elif deck_title_data != None:

        error_message = "*please give your deck a title"
        return redirect(url_for('deck_pages.get_getStarted', deck_form_error=error_message))