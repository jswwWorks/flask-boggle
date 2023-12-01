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



