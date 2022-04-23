from flask import Flask, url_for, render_template

app = Flask(__name__)
app.config.from_object('config')

deck_title = "Test-deck"
username = "Dwight"

@app.route('/')
def index():
  return render_template('index.html', deck_title = deck_title, username = username)

if __name__ == '__main__':
    app.run()