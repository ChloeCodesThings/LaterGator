import unittest
from model import connect_to_db, db, User, FacebookInfo, FacebookPost, TwitterInfo, TwitterPost, example_data
from server import app
from flask import session

class FlaskTestsLoggedOut(unittest.TestCase):
    """Flask tests."""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True

    def test_index(self):
        """Test homepage page."""

        result = self.client.get("/")
        self.assertIn("A delayed status posting app.", result.data)

    def test_login(self):
        """Test login page"""

        result = self.client.get("/login")
        self.assertIn("Login", result.data)

    def test_register(self):
        """Test registration page"""

        result = self.client.get("/register")
        self.assertIn("Register", result.data)


class FlaskTestsLoggedIn(unittest.TestCase):
    """Flask tests with user logged in to session."""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()
        app.config['TESTING'] = True

        # Connect to test database
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data
        db.create_all()
        example_data()

        with self.client.session_transaction() as session:

            user = User.query.first()
            user_id = user.user_id
            session['user_id'] = user_id


    def test_logged_in(self):
        """Test logged in page"""

        result = self.client.get("/")
        self.assertIn("Welcome test_user1", result.data)

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()



if __name__ == "__main__":
    import unittest

    unittest.main()
