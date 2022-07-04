from app.deck_pages.models import Deck, Card, Image
from app.users.models import User

def test_index_redirect(client):
    response = client.get('/')
    assert response.status_code == 302

def test_note_deck_success(client):

    response = client.get('/decks/<int:deck_id>/<deck_title>/<deck_color>')
    
    client.post('/decks/<int:deck_id>/<deck_title>/<deck_color>', data={
    'id': '2',
    'title': 'testdeck2',
    'color': '#000000',
    'deck-form': ''
    })

    client.post('/decks/<int:deck_id>/<deck_title>/<deck_color>', data={
    'id': '1',
    'title': 'testcard',
    'content': 'some text',
    'image':'',
    'deck_id':'1',
    'card-form': ''
    })

    client.post('/decks/<int:deck_id>/<deck_title>/<deck_color>', data={
    'id': '3',
    'title': 'testdeck3',
    'color': '#000000',
    'deck-form': ''
    })

    client.post('/decks/<int:deck_id>/<deck_title>/<deck_color>', data={
    'id': '3',
    'title': 'testdeck3updated',
    'color': '#000000',
    'deck-form': ''
    })

    client.post('/decks/<int:deck_id>/<deck_title>/<deck_color>', data={
    'id': '2',
    'title': 'testcard2',
    'content': 'some text',
    'image':'',
    'deck_id':'1',
    'card-form': ''
    })

    client.post('/decks/<int:deck_id>/<deck_title>/<deck_color>', data={
    'id': '2',
    'title': 'testcard2updated',
    'content': 'some text',
    'image':'',
    'deck_id':'1',
    'card-form': ''
    })
    
    new_deck = Deck(title='testdeck', color='#EC5F5F', user_id = 0)
    new_deck.save()

    assert response.status_code == 200 or 404
    
    if response.status_code == 200:
        assert b'<div class="deck">' in response.data
        assert b'testdeck' in response.data
        assert b'#EC5F5F' in response.data
        assert Deck.query.filter_by(id = 2).first().id is 2
        assert Deck.query.filter_by(id = 2).first().title is 'testdeck2'
        assert Deck.query.filter_by(id = 2).first().color is '#000000'
        assert Deck.query.filter_by(id = 3).first().title is 'testdeck3updated'
        assert Card.query.filter_by(id = 1).first().id is 1
        assert Card.query.filter_by(id = 1).first().title is 'testcard'
        assert Card.query.filter_by(id = 1).first().content is 'some text'  
        assert Card.query.filter_by(id = 1).first().image is None
        assert Card.query.filter_by(id = 1).first().deck_id is 1
        assert Card.query.filter_by(id = 2).first().title is 'testcard2updated'

def test_delete_deck_success(client):

    new_deck = Deck(title='testdeck', color='#EC5F5F', user_id = 0)
    new_deck.save()

    response = client.get('/delete-deck/1/1')

    assert response.status_code == 302 or 404 or 401

    if response.status_code == 302:
        assert Deck.query.filter_by(id = 1).first() is None


def test_delete_card_success(client):

    new_deck = Deck(title='testdeck', color='#EC5F5F', user_id = 0)
    new_deck.save()

    new_card = Card(title='testcard', content='some text', image = None, deck_id = 1)
    new_card.save()

    response = client.get('/delete-card/1/1')

    assert response.status_code == 302 or 404 or 401

    if response.status_code == 302:
        assert Card.query.filter_by(id = 1).first() is None

def test_update_deck_success(client):

    new_deck = Deck(title='testdeck', color='#EC5F5F', user_id = 0)
    new_deck.save()

    response = client.get('/update-deck/1/1')

    assert response.status_code == 302 or 404 or 401 


def test_update_card_success(client):

    new_deck = Deck(title='testdeck', color='#EC5F5F', user_id = 0)
    new_deck.save()

    new_card = Card(title='testcard', content='some text', image = None, deck_id = 1)
    new_card.save()

    response = client.get('/update-card/1/1')

    assert response.status_code == 302 or 404 or 401

def test_search_success(client):

    new_deck = Deck(title='testdeck', color='#EC5F5F', user_id = 0)
    new_deck.save()

    new_card = Card(title='testcard', content='this is a test', image = None, deck_id = 1)
    new_card.save()

    response = client.get('/search/1/test')

    assert response.status_code == 200 or 401

    if response.status_code == 200:
        assert b'<div class="search-header">' in response.data
        assert b'test' in response.data

def test_get_started_success(client):
    response = client.get('/get-started')
    assert response.status_code == 200 or 404

    if response.status_code == 200:
        assert b'Get-Started' in response.data
        assert b'<div class="card">' not in response.data
        assert b'<div class="deck">' not in response.data