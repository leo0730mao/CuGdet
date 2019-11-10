import random
import string
from flask import request, redirect, session, url_for, render_template, Blueprint

from db.db import conn
from db import db


homepage = Blueprint('homepage', __name__)
letters = [s for s in string.ascii_lowercase]
numbers = [str(i) for i in range(10)]


@homepage.route('/all_records', methods=['GET', 'POST'])
def all_records():
    try:
        aid = request.cookies.get('aid')
    except:
        return redirect("signin")
    records = db.select(conn, {"": ['records']}, "*", {"T1": {'aid': aid}})
    return render_template("HomePage.html", records = records)


@homepage.route('/adding_record', methods=['GET', 'POST'])
def adding_record():
    try:
        aid = request.cookies.get('aid')
    except:
        return redirect("signin")
    return render_template("AddingRecord.html")


@homepage.route('/add_record', methods=['GET', 'POST'])
def add_record():
    try:
        aid = request.cookies.get('aid')
    except:
        return redirect("signin")
    record = dict()
    record['name'] = request.form.get("name")
    record['be_from'] = request.form.get("be_from")
    record['be_to'] = request.form.get("be_to")
    record['amt'] = request.form.get("amt")
    record['tag'] = request.form.get("tag")
    record['time'] = request.form.get("time")
    record['remark'] = request.form.get("remark")
    record['aid'] = request.cookies.get("aid")

    reids = db.select(conn, {"": ['records']}, {"T1": ['reid']}, dict())
    reids = [t['reids'] for t in reids]
    record['reid'] = ''.join(random.choice(letters + numbers) for j in range(10))
    while record['reid'] in reids:
        record['reid'] = ''.join(random.choice(letters + numbers) for j in range(10))

    db.insert(conn, 'records', record)
    return redirect('HomePage.html')
