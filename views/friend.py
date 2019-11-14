from db.db import conn
from flask import request, redirect, session, url_for, render_template, make_response, Blueprint

friend = Blueprint('friend', __name__)

@friend.route('/all_friends', methods=['GET', 'POST'])
def all_friends():
    aid = request.cookies.get('aid')
    if aid is None or aid == "":
        return redirect(url_for("login.sign_in"))
    formed_aid = "'%s'" % (aid)
    sql = '''
    SELECT a2.aid, a2.name, a2.email
    FROM friend, account AS a1, account AS a2
    WHERE friend.aid_1 = a1.aid 
          AND a1.aid = ''' + formed_aid + ''' 
          AND friend.aid_2 = a2.aid
    UNION
    SELECT a2.aid, a2.name, a2.email
    FROM friend, account AS a1, account AS a2
    WHERE friend.aid_2 = a1.aid 
          AND a1.aid = ''' + formed_aid + ''' 
          AND friend.aid_1 = a2.aid 
    '''
    print(sql)

    def get_log_out_time(fid):
        formed_fid = "'%s'" % (fid)
        return '''
    SELECT logs.time
    FROM logs
    WHERE logs.if_log_in = False
          AND logs.time IS NOT NULL
          AND logs.aid = ''' + formed_fid + '''
    ORDER BY logs.time DESC 
    LIMIT 1
        '''
    #sql_2 = get_log_out_time()
    #print(sql_2)
    trans = conn.begin()
    try:
        cur = conn.execute(sql)
        trans.commit()
        friends = cur.fetchall()
        idx = range(len(friends))
        logs = []
        transs = []
        for id in idx:
            sql_2 = get_log_out_time(friends[id]['aid'])
            transs.append(conn.begin())
            try:
                cur = conn.execute(sql_2)
                transs[-1].commit()
                logs += cur.fetchall()
            except:
                transs[-1].rollback()
                return redirect(url_for("friend.all_friends"))

        return render_template("/friend/Friend.html", friends=friends, idx=idx, logs=logs)
    except:
        trans.rollback()
        return redirect(url_for("friend.all_friends"))


@friend.route('/add_friend', methods=['GET', 'POST'])
def add_friend():
    aid = request.cookies.get('aid')
    if aid is None or aid == "":
        return redirect(url_for("login.sign_in"))
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
    trans = conn.begin()
    try:
        conn.execute(sql)
        trans.commit()
    except:
        trans.rollback()
    return redirect('all_friends')

