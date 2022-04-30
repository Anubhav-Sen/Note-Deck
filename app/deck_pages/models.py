from app.extensions.database import db, CRUDMethods

class Deck(db.Model, CRUDMethods):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    color = db.Column(db.String(7), nullable=False)

class Card(db.Model, CRUDMethods):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    content = db.Column(db.Text) 
    deck_id = db.Column(db.Integer, db.ForeignKey('deck.id'), nullable=False)

class Image(db.Model, CRUDMethods):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String, nullable=False)
    extention = db.Column(db.String(10), nullable=False)
    card_id = db.Column(db.Integer, db.ForeignKey('card.id'), nullable=False)