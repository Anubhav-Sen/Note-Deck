from app.extensions.database import db, CRUDMethods
from flask_login import UserMixin
from datetime import datetime

class User(db.Model, CRUDMethods, UserMixin):
  id = db.Column(db.Integer, primary_key = True)
  username = db.Column(db.String(128))
  email = db.Column(db.String(128), index = True, unique = True)
  password = db.Column(db.String(1024))
  decks = db.relationship('Deck', backref = 'user')
  date_created = db.Column(db.DateTime(timezone=True), default=datetime.utcnow, nullable=False)