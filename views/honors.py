from db import db
from db.db import conn
from flask import request, redirect, session, url_for, render_template, make_response, Blueprint

honors = Blueprint('honors', __name__)

@honors.route('/all_honors', methods=['GET', 'POST'])
def all_honors():
    aid = request.cookies.get('aid')
    if aid is None or aid == "":
        return redirect(url_for("login.sign_in"))
    formed_aid = "'%s'" % (aid)
    sql = '''
    SELECT honors.name
    FROM honors, win_honor
    WHERE honors.hid = win_honor.hid 
          AND win_honor.aid = ''' + formed_aid

    print(sql)
    trans = conn.begin()
    try:
        cur = conn.execute(sql)
        trans.commit()
        honors = cur.fetchall()
        return render_template("/honors/Honors.html", honors=honors)
    except:
        trans.rollback()
        return redirect(url_for("all_honors"))

@honors.route('/locked_honors', methods=['GET', 'POST'])
def locked_honors():
    aid = request.cookies.get('aid')
    if aid is None or aid == "":
        return redirect(url_for("login.sign_in"))
    formed_aid = "'%s'" % (aid)
    sql = '''
    SELECT honors.name
    FROM honors
    EXCEPT
    SELECT honors.name
    FROM honors, win_honor
    WHERE honors.hid = win_honor.hid 
          AND win_honor.aid = ''' + formed_aid
    print(sql)
    trans = conn.begin()
    try:
        cur = conn.execute(sql)
        trans.commit()
        honors = cur.fetchall()
        return render_template("/honors/LockedHonors.html", honors=honors)
    except:
        trans.rollback()
        return redirect(url_for("all_honors"))