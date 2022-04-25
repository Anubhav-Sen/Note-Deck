from flask import Flask
from . import deck_pages

def create_app():
  app = Flask(__name__)
  app.config.from_object('app.config')

  register_bluprints(app)

  return app

def register_bluprints(app: Flask):
  app.register_blueprint(deck_pages.routes.blueprint)