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
    password = db.Column(db.String(15), nullable=False)


    # not necessary, but can add in I guess
    def __repr__(self):
        """Show user info"""
        return "<User id=%d Username=%s Password=%s>"\
                %(self.user_id, self.username, self.password)


class Platform(db.Model):
    """Social media platforms"""

    __tablename__ = "platforms"

    platform_id = db.Column(db.Integer,
                        primary_key=True,
                        autoincrement=True)
    # name = db.Column(db.String(20), nullable=False) will add this when I add other platforms. Not needed for MVP
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    access_token = db.Column(db.String(200), nullable=False)
    facebook_user_id = db.Column(db.String(200), nullable=False)
    # expires_in = db.Column(db.String(10), nullable=False)

    user = db.relationship("User", backref="platforms")

    def __repr__(self):
        """Show platform info"""
        return "<Platform name=%s User ID=%d>"\
                %(self.platform_id, self.user_id)    


class Post(db.Model):
    """Posts that the user has made"""

    __tablename__ = "posts"

    post_id = db.Column(db.Integer,
                        primary_key=True,
                        autoincrement=True)
    text = db.Column(db.String(800), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    platform_id = db.Column(db.Integer, db.ForeignKey('platforms.platform_id'), nullable=False)
    postdatetime = db.Column(db.String(30), nullable=False) #remember to change to datetime!


    user = db.relationship("User", backref="posts")
    platform = db.relationship("Platform", backref="posts")

    def __repr__(self):
        """Show post info"""
        return "<Post=%s User ID=%d>"\
                %(self.text, self.user_id)  


##############################################################################
# Helper functions

def init_app():
    # So that we can use Flask-SQLAlchemy, we'll make a Flask app
    from flask import Flask
    app = Flask(__name__)

    connect_to_db(app)
    print "Connected to DB."


def connect_to_db(app):
    """Connect to database."""

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///latergator'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)


if __name__ == "__main__":

    from flask import Flask

    app = Flask(__name__)

    connect_to_db(app)
    print "Connected to DB."