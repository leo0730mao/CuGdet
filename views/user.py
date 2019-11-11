import random
import string

from db.db import conn
from db import db
from flask import request, redirect, session, url_for, render_template, make_response, Blueprint

user = Blueprint('user', __name__)
letters = [s for s in string.ascii_lowercase]
numbers = [str(i) for i in range(10)]


@user.route('/profile', methods=['GET', 'POST'])
def profile():
    try:
        aid = request.cookies.get('aid')
    except:
        return redirect(url_for("login.sign_in"))
    p = db.select(conn, 'account', "*", {'aid': aid})[0]
    return render_template("/user/Profile.html", profile = p)


@user.route('/modify_profile', methods=['GET', 'POST'])
def modifying_profile():
    try:
        aid = request.cookies.get('aid')
    except:
        return redirect(url_for("login.sign_in"))
    account = dict()
    account['name'] = request.form.get("name")
    account['pwd'] = request.form.get("password")
    account['email'] = request.form.get("email")
    db.update(conn, 'account', {"=": account}, {'aid': aid})
    return redirect(url_for("user.profile"))
