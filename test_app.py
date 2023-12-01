from unittest import TestCase

from app import app, games

# Make Flask errors be real errors, not HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']


class BoggleAppTestCase(TestCase):
    """Test flask app of Boggle."""

    def setUp(self):
        """Stuff to do before every test."""

        app.config['TESTING'] = True

    def test_homepage(self):
        """Make sure information is in the session and HTML is displayed"""

        with app.test_client() as client:
            response = client.get('/')
            html = response.get_data(as_text=True)

            # test that homepage loads and contains board and word form
            self.assertEqual(response.status_code, 200)
            self.assertIn("Comment for testing index.html opened", html)
            self.assertIn('<table class="board', html)
            self.assertIn('<form id="newWordForm">', html)

    def test_api_new_game(self):
        """Test starting a new game."""

        with app.test_client() as client:
            response = client.post("/api/new-game")
            game_id = response.json["game_id"]
            board = response.json["board"]

            self.assertEqual(response.status_code, 200)

            # should have string game id, and a list-of-lists for the board
            self.assertIsInstance(game_id, str)
            self.assertIsInstance(board, list)
            self.assertIsInstance(board[0], list)

            # check that game was added to games global dict
            self.assertIn(game_id, games)

    def test_api_score_word(self):
        """
        Tests route from starting new game to checking word validity works.
        Tests different outcomes of score_word (word doesn't exist, word isn't
        on board, or word is valid & on Boggle board).
        """

        with app.test_client() as client:
            new_game_response = client.post("/api/new-game")
            game_id = new_game_response.json["game_id"]

            # Grab specific game instance &
            # Alter board to ensure 'CATCH' is a valid word in testing
            game = games[game_id]
            game.board[0] = ["C", "A", "T", "C", "H"]

            print('game=', game, 'game.board=', game.board, "game_id=", game_id)

            not_word_response = client.post(
                "/api/score-word",
                data={"word": "ANKJSNDKJBFSFSF", "game_id": game_id})

            not_on_board_response = client.post(
                "/api/score-word",
                data={"word": "ZYZZYVA", "game_id": game_id})

            # This response should result in 'ok'
            ok_response = client.post(
                "/api/score-word",
                data={"word": "CATCH", "game_id": game_id})

            # Check route status
            self.assertEqual(ok_response.status_code, 200)
            self.assertEqual(not_word_response.json, {"result": "not-word"})
            self.assertEqual(
                not_on_board_response.json, {"result": "not-on-board"})
            self.assertEqual(ok_response.json, {"result": "not-word"})






        # Relies on creating a new game, so we need to call/generate
        # new game first using /api/new-game

        # figure out how to alter letters on board before scoring
        # also modifying arrays to make sure there is a word (last of tests)

        # check that route to this section works

        # 3 tests to include (at least):
        # word doesn't exist
        # word isn't on board
        # word is a-ok




