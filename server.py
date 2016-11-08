from flask import Flask, render_template, request, flash, redirect, session

from facebook import GraphAPI

from model import connect_to_db, db, User, Platform, Post

import time


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "YOLO"

@app.route('/')
def index():
    """Homepage for LaterGator"""
    return render_template("homepage.html")

@app.route('/register')
def register_form():
    """Show register form to user"""

    return render_template("register.html")


@app.route('/register', methods=['POST'])
def register_process():
    """Processes registration."""

    # Get form variables
    username = request.form.get("username")
    password = request.form.get("password")

    new_user = User(username=username, password=password)

    db.session.add(new_user)
    db.session.commit()

    session["user_id"] = new_user.user_id

    flash("Welcome %s! You are now have an account!" % username)
    return render_template("auth_post_view.html", username=username)


@app.route('/login')
def show_login():
    return render_template("login.html")

@app.route('/login', methods=['POST'])
def login_process():
    """Process login."""

    # Get form variables
    username = request.form.get("username")
    password = request.form.get("password")

    user = User.query.filter_by(username=username).first()

    if not user:
        flash("No such user")
        return redirect("/login")

    if user.password != password:
        flash("Incorrect password")
        return redirect("/login")

    session["user_id"] = user.user_id

    flash("You are now logged in")
    return redirect("/authorize")

@app.route('/logout')
def logout_user():
    if 'user_id' not in session:
        flash("You are not logged in!")
        return redirect('/login')

    del session["user_id"]
    flash("Logged Out.")
    return redirect("/")

@app.route('/authorize')
def login_user():
    """Process login."""

    if 'user_id' not in session:
        flash("You need to be logged in for that!")
        return redirect('/login')

    return render_template("auth_post_view.html")

@app.route('/add_token', methods=['POST'])
def add_token():
    """Add token to db"""

    access_token = request.form.get("access_token")
    facebook_user_id = request.form.get("facebook_user_id")

    platform_info = Platform.query.filter_by(facebook_user_id=facebook_user_id, user_id=session['user_id']).first()

    if not platform_info:
        platform_info = Platform(user_id=session["user_id"], access_token=access_token, facebook_user_id=facebook_user_id)


    else:
        platform_info.access_token = access_token

    db.session.add(platform_info)
    db.session.commit()


    return render_template("post.html")


@app.route('/post')
def show_post_form():
    if 'user_id' not in session:
        flash("You need to be logged in for that!")
        return redirect('/login')


    #dropdown to select page HELP!

    user_id = session["user_id"]
    platform = Platform.query.filter_by(user_id=user_id).first()
  
    access_token = platform.access_token

    api = GraphAPI(access_token)

    page_response = api.get_connections("me", "accounts")
    
    return render_template("post.html", pages=page_response["data"])

@app.route('/confirm', methods=['POST'])
def confirm_post():

    if 'user_id' not in session:
        flash("You need to be logged in for that!")
        return redirect('/login')



    page_id = request.form.get("page_id")
    msg = request.form.get("userpost")
    scheduled_publish_time = request.form.get('publish_timestamp')

    user_id = session["user_id"]
    platform = Platform.query.filter_by(user_id=user_id).first()
  
    access_token = platform.access_token


    api = GraphAPI(access_token)


    access_token_response = api.get_object(id=page_id, fields='access_token')

    page_token = access_token_response['access_token']


    # ***Need to test later to see if this works for useres other than Admin***

    # pages = api.get_connections("me", "accounts")

    # for page in pages["data"]:
        # if page_id == page['id']:
            # page_token = page['access_token']


    page_api = GraphAPI(page_token)

    status = page_api.put_object(parent_object='me', connection_name='feed', scheduled_publish_time=scheduled_publish_time, published=False,
                 message=msg)

    print status
    # page_api.put_wall_post(msg)

    # status = api.put_wall_post(msg)


    return render_template("/confirm.html")
    # return render_template("/confirm.html", hour=hour, minute=minute, timezone=timezone, ampm=ampm, userpost=userpost, monthyear=monthyear)

@app.route('/myposts')
def show_posts():
    if 'user_id' not in session:
        flash("You need to be logged in for that!")
        return redirect('/login')

    return render_template("myposts.html")


@app.route('/fbbutton')
def test():
    return render_template("fbbutton.html")




if __name__ == "__main__":
    app.debug = True
    connect_to_db(app)
    app.run(host="0.0.0.0")
