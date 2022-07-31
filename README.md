# Note-Deck

Note-Deck is a simple note taking application that revolves
arround the analogy of a deck of cards. Every note taken 
in Note-Deck is card that is a part of a larger deck. 

Writting notes on cards encourages users to make more conise notes,
and having to add a card into a deck helps users better organize 
thier notes.

## Run Locally

Open git bash and navigate to the directory you want the project to be in. Then clone the project

```bash
  git clone https://github.com/Anubhav-Sen/Note-Deck.git
```

Go to the project directory

```bash
  cd Note-Deck
```

Install python virtual enviroment

```bash
  python3 -m pip install virtualenv
```

Create a new virtual enviroment

```bash
  python3 -m venv venv
```
Activate the virtual enviroment

```bash
  . venv/Scripts/activate
```

Install the requirements

```bash
  python3 -m pip install -r requirements.txt
```
To run the flask appliaction type the following code in the terminal

```bash
python run.py