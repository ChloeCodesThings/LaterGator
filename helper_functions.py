from flask import Flask, request
from model import connect_to_db, db, User, Platform, Post
import time
from facebook import GraphAPI


app = Flask(__name__)


def check_for_posts():
    """Checks to see if there are posts that need to be sent"""

    unpublished_statuses = Post.query.filter_by(is_posted=False).all()
    current_time = time.time()
    statues_to_post = []


    for post in unpublished_statuses:
        time_to_be_posted = int(post.post_datetime)

        if time_to_be_posted <= current_time:
            statues_to_post.append(post.post_id)
    print statues_to_post



def post_it(the_posts):
    """Post a message to facebook"""



    for each_id in the_posts:
        post = Post.query.filter_by(post_id=each_id).first()
        msg = post.msg
        user_id = post.user_id
        platform = Platform.query.filter_by(user_id=user_id).first()
        access_token = platform.access_token
        api = GraphAPI(access_token)

        api.put_object(parent_object='me', connection_name='feed', message=msg)

        # post.update().values(is_posted=True)

        # user_id = post.user_id
        # platform = Platform.query.filter_by(user_id=user_id).first()
        # access_token = platform.access_token
        # api = GraphAPI(access_token)

        # api.put_object(parent_object='me', connection_name='feed', message=msg)

        # post.update().values(is_posted=True)





# ** check to see if "pending" post time has already passed
# ** if so, post the status update

if __name__ == "__main__":
    connect_to_db(app)