from db.db import conn
from flask import request, redirect, session, url_for, render_template, make_response, Blueprint
from psycopg2.extras import RealDictCursor

friend = Blueprint('friend', __name__)

@friend.route('/all_friends', methods=['GET', 'POST'])
def all_friends():
    try:
        aid = request.cookies.get('aid')
    except:
        return redirect(url_for("login.sign_in"))
    formed_aid = "'%s'" % (aid)
    sql = '''
    SELECT a2.name, a2.email
    FROM friend, account AS a1, account AS a2
    WHERE friend.aid_1 = a1.aid 
          AND a1.aid = ''' + formed_aid + ''' 
          AND friend.aid_2 = a2.aid
    UNION
    SELECT a2.name, a2.email
    FROM friend, account AS a1, account AS a2
    WHERE friend.aid_2 = a1.aid 
          AND a1.aid = ''' + formed_aid + ''' 
          AND friend.aid_1 = a2.aid 
    '''
    print(sql)
    try:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(sql)
        conn.commit()
        friends = cur.fetchall()
        return render_template("/friend/Friend.html", friends=friends)
    except:
        conn.rollback()


@friend.route('/add_friend', methods=['GET', 'POST'])
def add_friend():
    try:
        aid = request.cookies.get('aid')
    except:
        return redirect("signin")
    type = request.form.get("type")
    value = "'%s'" % (request.form.get(type))
    formed_aid = "'%s'" % (aid)

    sql = '''
        INSERT INTO friend (aid_1, aid_2)
        SELECT a1.aid, a2.aid
        FROM account a1, account a2
        WHERE a1.aid=''' + formed_aid + '''
              AND a2.''' + type + '''=''' + value + '''
    '''
    print(sql)
    try:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(sql)
        conn.commit()
    except:
        conn.rollback()
    return redirect('all_friends')

