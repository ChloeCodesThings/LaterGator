from flask import Flask, render_template, request, flash, redirect, session

from facebook import GraphAPI

from model import connect_to_db, db, User, FacebookInfo, FacebookPost, TwitterInfo, TwitterPost, FacebookPagePost

from passlib.hash import pbkdf2_sha256

import urlparse

import oauth2 as oauth

import os

app = Flask(__name__)

SECRET_KEY = os.environ.get("FLASK_SECRET_KEY", "BB8")

TWITTER_CONSUMER_KEY="CMAhx22eA4kSoi4g30QFy8qZo"
TWITTER_CONSUMER_SECRET="x0V8HY8fgSCPoDVw3qZ45FRJ4vtxIKN2z9o1cliCs5kl1qlaQb"
FACEBOOK_APP_SECRET="ed9fb0d4d03465ced13a78a974b93555"
FACEBOOK_APP_ID="235439073543334"



@app.route('/')
def index():
    """Homepage for LaterGator"""

    if 'user_id' in session:
        user_id = session['user_id']

        user = User.query.filter_by(user_id=user_id).first()
        username = user.username
        twitter = TwitterInfo.query.filter_by(user_id=user_id).first()
        logged_in = twitter

        return render_template("logged_in_page.html", username=username, logged_in=logged_in)

    else:
        return render_template("homepage.html")


@app.route('/register')
def register_form():
    """Show register form to user"""

    return render_template("register.html")


@app.route('/authorize_new_user', methods=['POST'])
def register_process():
    """Processes registration."""

    username = request.form.get("username")
    password = request.form.get("password")

    user = User.query.filter_by(username=username).first()

    if user:
        flash("Please choose another username! That one is taken")
        return redirect("/register")

    else:

        hash = pbkdf2_sha256.hash(password)

        new_user = User(username=username, password=hash)

        db.session.add(new_user)
        db.session.commit()

        session["user_id"] = new_user.user_id

        flash("You now have an account, %s!" % username)
        return redirect("/")


@app.route('/login')
def show_login():
    return render_template("login.html")


@app.route('/authorize', methods=['POST'])
def login_process():
    """Process login."""

    username = request.form.get("username")
    password = request.form.get("password")

    user = User.query.filter_by(username=username).first()

    if not user:
        flash("No such user")
        return redirect("/login")

    else:

        hashed_pw = user.password
        verified_pw = pbkdf2_sha256.verify(password, hashed_pw)

        if verified_pw is False:
            flash("Incorrect password")
            return redirect("/login")

        else:
            session["user_id"] = user.user_id
            flash("You are now logged in")
            return redirect("/")


@app.route('/logout')
def logout_user():
    """Logs out user"""

    if 'user_id' not in session:
        flash("You need to be logged in for that!")
    else:
        del session["user_id"]
        flash("You have been logged out- ttfn!")

    return redirect("/")


@app.route('/add_fb_token', methods=['POST'])
def add_facebook_token():
    """Add token to db"""

    access_token = request.form.get("access_token")
    facebook_user_id = request.form.get("facebook_user_id")

    graph = GraphAPI(access_token)
    app_id = os.environ['FACEBOOK_APP_ID']
    app_secret = os.environ['FACEBOOK_APP_SECRET']
    extended_token = graph.extend_access_token(app_id, app_secret)
    final_token = extended_token['access_token']
    facebook_info = FacebookInfo.query.filter_by(facebook_user_id=facebook_user_id, user_id=session['user_id']).first()

    if not facebook_info:
        facebook_info = FacebookInfo(user_id=session["user_id"], access_token=final_token, facebook_user_id=facebook_user_id)

    else:
        facebook_info.access_token = access_token

    db.session.add(facebook_info)
    db.session.commit()

    return "success"


@app.route('/twitter_oauth')
def twitter_oauth():
    """3-legged OAuth for Twitter"""

    consumer_key = os.environ['TWITTER_CONSUMER_KEY']
    consumer_secret = os.environ['TWITTER_CONSUMER_SECRET']


    request_token_url = 'https://api.twitter.com/oauth/request_token'
    access_token_url = 'https://api.twitter.com/oauth/access_token'
    authorize_url = 'https://api.twitter.com/oauth/authorize'

    consumer = oauth.Consumer(consumer_key, consumer_secret)
    client = oauth.Client(consumer)

    resp, content = client.request(request_token_url, "GET")
    if resp['status'] != '200':
        raise Exception("Invalid response %s." % resp['status'])

    request_token = dict(urlparse.parse_qsl(content))
    session['secret'] = request_token['oauth_token_secret']
    session['token'] = request_token['oauth_token']

    return redirect("%s?oauth_token=%s" % (authorize_url, request_token['oauth_token']))


@app.route('/add_twitter_token')
def add_twitter_token():
    """Add twitter tokens to db"""
    oauth_token_secret = session['secret']

    token = oauth.Token(session['token'], oauth_token_secret)

    oauth_verifier = request.args.get('oauth_verifier')

    token.set_verifier(oauth_verifier)
    consumer_key = os.environ['TWITTER_CONSUMER_KEY'],
    consumer_secret = os.environ['TWITTER_CONSUMER_SECRET']

    consumer = oauth.Consumer(consumer_key, consumer_secret)
    client = oauth.Client(consumer, token)
    access_token_url = 'https://api.twitter.com/oauth/access_token'

    resp, content = client.request(access_token_url, "POST")
    access_token = dict(urlparse.parse_qsl(content))

    oauth_token = access_token['oauth_token']
    oauth_token_secret = access_token['oauth_token_secret']
    twitter_info = TwitterInfo.query.filter_by(oauth_token=oauth_token, user_id=session['user_id']).first()

    if not twitter_info:
        twitter_info = TwitterInfo(user_id=session["user_id"], oauth_token=oauth_token, oauth_token_secret=oauth_token_secret)

    else:
        twitter_info.oauth_token = oauth_token
        twitter_info.oauth_token_secret = oauth_token_secret

    db.session.add(twitter_info)
    db.session.commit()

    return redirect("/")


@app.route('/post_twitter')
def show_post_form():
    """Show posting for for Twitter"""
    if 'user_id' not in session:
        flash("You need to be logged in for that!")
        return redirect('/')

    user_id = session["user_id"]
    twitterprofile = TwitterInfo.query.filter_by(user_id=user_id).first()

    if not twitterprofile:
        flash("You need to log into Twitter first!")
        return redirect('/')

    user = User.query.filter_by(user_id=user_id).first()
    username = user.username

    return render_template("post_twitter.html", username=username)


@app.route('/post_pages')
def show_post_form_pages():
    """Show posting for for Facebook Pages"""
    if 'user_id' not in session:
        flash("You need to be logged in for that!")
        return redirect('/')

    user_id = session["user_id"]
    user = User.query.filter_by(user_id=user_id).first()

    username = user.username

    facebook_info = FacebookInfo.query.filter_by(user_id=user_id).first()

    if not facebook_info:
        flash("You need to log into Facebook first!")
        return redirect('/')

    access_token = facebook_info.access_token

    api = GraphAPI(access_token)

    page_response = api.get_connections("me", "accounts")

    return render_template("post_pages.html", username=username, pages=page_response["data"])


@app.route('/post_profile')
def show_post_form_profile():
    """Show posting for for Facebook profile"""
    if 'user_id' not in session:
        flash("You need to be logged in for that!")
        return redirect('/')

    user_id = session["user_id"]
    facebook_info = FacebookInfo.query.filter_by(user_id=user_id).first()

    if not facebook_info:
        flash("You need to log into Facebook first!")
        return redirect('/')

    user = User.query.filter_by(user_id=user_id).first()
    username = user.username
    return render_template("post_profile.html", username=username)


@app.route('/confirm_pages', methods=['POST'])
def confirm_post():
    """Sends scheduled post info to Facebook (pages only) and redirects to confirmation page"""

    if 'user_id' not in session:
        flash("You need to be logged in for that!")
        return redirect('/login')

    page_id = request.form.get("page_id")
    user_id = session["user_id"]
    msg = request.form.get("userpost")
    scheduled_publish_time = int(request.form.get('publish_timestamp'))
    facebook_info = FacebookInfo.query.filter_by(user_id=user_id).one()
    facebookinfo_id = facebook_info.facebookinfo_id
    time_to_show = request.form.get('time_to_show')

    user_id = session["user_id"]
    facebook_info = FacebookInfo.query.filter_by(user_id=user_id).first()

    access_token = facebook_info.access_token
    api = GraphAPI(access_token)

    access_token_response = api.get_object(id=page_id, fields='access_token')

    page_token = access_token_response['access_token']

    page_api = GraphAPI(page_token)

    page_api.put_object(parent_object='me', connection_name='feed', scheduled_publish_time=scheduled_publish_time, published=False,
                 message=msg)

    new_post = FacebookPagePost(msg=msg, post_datetime=scheduled_publish_time, user_id=session["user_id"], facebookinfo_id=facebookinfo_id)

    db.session.add(new_post)
    db.session.commit()

    #Add unpublished part here??

    # page_response = api.get_connections("me", "accounts")

    # pages = page_response["data"]

    # published_posts = []
    # unpublished_posts = []

    # for page in pages:
    #     current_page_id = str(page['id'])

    #     post_rsp = api.get_connections(id=current_page_id, connection_name='promotable_posts', fields='is_published,message,id')

    #     for post in post_rsp['data']:
    #         print post
    #         if post['is_published']:
    #             published_posts.append(post)
    #         else:
    #             unpublished_posts.append(post)

    unpublished_page_posts = FacebookPagePost.query.filter_by(is_posted=False, user_id=user_id).all()

    return render_template("/confirm_page.html", time_to_show=time_to_show, unpublished_page_posts=unpublished_page_posts)


@app.route('/confirm_profile', methods=['POST'])
def add_post_to_db():
    """Add post info to db"""

    if 'user_id' not in session:
        flash("You need to be logged in for that!")
        return redirect('/login')

    user_id = session["user_id"]
    msg = request.form.get("userpost")
    scheduled_publish_time = int(request.form.get('publish_timestamp'))
    facebook_info = FacebookInfo.query.filter_by(user_id=user_id).one()
    facebookinfo_id = facebook_info.facebookinfo_id
    time_to_show = request.form.get('time_to_show')

    new_post = FacebookPost(msg=msg, post_datetime=scheduled_publish_time, user_id=session["user_id"], facebookinfo_id=facebookinfo_id)

    db.session.add(new_post)
    db.session.commit()

    unpublished_profile_posts = FacebookPost.query.filter_by(is_posted=False, user_id=user_id).all()

    return render_template("confirm_profile.html", time_to_show=time_to_show, unpublished_profile_posts=unpublished_profile_posts)


@app.route('/confirm_twitter', methods=['POST'])
def add_twitter_post_to_db():
    """Add post info to db"""

    if 'user_id' not in session:
        flash("You need to be logged in for that!")
        return redirect('/login')

    user_id = session["user_id"]
    msg = request.form.get("userpost")
    scheduled_publish_time = int(request.form.get('publish_timestamp'))
    twitterinfo = TwitterInfo.query.filter_by(user_id=user_id).one()
    twitterinfo_id = twitterinfo.twitterinfo_id
    time_to_show = request.form.get('time_to_show')

    new_twitter_post = TwitterPost(msg=msg, post_datetime=scheduled_publish_time, user_id=session["user_id"], twitterinfo_id=twitterinfo_id)

    db.session.add(new_twitter_post)
    db.session.commit()

    unpublished_tweets = TwitterPost.query.filter_by(is_posted=False, user_id=user_id).all()

    return render_template("confirm_twitter.html", time_to_show=time_to_show, unpublished_tweets=unpublished_tweets)


@app.route("/error")
def error():
    raise Exception("Error!")

if __name__ == "__main__":
    DEBUG = "NO_DEBUG" not in os.environ
    connect_to_db(app, os.environ.get("DATABASE_URL"))
    PORT = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=PORT, debug=DEBUG)
