from flask import Flask
from app.extensions.database import db, migrate
from . import deck_pages

def create_app():
  app = Flask(__name__)
  app.config.from_object('app.config')

  register_extensions(app)
  register_bluprints(app)

  return app

def register_bluprints(app: Flask):
  app.register_blueprint(deck_pages.routes.blueprint)

def register_extensions(app: Flask):
  db.init_app(app)
  migrate.init_app(app, db)