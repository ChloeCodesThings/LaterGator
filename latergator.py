from flask import Flask, render_template, request, flash, redirect, session
import facebook

def main():

    access_token = "EAACEdEose0cBAHOB56Y9MUDXNKtyW2RDWyVDQE0YkdUyAKom6Nxb6c6ZCWCK8pvyePxO2H2rTs7xoZAHHShsJLmuExCbHHA44HJQkxAIZC796nnyL8MAZCXL15Cn0HwhRQsJDIRfOyu3vYJ11MUzPgPjujYeVlFEzoHUaEwZCv2DZB4HOAZBoFSGcI6cF38ZBCYZD"
    api = facebook.GraphAPI(access_token)
    msg = "testing"


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "YOLO"

@app.route('/')
def index():
    """Homepage login for LaterGator"""
    return render_template("homepage.html")

@app.route('/register', methods=['GET'])
def register_form():
    """Show register form to user"""

    return render_template("register.html")


@app.route('/register', methods=['POST'])
def register_process():
    """Processes registration."""

    # Get form variables
    username = request.form["username"]
    password = request.form["password"]

    # new_user = User(username=username, password=password)

    # db.session.add(new_user)
    # db.session.commit()

    # flash("User %s added." % email)
    flash("Welcome %s! You are (fake) logged in" % username)
    return render_template("auth_post_view.html", username=username)

@app.route('/loginpage')
def show_login():
    return render_template("login.html")

@app.route('/authorize', methods=['POST'])
def login_user():
    """Process login."""

    # Get form variables
    username = request.form.get("username")
    password = request.form.get("password")


    # user = User.query.filter_by(email=email).first()

    # if not user:
    #     flash("No such user")
    #     return redirect("/login")

    # if user.password != password:
    #     flash("Incorrect password")
    #     return redirect("/login")

    # session["user_id"] = user.user_id

    # flash("You are logged in, %s" % username)
    return render_template("auth_post_view.html", username=username)

# @app.route('/auth_post_view')
# def show_options():
#     """Show user options to auth, post, or view"""

#     username = request..get("username")

#     return render_template("auth_post_view.html", username=username)


@app.route('/authorize')
def show_authorize():
    return render_template("authorize.html")


@app.route('/post')
def show_post_form():
    return render_template("post.html")

@app.route('/confirm', methods=['POST'])
def confirm_post():
    hour = request.form.get("hour")
    minute = request.form.get("minute")
    timezone = request.form.get("timezone")
    ampm = request.form.get("ampm")
    userpost = request.form.get("userpost")
    monthyear = request.form.get("monthyear")

    return render_template("/confirm.html", hour=hour, minute=minute, timezone=timezone, ampm=ampm, userpost=userpost, monthyear=monthyear)

@app.route('/myposts')
def show_posts():
    return render_template("myposts.html")


@app.route('/fbbutton')
def test():
    return render_template("fbbutton.html")


if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0")
