import random
import string
import time
from db.db import conn
from db import db
from flask import request, redirect, session, url_for, render_template, make_response, Blueprint

login = Blueprint('login', __name__)
letters = [s for s in string.ascii_lowercase]
numbers = [str(i) for i in range(10)]


@login.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    data = {'name': request.form.get("username"), 'pwd': request.form.get("password")}
    res = db.select(conn, 'account', ['aid'], data)
    if res is not None and len(res) != 0:
        log = dict()
        lids = db.select(conn, 'logs', ['lid'], dict())
        lids = set([t['lid'] for t in lids])
        log['lid'] = ''.join(random.choice(letters + numbers) for j in range(10))
        while log['lid'] in lids:
            log['lid'] = ''.join(random.choice(letters + numbers) for j in range(10))
        log['if_log_in'] = True
        log['time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        log['aid'] = res[0]['aid']
        db.insert(conn, 'logs', log)

        resp = make_response(redirect(url_for("homepage.all_records")))
        resp.set_cookie(key = 'aid', value = res[0]['aid'], expires = None)
        return resp
    else:
        return render_template('/login/SignIn.html', msg = "error user name or password")


@login.route('/to_sign_up', methods=['GET', 'POST'])
def to_sign_up():
    return render_template('/login/SignUp.html')


@login.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    data = {'username': request.form.get("username"), 'password': request.form.get("password"),
            'email': request.form.get("email")}

    aids = db.select(conn, 'account', ['aid'], dict())
    aids = set([t['aid'] for t in aids])
    data['aid'] = ''.join(random.choice(letters + numbers) for j in range(10))
    while data['aid'] in aids:
        data['aid'] = ''.join(random.choice(letters + numbers) for j in range(10))

    res = db.insert(conn, 'account', data)
    if res is True:
        sids = db.select(conn, "stocks", "*", dict())
        random.seed(time.time())
        rec_stk = random.sample(sids, 10)
        for stk in rec_stk:
            db.insert(conn, "rec_stk", {'aid': data['aid'], 'sid': stk['sid']})
        resp = make_response(redirect(url_for("homepage.all_records")))
        resp.set_cookie('aid', data['aid'])
        return resp
    else:
        return render_template('/login/SignUp.html', msg = "name or email duplicate")


@login.route('/sign_out', methods=['GET', 'POST'])
def sign_out():
    resp = make_response(redirect(url_for(".sign_in")))
    aid = request.cookies.get('aid')
    resp.delete_cookie('aid')

    log = dict()
    lids = db.select(conn, 'logs', ['lid'], dict())
    lids = set([t['lid'] for t in lids])
    log['lid'] = ''.join(random.choice(letters + numbers) for j in range(10))
    while log['lid'] in lids:
        log['lid'] = ''.join(random.choice(letters + numbers) for j in range(10))
    log['if_log_in'] = False
    log['time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    log['aid'] = aid
    db.insert(conn, 'logs', log)

    return resp
