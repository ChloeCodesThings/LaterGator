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


@app.route('/authorize_new_user', methods=['POST'])
def register_process():
    """Processes registration."""

    # Get form variables
    username = request.form.get("username")
    password = request.form.get("password")

    user = User.query.filter_by(username=username).first()

    if not user:

        #Create new user
        new_user = User(username=username, password=password)

        #Add new user to database
        db.session.add(new_user)
        db.session.commit()

        #Creates session with current user
        session["user_id"] = new_user.user_id

        flash("You now have an account %s!" % username)
        return render_template("auth_post_view.html", username=username)

    if user.username:
        flash("Please choose another username! That one is taken")
        return redirect("/register")



@app.route('/login')
def show_login():
    return render_template("login.html")

@app.route('/authorize', methods=['POST'])
def login_process():
    """Process login."""

    # Get form variables
    username = request.form.get("username")
    password = request.form.get("password")

    #Checks if user is in database
    user = User.query.filter_by(username=username).first()

    if not user:
        flash("No such user")
        return redirect("/login")

    if user.password != password:
        flash("Incorrect password")
        return redirect("/login")

    session["user_id"] = user.user_id

    flash("You are now logged in")
    return render_template("auth_post_view.html", username=username)

@app.route('/logout')
def logout_user():

    del session["user_id"]
    flash("You have been logged out- ttfn!")
    return redirect("/")




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


    return render_template("post.html") #necessary?


@app.route('/post')
def show_post_form():
    if 'user_id' not in session:
        flash("You need to be logged in for that!")
        return redirect('/login')

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
    time_to_show = request.form.get('time_to_show')
    user_input_time = '"time_to_show"'

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

    # page_posts = page_api.get_connections("me", "posts")


    page_api.put_object(parent_object='me', connection_name='feed', scheduled_publish_time=scheduled_publish_time, published=False,
                 message=msg)

    # print status
    # page_api.put_wall_post(msg)

    # status = api.put_wall_post(msg)


    return render_template("/confirm.html", time_to_show=time_to_show)
    # return render_template("/confirm.html", hour=hour, minute=minute, timezone=timezone, ampm=ampm, userpost=userpost, monthyear=monthyear)

@app.route('/myposts')
def show_posts():
    if 'user_id' not in session:
        flash("You need to be logged in for that!")
        return redirect('/login')

    user_id = session["user_id"]
    platform = Platform.query.filter_by(user_id=user_id).first()
  
    access_token = platform.access_token
    api = GraphAPI(access_token)
    
    page_response = api.get_connections("me", "accounts")

    pages = page_response["data"]

    all_posts_regardless_of_page = []
    published_posts = []
    unpublished_posts = []

    for page in pages:
        current_page_id = str(page['id']) #getting current page id

        print current_page_id
        #getting page's posts
        post_rsp=api.get_connections(id=current_page_id, connection_name='promotable_posts')

        

        for post in post_rsp['data']:
            # post_ids.append(post['id'])
            current_post_id = post['id']
            post_info = api.get_object(id=current_post_id, fields='is_published,message')

            if post_info['is_published']:
                published_posts.append(post_info)
            else:
                unpublished_posts.append(post_info)




            # for each_post in all_posts_regardless_of_page:
            #     message = each_post['message']
            #     is_published = each_post['is_published']




        # post_ids = [ p['id'] for p in  post_rsp['data']] #getting post ids





    return render_template("myposts.html", published_posts=published_posts, unpublished_posts=unpublished_posts)


@app.route('/fbbutton')
def test():
    return render_template("fbbutton.html")




if __name__ == "__main__":
    app.debug = True
    connect_to_db(app)
    app.run(host="0.0.0.0")
