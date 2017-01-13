from flask import Flask
from model import connect_to_db, db, User, FacebookPost, FacebookInfo, TwitterPost, TwitterInfo
import time
from facebook import GraphAPI
from twython import Twython
import os



app = Flask(__name__)


def check_for_posts():
    """Checks to see if there are posts that need to be sent"""

    current_time = int(time.time())
    unpublished_statuses = FacebookPost.query.options(db.joinedload('facebookinfo')).filter_by(is_posted=False).filter(FacebookPost.post_datetime<=current_time).all()

    return unpublished_statuses




def post_statuses(unpublished_statuses):
    """Posts all statuses to facebook that need to be posted"""



    for post in unpublished_statuses:
        msg = post.msg
        access_token = post.facebookinfo.access_token
        api = GraphAPI(access_token)

        api.put_object(parent_object='me', connection_name='feed', message=msg)

        post.is_posted=True
        db.session.add(post)

    db.session.commit()

# To call these:

# post_statuses(check_for_posts())

# or x = check_for_posts()
# post_statuses(x)

def check_for_tweets():
    """Checks to see if there are tweets that need to be sent"""

    current_time = int(time.time())
    unpublished_tweets = TwitterPost.query.options(db.joinedload('twitterinfo')).filter_by(is_posted=False).filter(TwitterPost.post_datetime<=current_time).all()

    return unpublished_tweets

def post_tweets(unpublished_tweets):
    """Posts all tweets to Twitter that need to be posted"""


    for tweet in unpublished_tweets:
        msg = tweet.msg
        access_token = tweet.twitterinfo.oauth_token
        secret_token = tweet.twitterinfo.oauth_token_secret

        APP_KEY=os.environ['TWITTER_CONSUMER_KEY']
        APP_SECRET=os.environ['TWITTER_CONSUMER_SECRET']
        OAUTH_TOKEN=access_token
        OAUTH_TOKEN_SECRET=secret_token

        twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)


        twitter.update_status(status=msg)

        tweet.is_posted=True
        db.session.add(tweet)

    db.session.commit()

# To call these:

# post_tweets(check_for_tweets())
# post_statuses(check_for_posts())


# or x = check_for_tweets()
# post_tweets(x)

def scheduled_run():
    connect_to_db(app, os.environ.get("DATABASE_URL"))
    post_statuses(check_for_posts())
    post_tweets(check_for_tweets())




if __name__ == "__main__":
    scheduled_run()
    connect_to_db(app, os.environ.get("DATABASE_URL"))