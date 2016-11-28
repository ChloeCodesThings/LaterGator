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

    def test_index_logged_out(self):
        """Test homepage page."""

        result = self.client.get("/")
        self.assertIn("A delayed", result.data)

    def test_login(self):
        """Test login page"""

        result = self.client.get("/login")
        self.assertIn("Login", result.data)

    def test_register(self):
        """Test registration page"""

        result = self.client.get("/register")
        self.assertIn("Register", result.data)

    def test_logout_error(self):
        """Test if user tries to log out, but is not logged in"""

        result = self.client.get("/logout", follow_redirects=True)
        self.assertIn("You need to be logged in for that!", result.data)



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

    def test_authorize_new_user_existing(self):
        """Test if user exists"""

        result = self.client.post("/authorize_new_user",
                                  data={"username": "test_user1", "password": "testing123"},
                                  follow_redirects=True)
        self.assertIn("Please choose another username! That one is taken", result.data)

    def test_authorize_new_user_success(self):
        """Test if user added successfully"""

        result = self.client.post("/authorize_new_user",
                                  data={"username": "test_user2", "password": "testing123"},
                                  follow_redirects=True)
        self.assertIn("You now have an account, test_user2!", result.data)

    def test_authorize_no_such_user(self):
        """Test case with no such user"""

        result = self.client.post("/authorize",
                                  data={"username": "nope", "password": "nope"},
                                  follow_redirects=True)

        self.assertIn("No such user", result.data)

    def test_authorize_wrong_password(self):
        """Test case with wrong password"""

        result = self.client.post("/authorize",
                                  data={"username": "test_user1", "password": "nope"},
                                  follow_redirects=True)

        self.assertIn("Incorrect password", result.data)

    def test_authorize_success(self):
        """Test case successful login"""

        result = self.client.post("/authorize",
                                  data={"username": "test_user1", "password": "testing123"},
                                  follow_redirects=True)

        self.assertIn("You are now logged in", result.data)

    def test_logout(self):
        """Test if user tries to log out successfully"""

        result = self.client.get("/logout", follow_redirects=True)

        self.assertIn("You have been logged out- ttfn!", result.data)

    def test_post_twitter(self):
        """Test"""

        result = self.client.get("/post_twitter", follow_redirects=True)

        self.assertIn("Let's post to your Twitter, test_user1!", result.data)




    # def test_index_logged_in(self):
    #     """Test logged in page"""

    #     result = self.client.get("/")
    #     self.assertIn("Welcome test_user1", result.data)

    # def test_post_profile(self):
    #     """Test post to profile page"""
    #     result = self.client.get("/post_profile")
    #     self.assertIn("Let's post to your profile, test_user1!", result.data)

    # def test_confirm_profile(self):
    #     """Test post to profile page"""
    #     pass

    # def test_confirm_profile_too_far_in_future(self):
    #     """Test post to profile page"""
    #     pass

    # def test_confirm_profile_empty_message(self):
    #     """Test post to profile page"""
    #     pass

    # def test_post_twitter(self):
    #     """Test post to Twitter"""
    #     result = self.client.get("/post_twitter")
    #     self.assertIn("Let's post to your Twitter, test_user1!", result.data)

    # def test_confirm_twitter(self):
    #     """Test post to Twitter"""
    #     pass

    # def test_confirm_twitter_too_far_in_future(self):
    #     """Test post to Twitter"""
    #     pass

    # def test_confirm_twitter_empty_message(self):
    #     """Test post to Twitter"""
    #     pass

    # def test_confirm_twitter_over_140(self):
    #     """Test post to Twitter"""
    #     pass

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()


if __name__ == "__main__":

    unittest.main()
