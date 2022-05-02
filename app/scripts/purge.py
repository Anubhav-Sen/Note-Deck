from app.app import create_app
from app.deck_pages.models import Deck, Card, Image
from app.extensions.database import db

app = create_app()
app.app_context().push()

Deck.query.delete()

db.session.flush()

Card.query.delete()

db.session.flush()

Image.query.delete()

db.session.flush()

db.session.commit()