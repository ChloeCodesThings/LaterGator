#LaterGator

![](https://github.com/ChloeCodesThings/LaterGator/blob/master/screenshots/latergator_readme.png "Welcome image")

LaterGator is a delayed status posting app that allows the user to post their status or tweet at a later scheduled time. In addition to letting the user choose their own time, the app also provides suggestions for the "next best time" to post content. The app uses Chrono (a natural language date parser in Javascript) to easily allow the user to adjust the time by simply typing in sentences such as "Next Wednesday at 1pm EST". LaterGator was originally intended to be used by people traveling internationally, so that they could make sure their awesome status updates were being posted at good times for their friends back home. However, it can also be used to help the user post during heavy traffic times on Twitter and Facebook.

##Contents
* [Tech Stack](#technologies)
* [Features](#features)
* [Installation](#install)
* [About Me](#aboutme)

## <a name="technologies"></a>Technologies
Backend: Python, Flask, PostgreSQL, SQLAlchemy<br/>
Frontend: JavaScript, jQuery, AJAX, Jinja2, Bootstrap, HTML5, CSS3<br/>
APIs: Facebook Graph API, Twitter<br/>

## <a name="features"></a>Features

Using a simple UI, users can create an account with LaterGator:
![](https://github.com/ChloeCodesThings/LaterGator/blob/master/screenshots/login_page_readme.png "Login Page Screenshot")

Users can then use Twitter and Facebook OAuth to give LaterGator publish access on their behalf:
![](https://github.com/ChloeCodesThings/LaterGator/blob/master/screenshots/fb_oauth_screenshot.png "FB OAuth Screenshot")

![](https://github.com/ChloeCodesThings/LaterGator/blob/master/screenshots/twitter_oauth_screenshot.png "Twitter OAuth Screenshot")


Next, they enter their status, and type in the time they would like it posted using phrases such as "Next Monday at 9am" or "In 1 hour" (the default time is the next best time to post based on LaterGator's research):
![](https://github.com/ChloeCodesThings/LaterGator/blob/master/screenshots/post_profile_screenshot.png "FB Profile Post Screenshot")

LaterGator takes care of the rest! Your status will be posted at your specified time.:
![](https://github.com/ChloeCodesThings/LaterGator/blob/master/screenshots/fb_confirm_screenshot.png "FB Profile Post Confirmation Screenshot")

## <a name="install"></a>Installation

To run LaterGator:

Install PostgreSQL (Mac OSX)

Clone or fork this repo:

```
https://github.com/chloecodesthings/latergator.git
```

Create and activate a virtual environment inside your LaterGator directory:

```
virtualenv env
source env/bin/activate
```

Install the dependencies:

```
pip install -r requirements.txt
```

Sign up to use the [FacebookGraph API](https://developers.facebook.com/apps/), and the [Twitter API](https://apps.twitter.com/).

Save your API keys in a file called <kbd>secrets.sh</kbd> using this format:

```
export TWITTER_CONSUMER_KEY="YOURKEYHERE"
export TWITTER_CONSUMER_SECRET="YOURKEYHERE"
export FACEBOOK_APP_SECRET="YOURKEYHERE"
export FACEBOOK_APP_ID="YOURKEYHERE"
```

Source your keys from your secrets.sh file into your virtual environment:

```
source secrets.sh
```

Set up the database:

```
createdb latergator
```


```
python model.py
```

Edit your crontab to run every minute while running this app (make sure to remove this when done, or it will keep running!):

```
crontab -e
```

```
#Run functions for LaterGator app
* * * * * /home/vagrant/src/my_hb_project/scheduled_run.sh
```

Create a cron.log file so you can check to see your logged cron info:

```
touch cron.log
```

Run the app:

```
python server.py
```

You can now navigate to 'localhost:5000/' to access LaterGator.

## <a name="aboutme"></a>About Me
Chloe Condon lives in the San Francisco Bay Area. This is her first software project which she made while attending Hackbright.


Before Hackbright, Chloe spent her nights and weekends performing around the Bay Area as a singer/actress on stage in musicals and solo performances. To support her theatre career, she spent her days working the tech world- ranging from working as an executive assistant to CEOs, working at large online video game companies, and even being the first in-house hire at a virtual personal assistant company. Seeing all these companies from support roles peaked her interest and she wanted to learn how the products she was working on were getting made. So, she started to learn to code on her own through online resources like CodeAcademy and TreeHouse. Chloe is looking forward to bringing her artistic background into the tech world as an engineer!


Visit her on [LinkedIn](https://www.linkedin.com/in/chloecondon).


![](https://github.com/ChloeCodesThings/LaterGator/blob/master/screenshots/chloecondonpic.png "Chloe Condon")