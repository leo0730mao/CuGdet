import random
import string

from db import db
from db.db import conn
from flask import request, redirect, session, url_for, render_template, make_response, Blueprint

defaults = Blueprint('defaults', __name__)
letters = [s for s in string.ascii_lowercase]
numbers = [str(i) for i in range(10)]


@defaults.route('/own_defaults', methods = ['GET', 'POST'])
def own_defaults():
    try:
        aid = request.cookies.get('aid')
    except:
        return redirect(url_for("login.sign_in"))
    defaults = db.select(conn, 'defaults', "*", {'aid': aid})
    return render_template("/defaults/OwnDefaults.html", defaults = defaults)


@defaults.route('/adding_defaults', methods = ['GET', 'POST'])
def adding_defaults():
    try:
        aid = request.cookies.get('aid')
    except:
        return redirect(url_for("login.sign_in"))
    return render_template("/defaults/AddingDefaults.html")


@defaults.route('/add_defaults', methods = ['GET', 'POST'])
def add_defaults():
    try:
        aid = request.cookies.get('aid')
    except:
        return redirect(url_for("login.sign_in"))
    default = {'aid': aid, 'name': request.form.get("name"), 'be_from': request.form.get("be_from"),
               'be_to': request.form.get("be_to"),
               'starting': request.form.get("starting"), 'ending': request.form.get("ending"),
               'cycle': request.form.get("cycle"), 'amt': request.form.get("amt"),
               'remark': request.form.get("remark"), 'tag': request.form.get("tag")}
    dids = db.select(conn, 'defaults', ['did'], dict())
    dids = set([t['did'] for t in dids])
    default['did'] = ''.join(random.choice(letters + numbers) for j in range(10))
    while default['did'] in dids:
        default['did'] = ''.join(random.choice(letters + numbers) for j in range(10))
    db.insert(conn, 'defaults', default)
    return redirect(url_for(".own_defaults"))


@defaults.route('/delete_defaults', methods = ['GET', 'POST'])
def delete_defaults():
    try:
        aid = request.cookies.get('aid')
    except:
        return redirect(url_for("login.sign_in"))
    db.delete(conn, 'defaults', {'did': request.form.get('did')})
    return redirect(url_for(".own_defaults"))
