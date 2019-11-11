from db.db import conn
from flask import request, redirect, session, url_for, render_template, make_response, Blueprint
from psycopg2.extras import RealDictCursor

races = Blueprint('races', __name__)

@races.route('/in_races', methods=['GET', 'POST'])
def in_races():
    try:
        aid = request.cookies.get('aid')
    except:
        return redirect(url_for("login.sign_in"))
    formed_aid = "'%s'" % (aid)
    sql = '''
    SELECT account.name as tname, races.name 
    FROM races, in_race, account
    WHERE in_race.aid_1 = ''' + formed_aid + '''
          AND races.rid = in_race.rid
          AND in_race.aid_2 = account.aid
    UNION
    SELECT account.name as tname, races.name
    FROM races, in_race, account
    WHERE in_race.aid_2 = ''' + formed_aid + '''
          AND races.rid = in_race.rid
          AND in_race.aid_2 = account.aid'''
    print(sql)
    try:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(sql)
        conn.commit()
        races = cur.fetchall()
        return render_template("/races/Races.html", races=races)
    except:
        conn.rollback()

@races.route('/all_races', methods=['GET', 'POST'])
def all_races():
    try:
        aid = request.cookies.get('aid')
    except:
        return redirect(url_for("login.sign_in"))
    sql = '''
    SELECT races.rid, races.name
    FROM races
    '''
    print(sql)
    try:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(sql)
        conn.commit()
        races = cur.fetchall()
        return render_template("/races/AllRaces.html", races=races)
    except:
        conn.rollback()

@races.route('/adding_race', methods=['GET', 'POST'])
def adding_race():
    try:
        aid = request.cookies.get('aid')
    except:
        return redirect(url_for("login.sign_in"))
    formed_aid = "'%s'" % (aid)
    rid = request.form.get("rid")
    name = request.form.get('name')
    sql = '''
        SELECT a2.name, a2.aid AS tid
        FROM friend, account AS a1, account AS a2
        WHERE friend.aid_1 = a1.aid 
              AND a1.aid = ''' + formed_aid + ''' 
              AND friend.aid_2 = a2.aid
        UNION
        SELECT a2.name, a2.aid AS tid
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
        return render_template("/races/AddRace.html", friends=friends, rid=rid, name=name)
    except:
        conn.rollback()
        return redirect(url_for("races.all_races"))

@races.route('/add_race', methods=['GET', 'POST'])
def add_race():
    try:
        aid = request.cookies.get('aid')
    except:
        return redirect(url_for("login.sign_in"))
    formed_aid = "'%s'" % (aid)
    tid = "'%s'" % request.form.get("tid")
    rid = "'%s'" % request.form.get('rid')
    data = ','.join([formed_aid, tid, rid])
    sql = '''
        INSERT INTO in_race (aid_1, aid_2, rid)
        VALUES (''' + data + ''')
        '''
    print(sql)
    try:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(sql)
        conn.commit()
    except:
        conn.rollback()
    return redirect(url_for("races.in_races"))