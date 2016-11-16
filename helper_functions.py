from flask import Flask, request
from model import connect_to_db, db, User, Platform, Post
import time
from facebook import GraphAPI


app = Flask(__name__)


def check_for_posts():
    """Checks to see if there are posts that need to be sent"""

    current_time = int(time.time())
    unpublished_statuses = Post.query.options(db.joinedload('platform')).filter_by(is_posted=False).filter(Post.post_datetime<=current_time).all()

    return unpublished_statuses




def post_it(the_posts):
    """Post a message to facebook"""



    for post in the_posts:
        msg = post.msg
        user_id = post.user_id
        access_token = post.platform.access_token
        api = GraphAPI(access_token)

        api.put_object(parent_object='me', connection_name='feed', message=msg)

        post.is_posted=True
        db.session.add(post)

    db.session.commit()

#post_it(check_for_posts())

# or x = check_for_posts()
# post_it(x)


if __name__ == "__main__":
    connect_to_db(app)