from flask import Flask, request, redirect, session, url_for, render_template
import os
from datetime import timedelta

from views.defaults import defaults
from views.homepage import homepage
from views.login import login
from views.plans import plans
from views.stat import stat
from views.stocks import stocks
from views.honors import honors
from views.friend import friend
from views.races import races

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)

app.register_blueprint(homepage)
app.register_blueprint(login)
app.register_blueprint(plans)
app.register_blueprint(stat)
app.register_blueprint(stocks)
app.register_blueprint(defaults)
app.register_blueprint(honors)
app.register_blueprint(friend)
app.register_blueprint(races)

@app.route('/')
def index():
    return render_template('/login/SignIn.html')


if __name__ == '__main__':
    app.run(debug = True, port = 8080)
