#LaterGator

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