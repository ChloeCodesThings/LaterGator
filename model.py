"""Models and database functions for latergator db."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """Users of LaterGator"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)


    def __repr__(self):
        """Show user info"""
        return "<User id=%d Username=%s Password=%s>"\
                %(self.user_id, self.username, self.password)


class FacebookInfo(db.Model):
    """Facebook OAuth info"""

    __tablename__ = "facebookinfo"

    facebookinfo_id = db.Column(db.Integer,
                        primary_key=True,
                        autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    access_token = db.Column(db.String(200), nullable=False)
    facebook_user_id = db.Column(db.String(200), nullable=False)

    user = db.relationship("User", backref="facebookinfo")


class TwitterInfo(db.Model):
    """Twitter OAuth info"""

    __tablename__ = "twitterinfo"

    twitterinfo_id = db.Column(db.Integer,
                        primary_key=True,
                        autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    oauth_token = db.Column(db.String(200), nullable=False)
    oauth_token_secret = db.Column(db.String(200), nullable=False)

    user = db.relationship("User", backref="twitterinfo")


class FacebookPost(db.Model):
    """Facebook posts that the user has submitted"""

    __tablename__ = "facebookposts"

    post_id = db.Column(db.Integer,
                        primary_key=True,
                        autoincrement=True)
    msg = db.Column(db.String(63206), nullable=False)
    post_datetime = db.Column(db.Integer, nullable=False)
    is_posted = db.Column(db.Boolean, default=False, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    facebookinfo_id = db.Column(db.Integer, db.ForeignKey('facebookinfo.facebookinfo_id'), nullable=False)

    user = db.relationship("User", backref="facebookposts")
    facebookinfo = db.relationship("FacebookInfo", backref="facebookposts")

    def __repr__(self):
        """Show post info"""
        return "<Status=%s User ID=%d>"\
                %(self.msg, self.user_id)

class FacebookPagePost(db.Model):
    """Facebook PAGE posts that the user has submitted through LaterGator"""

    __tablename__ = "facebookpageposts"

    post_id = db.Column(db.Integer,
                        primary_key=True,
                        autoincrement=True)
    msg = db.Column(db.String(63206), nullable=False)
    is_posted = db.Column(db.Boolean, default=False, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    facebookinfo_id = db.Column(db.Integer, db.ForeignKey('facebookinfo.facebookinfo_id'), nullable=False)

    user = db.relationship("User", backref="facebookpageposts")
    facebookinfo = db.relationship("FacebookInfo", backref="facebookpageposts")

    def __repr__(self):
        """Show post info"""
        return "<Status=%s Is Posted?=%s>"\
                %(self.msg, self.is_posted)




class TwitterPost(db.Model):
    """Twitter posts that the user has submitted"""

    __tablename__ = "twitterposts"

    post_id = db.Column(db.Integer,
                        primary_key=True,
                        autoincrement=True)
    msg = db.Column(db.String(140), nullable=False)
    post_datetime = db.Column(db.Integer, nullable=False) #remember to change to datetime!
    is_posted = db.Column(db.Boolean, default=False, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    twitterinfo_id = db.Column(db.Integer, db.ForeignKey('twitterinfo.twitterinfo_id'), nullable=False)


    user = db.relationship("User", backref="twitterposts")
    twitterinfo = db.relationship("TwitterInfo", backref="twitterposts")

    def __repr__(self):
        """Show tweet info"""
        return "<Tweet=%s User ID=%d>"\
            %(self.msg, self.user_id)

##############################################################################
# Helper functions

def init_app():
    # So that we can use Flask-SQLAlchemy, we'll make a Flask app
    from flask import Flask
    app = Flask(__name__)

    connect_to_db(app)
    print "Connected to DB."


def connect_to_db(app, db_uri="postgresql:///latergator"):
    """Connect to database."""

    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)


##############################################################################
# Tests

def example_data():
    """Create some sample data."""

    # In case this is run more than once, empty out existing data

    FacebookPost.query.delete()
    TwitterPost.query.delete()
    FacebookInfo.query.delete()
    TwitterInfo.query.delete()
    User.query.delete()


    # Test user
    test_user = User(username='test_user1', password='$pbkdf2-sha256$29000$FALgPKfUWiuFkNK6NwZA6A$p.mRwWhJ8zs3cFNt7ygsb/HDF1EY5rYW3DdySpIm/NQ')

    db.session.add(test_user)
    db.session.commit()


    # Test login info
    test_fb_info = FacebookInfo(user_id=test_user.user_id, access_token='fake1234', facebook_user_id='1234567' )

    db.session.add(test_fb_info)
    db.session.commit()

    #Test login info
    test_twitter_info = TwitterInfo(user_id=test_user.user_id, oauth_token='fake1234', oauth_token_secret='1234567')

    db.session.add(test_twitter_info)
    db.session.commit()

    #Test Facebook post
    test_fb_post = FacebookPost(user_id=test_user.user_id, msg='Test for Facebook!', post_datetime='1480203960', facebookinfo_id=test_fb_info.facebookinfo_id)

    db.session.add(test_fb_post)
    db.session.commit()

    # Test Twitter post
    test_twitter_post = TwitterPost(user_id=test_user.user_id, msg='Test for Twitter!', post_datetime='1480203960', twitterinfo_id= test_twitter_info.twitterinfo_id)

    db.session.add(test_twitter_post)

    db.session.commit()



if __name__ == "__main__":

    from flask import Flask

    app = Flask(__name__)

    connect_to_db(app)
    print "Connected to DB."
    db.create_all()
    print "DB created"