from db import db
from db.db import conn
from flask import request, redirect, session, url_for, render_template, make_response, Blueprint


stat = Blueprint('stat', __name__)


@stat.route('/statistic', methods=['GET', 'POST'])
def statistic():
    aid = request.cookies.get('aid')
    if aid is None or aid == "":
        return redirect(url_for("login.sign_in"))
    data = dict()
    sql = """select tag as x, COUNT(tag) as y from records where aid = '%s' group by tag;""" % aid
    data['tag_num'] = db.special_select(sql)

    sql = """select be_from as x, COUNT(be_from) as y from records where aid = '%s' group by be_from;""" % aid
    data['source_num'] = db.special_select(sql)

    sql = """select be_to as x, COUNT(be_to) as y from records where aid = '%s' group by be_to;""" % aid
    data['receiver_num'] = db.special_select(sql)

    sql = """select date_part('day', time) as x, SUM(amt) as y from records where aid = '%s' group by date_part('day', time);""" % aid
    data['amt_daily'] = db.special_select(sql)

    sql = """select date_part('month', time) as x, SUM(amt) as y from records where aid = '%s' group by date_part('month', time);""" % aid
    data['amt_monthly'] = db.special_select(sql)

    return render_template("/stat/Statistic.html", data = data)
