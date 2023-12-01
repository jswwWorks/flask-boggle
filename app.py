from flask import Flask, request, render_template, jsonify
from flask_debugtoolbar import DebugToolbarExtension


from uuid import uuid4

from boggle import BoggleGame

app = Flask(__name__)
app.config["SECRET_KEY"] = "this-is-secret"

debug = DebugToolbarExtension(app)

# The boggle games created, keyed by game id
games = {}


@app.get("/")
def homepage():
    """Show board."""

    return render_template("index.html")


@app.post("/api/new-game")
def new_game():
    """Start a new game and return JSON: {game_id, board}."""

    # get a unique string id for the board we're creating
    game_id = str(uuid4())
    game = BoggleGame()

    # add game to global games dictionary
    games[game_id] = game

    return jsonify({"game_id": game_id, "board": game.board})


@app.post("/api/score-word")
def score_word():
    """Check if a word is legal. Post request should be json with game_id / word
    Return a json with result key and value of not-word, not-on-board, or ok"""

    game_id = request.json['game_id']
    word = request.json['word']

    game = games[game_id]

    word_list = game.word_list
    if not word_list.check_word(word):
        result = 'not-word'

    if not game.check_word_on_board(word):
        result = 'not-on-board'

    else:
        result = 'ok'

    return jsonify({"result": result})





