from app.extensions.database import db
from app.deck_pages.models import Deck, Card, Image

def test_deck_update(client):
  deck = Deck(title = 'test', color = '#adadad', user_id = 0)
  db.session.add(deck)
  db.session.commit()

  deck.title = 'updatetest'
  deck.save()

  updated_deck = Deck.query.filter_by(id = deck.id).first()
  assert updated_deck.title == 'updatetest'

def test_card_update(client):
  card = Card(title = 'test', content = '', deck_id = 1)
  db.session.add(card)
  db.session.commit()

  card.title = 'updatetest'
  card.save()

  updated_card = Card.query.filter_by(id = card.id).first()
  assert updated_card.title == 'updatetest'

def test_image_update(client):
  image = Image(data = 'ArbitraryString', extention = 'png', card_id = 1)
  db.session.add(image)
  db.session.commit()

  image.data = 'ArbitraryStringUpdated'
  image.save()

  updated_image = Image.query.filter_by(id = image.id).first()
  assert updated_image.data == 'ArbitraryStringUpdated'


def test_deck_delete(client):
  deck = Deck(title = 'test', color = '#adadad', user_id = 0)
  db.session.add(deck)
  db.session.commit()

  deck.delete()

  deleted_deck = Deck.query.filter_by(id = deck.id).first()
  assert deleted_deck is None

def test_card_delete(client):
  card = Card(title = 'test', content = '', deck_id = 1)
  db.session.add(card)
  db.session.commit()

  card.delete()

  deleted_card = Card.query.filter_by(id = card.id).first()
  assert deleted_card is None

def test_image_delete(client):
  image = Image(data = 'ArbitraryString', extention = 'png', card_id = 1)
  db.session.add(image)
  db.session.commit()

  image.delete()

  deleted_image = Image.query.filter_by(id = image.id).first()
  assert deleted_image is None