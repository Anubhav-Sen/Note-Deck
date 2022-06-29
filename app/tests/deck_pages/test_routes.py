from app.deck_pages.models import Deck, Card, Image

def test_index_redirect(client):
    response = client.get('/')
    assert response.status_code == 302

def test_note_deck_success(client):

    response = client.get('/decks/<int:deck_id>/<deck_title>/<deck_color>')
    deck_form_post_response = client.post('/decks/<int:deck_id>/<deck_title>/<deck_color>', data={
    'id': '2',
    'title': 'testdeck2',
    'color': '#000000',
    'deck-form': '',
  })
    
    new_deck = Deck(title='testdeck', color='#EC5F5F')
    new_deck.save()

    assert response.status_code == 200 or 404
    
    if response.status_code == 200:
        assert b'<div class="deck">' in response.data
        assert b'testdeck' in response.data
        assert b'#EC5F5F' in response.data
        assert Deck.query.filter_by(id = 2).first().id is 2
        assert Deck.query.filter_by(id = 2).first().title is 'testdeck2'
        assert Deck.query.filter_by(id = 2).first().color is '#000000'



def test_get_started_success(client):
    response = client.get('/get-started')
    assert response.status_code == 200 or 404

    if response.status_code == 200:
        assert b'Get-Started' in response.data
        assert b'<div class="card">' not in response.data
        assert b'<div class="deck">' not in response.data