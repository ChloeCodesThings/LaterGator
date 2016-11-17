from flask import Flask, render_template, request, flash, redirect, session

from facebook import GraphAPI

from model import connect_to_db, db, User, Platform, Post, TwitterInfo, TwitterPost

import time

import urlparse

import oauth2 as oauth


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "CC89"

@app.route('/')
def index():
    """Homepage for LaterGator"""

    if 'user_id' in session:
        user_id = session["user_id"]

        user = User.query.filter_by(user_id=user_id).first()
        username = user.username
        return render_template("logged_in_page.html", username=username)

    else:
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

    if user:
        flash("Please choose another username! That one is taken")
        return redirect("/register")

    else:

        #Create new user
        new_user = User(username=username, password=password)

        #Add new user to database
        db.session.add(new_user)
        db.session.commit()

        #Creates session with current user
        session["user_id"] = new_user.user_id

        flash("You now have an account %s!" % username)
        return redirect("/")


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

    elif user.password != password:
        flash("Incorrect password")
        return redirect("/login")

    else:
        session["user_id"] = user.user_id
        flash("You are now logged in")
        return redirect("/")

@app.route('/logout')
def logout_user():

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

    platform_info = Platform.query.filter_by(facebook_user_id=facebook_user_id, user_id=session['user_id']).first()

    if not platform_info:
        platform_info = Platform(user_id=session["user_id"], access_token=access_token, facebook_user_id=facebook_user_id)


    else:
        platform_info.access_token = access_token

    db.session.add(platform_info)
    db.session.commit()


    return "success"

@app.route('/post_twitter')
def show_post_form():
    if 'user_id' not in session:
        flash("You need to be logged in for that!")
        return redirect('/')

    user_id = session["user_id"]
    twitterprofile = TwitterInfo.query.filter_by(user_id=user_id).first()

    oauth_token = twitterprofile.oauth_token
    user = User.query.filter_by(user_id=user_id).first()
    username = user.username
        
    return render_template("post_twitter.html", username=username)


@app.route('/post_pages')
def show_post_form_pages():
    if 'user_id' not in session:
        flash("You need to be logged in for that!")
        return redirect('/')

    user_id = session["user_id"]
    platform = Platform.query.filter_by(user_id=user_id).first()
  
    access_token = platform.access_token

    api = GraphAPI(access_token)
    
    page_response = api.get_connections("me", "accounts")
    
    return render_template("post_pages.html", pages=page_response["data"])


@app.route('/post_profile')
def show_post_form_profile():
    if 'user_id' not in session:
        flash("You need to be logged in for that!")
        return redirect('/')

    user_id = session["user_id"]
    platform = Platform.query.filter_by(user_id=user_id).first()
  
    access_token = platform.access_token
    user = User.query.filter_by(user_id=user_id).first()
    username = user.username
        
    return render_template("post_profile.html", username=username)





@app.route('/confirm_pages', methods=['POST'])
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

    page_api = GraphAPI(page_token)

    page_api.put_object(parent_object='me', connection_name='feed', scheduled_publish_time=scheduled_publish_time, published=False,
                 message=msg)

    #insert response['post_id'] into post DB

    #return redirect("/posts/{ID}")

    page_response = api.get_connections("me", "accounts")

    pages = page_response["data"]

    all_posts_regardless_of_page = []
    published_posts = []
    unpublished_posts = []

    for page in pages:
        current_page_id = str(page['id']) #getting current page id

        #getting page's posts
        
        post_rsp=api.get_connections(id=current_page_id, connection_name='promotable_posts', fields='is_published,message,id')

        for post in post_rsp['data']:
            # post_ids.append(post['id'])

            if post['is_published']:
                published_posts.append(post)
            else:
                unpublished_posts.append(post)


    return render_template("/confirm_page.html", time_to_show=time_to_show, published_posts=published_posts, unpublished_posts=unpublished_posts)
    # return render_template("/confirm.html", hour=hour, minute=minute, timezone=timezone, ampm=ampm, userpost=userpost, monthyear=monthyear)



# @app.route('/myposts')
# def show_posts():
#     if 'user_id' not in session:
#         flash("You need to be logged in for that!")
#         return redirect('/login')

#     user_id = session["user_id"]
#     platform = Platform.query.filter_by(user_id=user_id).first()
  
#     access_token = platform.access_token
#     api = GraphAPI(access_token)
    
#     page_response = api.get_connections("me", "accounts")

#     pages = page_response["data"]

#     all_posts_regardless_of_page = []
#     published_posts = []
#     unpublished_posts = []

#     for page in pages:
#         current_page_id = str(page['id']) #getting current page id

#         #getting page's posts
        
#         post_rsp=api.get_connections(id=current_page_id, connection_name='promotable_posts', fields='is_published,message')

#         for post in post_rsp['data']:
#             # post_ids.append(post['id'])

#             if post['is_published']:
#                 published_posts.append(post)
#             else:
#                 unpublished_posts.append(post)




#             # for each_post in all_posts_regardless_of_page:
#             #     message = each_post['message']
#             #     is_published = each_post['is_published']




#         # post_ids = [ p['id'] for p in  post_rsp['data']] #getting post ids





#     return render_template("myposts.html", published_posts=published_posts, unpublished_posts=unpublished_posts)


# @app.route('/fbbutton')
# def test():
#     return render_template("fbbutton.html")

@app.route('/confirm_profile', methods=['POST'])
def add_post_to_db():
    """Add post info to db"""

    if 'user_id' not in session:
        flash("You need to be logged in for that!")
        return redirect('/login')

    user_id = session["user_id"]
    msg = request.form.get("userpost")
    scheduled_publish_time = int(request.form.get('publish_timestamp'))
    platform = Platform.query.filter_by(user_id=user_id).one()
    platform_id = platform.platform_id
    time_to_show = request.form.get('time_to_show')


    new_post = Post(msg=msg, post_datetime=scheduled_publish_time, user_id=session["user_id"], platform_id=platform_id)
    

        #Add new user to database
    db.session.add(new_post)
    db.session.commit()

    return render_template("confirm_profile.html", time_to_show=time_to_show)


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

        #Add new user to database
    db.session.add(new_twitter_post)
    db.session.commit()

    return render_template("confirm_twitter.html", time_to_show=time_to_show)


@app.route('/send_posts_later')
def check_for_posts():
    """Checks to see if posts need to be sent, and sends them"""

    unpublished_statuses = Posts.query.filter_by(is_posted=False).all()
    current_time = time.time()

    for post in unpublished_statuses:
        time_to_be_posted = post.post_datetime

        if time_to_be_posted < current_time:

            msg = post.msg
            user_id = post.user_id
            platform = Platform.query.filter_by(user_id=user_id).first()
            access_token = platform.access_token
            api = GraphAPI(access_token)

            api.put_object(parent_object='me', connection_name='feed', message=msg)

            post.update().values(is_posted=True)



    return 

@app.route('/twitter_oauth')
def twitter_oauth():
    """3-legged OAuth for Twitter"""

    consumer_key =  'CMAhx22eA4kSoi4g30QFy8qZo'
    consumer_secret =   'x0V8HY8fgSCPoDVw3qZ45FRJ4vtxIKN2z9o1cliCs5kl1qlaQb'


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


    return redirect("%s?oauth_token=%s" % (authorize_url, request_token['oauth_token']))



@app.route('/add_twitter_token')
def add_twitter_token():
    """Add token to db"""

    oauth_token_secret = session['secret']

    oauth_token = request.args.get('oauth_token')

    twitter_info = TwitterInfo.query.filter_by(oauth_token=oauth_token, user_id=session['user_id']).first()

    if not twitter_info:
        twitter_info = TwitterInfo(user_id=session["user_id"], oauth_token=oauth_token, oauth_token_secret=oauth_token_secret)


    else:
        twitter_info.oauth_token = oauth_token

    db.session.add(twitter_info)
    db.session.commit()


    return redirect("/")

if __name__ == "__main__":
    app.debug = True
    connect_to_db(app)
    app.run(host="0.0.0.0")
