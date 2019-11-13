from db.db import conn
from flask import request, redirect, session, url_for, render_template, make_response, Blueprint

races = Blueprint('races', __name__)

@races.route('/in_races', methods=['GET', 'POST'])
def in_races():
    aid = request.cookies.get('aid')
    if aid is None or aid == "":
        return redirect(url_for("login.sign_in"))
    formed_aid = "'%s'" % (aid)
    sql = '''
    SELECT account.name as tname, races.rid, races.name 
    FROM races, in_race, account
    WHERE in_race.aid_1 = ''' + formed_aid + '''
          AND races.rid = in_race.rid
          AND in_race.aid_2 = account.aid
    UNION
    SELECT account.name as tname, races.rid, races.name
    FROM races, in_race, account
    WHERE in_race.aid_2 = ''' + formed_aid + '''
          AND races.rid = in_race.rid
          AND in_race.aid_2 = account.aid
    
    '''
    print(sql)
    trans = conn.begin()
    try:
        cur = conn.execute(sql)
        trans.commit()
        races = cur.fetchall()
        return render_template("/races/Races.html", races=races)
    except:
        trans.rollback()

@races.route('/race_rank', methods=['GET', 'POST'])
def race_rank():
    aid = request.cookies.get('aid')
    if aid is None or aid == "":
        return redirect(url_for("login.sign_in"))
    tname = request.form.get('tname')
    rid = request.form.get('rid')
    rname = request.form.get('name')
    formed_aid = "'%s'" % (aid)
    formed_tname = "'%s'" % (tname)
    formed_rid = "'%s'" % (rid)
    sql = """
    WITH ranking(aid_1, aid_2, name_1, name_2, amt, type) AS 
    (SELECT a1.aid, a2.aid, a1.name, a2.name, (SUM(r1.amt) + SUM(r2.amt)) AS amt, r.type
    FROM records as r1, records as r2, races as r, in_race as ir, account as a1, account as a2
    WHERE r.rid = """ + formed_rid + """
          AND r1.aid = a1.aid AND r2.aid = a2.aid
          AND ir.rid = r.rid
          AND r1.aid = ir.aid_1 AND r2.aid=ir.aid_2
          AND r.starting <= r1.time AND r.starting <= r2.time
          AND (r.tag IS NULL OR (r.tag = r1.tag AND r.tag = r2.tag))
          AND (r.ending IS NULL OR (r.ending >= r1.time AND r.ending >= r2.time) )
    GROUP BY a1.aid, a2.aid, r.type) 
    SELECT final_rank.name_1, final_rank.name_2, final_rank.amt, final_rank.rank 
    FROM (SELECT aid_1, aid_2, name_1, name_2, amt,
          ROW_NUMBER() OVER ( ORDER BY  
                              CASE WHEN rk.type='beq' THEN amt END DESC,
                              CASE WHEN rk.type='leq' THEN amt END ASC) AS rank
          FROM ranking AS rk
          ORDER BY rank ASC) AS final_rank(aid_1, aid_2, name_1, name_2, amt, rank)
     
    """
    print(sql)
    sql_2 = """
        WITH ranking(aid_1, aid_2, name_1, name_2, amt, type) AS 
    (SELECT a1.aid, a2.aid, a1.name, a2.name, (SUM(r1.amt) + SUM(r2.amt)) AS amt, r.type
    FROM records as r1, records as r2, races as r, in_race as ir, account as a1, account as a2
    WHERE r.rid = """ + formed_rid + """
          AND r1.aid = a1.aid AND r2.aid = a2.aid
          AND ir.rid = r.rid
          AND r1.aid = ir.aid_1 AND r2.aid=ir.aid_2
          AND r.starting <= r1.time AND r.starting <= r2.time
          AND (r.tag IS NULL OR (r.tag = r1.tag AND r.tag = r2.tag))
          AND (r.ending IS NULL OR (r.ending >= r1.time AND r.ending >= r2.time) )
    GROUP BY a1.aid, a2.aid, r.type) 
    SELECT final_rank.name_1, final_rank.name_2, final_rank.amt, final_rank.rank 
    FROM (SELECT aid_1, aid_2, name_1, name_2, amt,
          ROW_NUMBER() OVER ( ORDER BY  
                              CASE WHEN rk.type='beq' THEN amt END DESC,
                              CASE WHEN rk.type='leq' THEN amt END ASC) AS rank
          FROM ranking AS rk
          ORDER BY rank ASC) AS final_rank(aid_1, aid_2, name_1, name_2, amt, rank)
        WHERE (final_rank.aid_1 = """ + formed_aid + """ AND final_rank.name_2 = """ + formed_tname + """) 
           OR (final_rank.aid_2 = """ + formed_aid + """ AND final_rank.name_1 = """ + formed_tname + """)

        """
    print(sql_2)
    trans = conn.begin()
    try:
        cur = conn.execute(sql)
        trans.commit()
        ranking = cur.fetchall()
        trans = conn.begin()
        cur = conn.execute(sql_2)
        my_ranking = cur.fetchall()
        trans.commit()
        return render_template("/races/RaceRank.html", ranking=ranking, my_ranking=my_ranking, rname=rname)
    except:
        trans.rollback()
        return redirect(url_for("races.in_races"))

@races.route('/all_races', methods=['GET', 'POST'])
def all_races():
    aid = request.cookies.get('aid')
    if aid is None or aid == "":
        return redirect(url_for("login.sign_in"))
    sql = '''
    SELECT races.rid, races.name
    FROM races
    '''
    print(sql)
    trans = conn.begin()
    try:
        cur = conn.execute(sql)
        trans.commit()
        races = cur.fetchall()
        return render_template("/races/AllRaces.html", races=races)
    except:
        trans.rollback()

@races.route('/hot_races', methods=['GET', 'POST'])
def hot_races():
    aid = request.cookies.get('aid')
    if aid is None or aid == "":
        return redirect(url_for("login.sign_in"))
    sql = '''
    WITH race_count(rid, count, row_id) AS
(SELECT r.rid, COUNT(*), ROW_NUMBER () OVER (ORDER BY COUNT(*) DESC)
FROM in_race r INNER JOIN races rs on rs.rid = r.rid
WHERE CURRENT_TIMESTAMP>=rs.starting AND (rs.ending IS NULL OR CURRENT_TIMESTAMP<rs.ending)
GROUP BY r.rid
ORDER BY COUNT(*) DESC)

SELECT races.rid, races.name, race_count.count as participants
FROM race_count, races
WHERE race_count.row_id <= 10 AND race_count.rid = races.rid

UNION

SELECT races.rid, races.name, race_count.count as participants
FROM race_count, races
WHERE race_count.rid NOT IN (SELECT race_count.rid FROM race_count WHERE race_count.row_id=10) AND race_count.count IN (SELECT race_count.count FROM race_count WHERE race_count.row_id=10)
AND race_count.rid=races.rid

ORDER BY 
participants DESC
'''
    print(sql)
    trans = conn.begin()
    try:
        cur = conn.execute(sql)
        trans.commit()
        races = cur.fetchall()
        return render_template("/races/HotRaces.html", races=races)
    except:
        trans.rollback()

@races.route('/adding_race', methods=['GET', 'POST'])
def adding_race():
    aid = request.cookies.get('aid')
    if aid is None or aid == "":
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
    trans = conn.begin()
    try:
        cur = conn.execute(sql)
        trans.commit()
        friends = cur.fetchall()
        return render_template("/races/AddRace.html", friends=friends, rid=rid, name=name)
    except:
        trans.rollback()
        return redirect(url_for("races.all_races"))

@races.route('/add_race', methods=['GET', 'POST'])
def add_race():
    aid = request.cookies.get('aid')
    if aid is None or aid == "":
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
    trans = conn.begin()
    try:
        conn.execute(sql)
        trans.commit()
        sql_2 = '''
            SELECT account.name as tname, races.rid, races.name 
            FROM races, in_race, account
            WHERE in_race.aid_1 = ''' + formed_aid + '''
                  AND races.rid = in_race.rid
                  AND in_race.aid_2 = account.aid
            UNION
            SELECT account.name as tname, races.rid, races.name
            FROM races, in_race, account
            WHERE in_race.aid_2 = ''' + formed_aid + '''
                  AND races.rid = in_race.rid
                  AND in_race.aid_2 = account.aid

            '''
        print(sql_2)
        trans = conn.begin()
        cur = conn.execute(sql_2)
        trans.commit()
        races = cur.fetchall()
        return render_template("races/Races.html", races=races)
    except:
        trans.rollback()
        return redirect(url_for("races.in_races"))
