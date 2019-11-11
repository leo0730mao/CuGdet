from db import db
from db.db import conn
from flask import request, redirect, session, url_for, render_template, make_response, Blueprint
from psycopg2.extras import RealDictCursor

honors = Blueprint('honors', __name__)

@honors.route('/all_honors', methods=['GET', 'POST'])
def all_honors():
    try:
        aid = request.cookies.get('aid')
    except:
        return redirect(url_for("login.sign_in"))
    print(request.cookies)
    formed_aid = "'%s'" % (aid)
    sql = '''
    SELECT honors.name
    FROM honors, win_honor
    WHERE honors.hid = win_honor.hid 
          AND win_honor.aid = ''' + formed_aid

    print(sql)
    try:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(sql)
        conn.commit()
        honors = cur.fetchall()
        return render_template("/honors/Honors.html", honors=honors)
    except:
        conn.rollback()
