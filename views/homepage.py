import random
import string
from flask import request, redirect, session, url_for, render_template, Blueprint

from db.db import conn
from db import db
from db.utils import *


homepage = Blueprint('homepage', __name__)
letters = [s for s in string.ascii_lowercase]
numbers = [str(i) for i in range(10)]


@homepage.route('/all_records', methods=['GET', 'POST'])
def all_records():
    aid = request.cookies.get('aid')
    if aid is None or aid == "":
        return redirect(url_for("login.sign_in"))
    records = db.select(conn, 'records', "*", {'aid': aid}, special = "ORDER BY time DESC")
    return render_template("/homepage/HomePage.html", records = records)


@homepage.route('/adding_record', methods=['GET', 'POST'])
def adding_record():
    aid = request.cookies.get('aid')
    if aid is None or aid == "":
        return redirect(url_for("login.sign_in"))
    return render_template("/homepage/AddingRecord.html")


@homepage.route('/add_record', methods=['GET', 'POST'])
def add_record():
    aid = request.cookies.get('aid')
    if aid is None or aid == "":
        return redirect(url_for("login.sign_in"))
    record = dict()
    record['name'] = request.form.get("name")
    record['be_from'] = request.form.get("be_from")
    record['be_to'] = request.form.get("be_to")
    record['amt'] = request.form.get("amt")
    record['tag'] = request.form.get("tag")
    record['time'] = request.form.get("time")
    record['remark'] = request.form.get("remark")
    record['aid'] = request.cookies.get("aid")

    reids = db.select(conn, 'records', ['reid'], dict())
    reids = [t['reid'] for t in reids]

    record['reid'] = ''.join(random.choice(letters + numbers) for j in range(10))
    while record['reid'] in reids:
        record['reid'] = ''.join(random.choice(letters + numbers) for j in range(10))

    db.insert(conn, 'records', record)

    # influence plans
    db.update(conn, "plans", {"-": {"credit": record['amt']}}, {'aid': aid})

    # influence win_honor
    valid_honor(conn, aid)

    return redirect(url_for('homepage.all_records'))


@homepage.route('/delete_record', methods = ['GET', 'POST'])
def delete_record():
    aid = request.cookies.get('aid')
    if aid is None or aid == "":
        return redirect(url_for("login.sign_in"))

    old_amt = request.form.get('old_amt')

    db.update(conn, "plans", {"+": {"credit": old_amt}}, {'aid': aid})
    db.delete(conn, 'records', {'reid': request.form.get('reid')})

    # influence win_honor
    valid_honor(conn, aid)

    return redirect(url_for(".all_records"))


@homepage.route('/modifing_record', methods = ['GET', 'POST'])
def modifing_record():
    aid = request.cookies.get('aid')
    if aid is None or aid == "":
        return redirect(url_for("login.sign_in"))
    reid = request.form.get("reid")
    record = db.select(conn, "records", "*", {'reid': reid})[0]
    return render_template("/homepage/ModifyRecord.html", record = record)


@homepage.route('/modify_record', methods=['GET', 'POST'])
def modify_record():
    aid = request.cookies.get('aid')
    if aid is None or aid == "":
        return redirect(url_for("login.sign_in"))
    record = dict()
    record['name'] = request.form.get("name")
    record['be_from'] = request.form.get("be_from")
    record['be_to'] = request.form.get("be_to")
    record['amt'] = request.form.get("amt")
    record['time'] = request.form.get("time")
    record['tag'] = request.form.get("tag")
    record['remark'] = request.form.get("remark")

    old_amt = request.form.get('old_amt')

    db.update(conn, "plans", {"+": {"credit": old_amt}}, {'aid': aid})
    db.update(conn, 'account', {"=": record}, {'aid': aid})
    db.update(conn, "plans", {"-": {"credit": record['amt']}}, {'aid': aid})

    # influence win_honor
    valid_honor(conn, aid)

    return redirect(url_for(".all_records"))

