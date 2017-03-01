import unittest
from model import connect_to_db, db, User, FacebookInfo, FacebookPost, TwitterInfo, TwitterPost, example_data
from server import app
from passlib.hash import pbkdf2_sha256
from flask import session


class FlaskTestsLoggedOut(unittest.TestCase):
    """Flask tests."""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = "ABCDEFG"
        self.app = app.test_client()


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

    def test_post_profile_error(self):
        """Test if user tries to post to Facebook, but not logged in"""

        result = self.client.get("/post_profile", follow_redirects=True)
        self.assertIn("You need to be logged in for that!", result.data)

    def test_post_twitter_error(self):
        """Test if user tries to post to twitter, but not logged in"""

        result = self.client.get("/post_twitter", follow_redirects=True)
        self.assertIn("You need to be logged in for that!", result.data)

    def test_post_profile_confirm_error(self):
        """Test if user tries to access confirmation page, but not logged in"""

        result = self.client.post("/confirm_profile", follow_redirects=True)
        self.assertIn("You need to be logged in for that!", result.data)

    def test_post_twitter_confirm_error(self):
        """Test if user tries to access confirmation page, but not logged in"""

        result = self.client.post("/confirm_twitter", follow_redirects=True)
        self.assertIn("You need to be logged in for that!", result.data)





class FlaskTestsLoggedIn(unittest.TestCase):
    """Flask tests with user logged in to session."""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()
        app.config['TESTING'] = True

        app.config['SECRET_KEY'] = "ABCDEFG"

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
        """Testing post_twitter page success"""

        result = self.client.get("/post_twitter", follow_redirects=True)

        self.assertIn("Let's post to your Twitter, test_user1!", result.data)

    def test_post_twitter_error(self):
        """Testing post_twitter page error"""

        TwitterPost.query.delete()
        TwitterInfo.query.delete()
        db.session.commit()

        result = self.client.get("/post_twitter", follow_redirects=True)

        self.assertIn("You need to log into Twitter first!", result.data)

    def test_post_profile(self):
        """Testing post_profile page success"""

        result = self.client.get("/post_profile", follow_redirects=True)

        self.assertIn("Let's post to your profile, test_user1!", result.data)

    def test_post_profile_error(self):
        """Testing post_profile page error"""

        FacebookPost.query.delete()
        FacebookInfo.query.delete()
        db.session.commit()

        result = self.client.get("/post_profile", follow_redirects=True)

        self.assertIn("You need to log into Facebook first!", result.data)

    def test_confirm_profile(self):
        """Testing confirm_profile"""
        result = self.client.post("/confirm_profile",
                                  data={"userpost": "Test for Facebook!", "publish_timestamp": "1480203960", "user_id": "test_user.user_id", "facebookinfo_id": "test_fb_info.facebookinfo_id"},
                                  follow_redirects=True)

        self.assertIn("Test for Facebook!", result.data)

    def test_confirm_twitter(self):
        """Testing confirm_twitter"""
        result = self.client.post("/confirm_twitter",
                                  data={"userpost": "Test for Twitter!", "publish_timestamp": "1480203960", "user_id": "test_user.user_id", "twitterinfo_id": "test_twitter_info.twitterinfo_id"},
                                  follow_redirects=True)

        self.assertIn("Test for Twitter!", result.data)

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()


if __name__ == "__main__":

    unittest.main()
