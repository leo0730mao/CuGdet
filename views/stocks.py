from db import db
from db.db import conn
from flask import request, redirect, session, url_for, render_template, make_response, Blueprint


stocks = Blueprint('stocks', __name__)


@stocks.route('/stock_market', methods=['GET', 'POST'])
def stock_market():
    aid = request.cookies.get('aid')
    if aid is None or aid == "":
        return redirect(url_for("login.sign_in"))
    page = request.form.get('page')
    if page is None or page == "" or int(page) < 0:
        page = 0
    else:
        page = int(page)
    sql = """select s.sid, s.name, s.type, s.info, c.price from (select * from stocks order by sid limit 10 offset %s) as s INNER JOIN current_price as c on s.sid = c.sid;""" % (page * 10)
    all_stocks = db.special_select(sql)

    pre_page = max(0, page - 1)
    nxt_page = page + 1
    return render_template("/stocks/StockMarket.html", all_stocks = all_stocks, page = page, pre_page = pre_page, nxt_page = nxt_page)


@stocks.route('/rec_stock', methods=['GET', 'POST'])
def rec_stock():
    aid = request.cookies.get('aid')
    if aid is None or aid == "":
        return redirect(url_for("login.sign_in"))
    sql = """select s.sid, s.name, s.type, s.info, c.price from (select * from rec_stk where aid = 
    '%s') as r INNER JOIN stocks as s on r.sid = s.sid INNER JOIN current_price as c on s.sid = c.sid;""" % aid
    rec_stocks = db.special_select(sql)
    return render_template("/stocks/RecStock.html", rec_stocks = rec_stocks)


@stocks.route('/own_stock', methods=['GET', 'POST'])
def own_stock():
    aid = request.cookies.get('aid')
    if aid is None or aid == "":
        return redirect(url_for("login.sign_in"))
    sql = """select s.sid, s.name, s.type, s.info, c.price as cur_price, o.price as old_price, o.num as num from (select * from 
    own_stk where aid = '%s') as o INNER JOIN stocks as s on o.sid = s.sid INNER JOIN current_price as c on 
    s.sid = c.sid;""" % aid
    own_stocks = db.special_select(sql)
    return render_template("/stocks/OwnStock.html", own_stocks = own_stocks)


@stocks.route('/buy_stock', methods=['GET', 'POST'])
def buy_stock():
    aid = request.cookies.get('aid')
    if aid is None or aid == "":
        return redirect(url_for("login.sign_in"))
    data = {'aid': aid, 'sid': request.form.get('sid'), 'num': int(request.form.get('num')),
            'price': float(request.form.get('price'))}
    tmp = db.select(conn, 'own_stk', "*", {'sid': data['sid'], 'aid': aid})
    if len(tmp) == 0:
        db.insert(conn, 'own_stk', data)
    else:
        new_num = int(tmp[0]['num']) + data['num']
        new_price = (float(tmp[0]['price']) * int(tmp[0]['num']) + data['num'] * data['price']) / new_num
        db.update(conn, 'own_stk', {"=": {'price': new_price, 'num': new_num}}, {'sid': data['sid'], 'aid': aid})
    return redirect(url_for(".own_stock"))


@stocks.route('/sell_stock', methods=['GET', 'POST'])
def sell_stock():
    aid = request.cookies.get('aid')
    if aid is None or aid == "":
        return redirect(url_for("login.sign_in"))
    sid = request.form.get('sid')
    old_price = float(request.form.get('old_price'))
    cur_price = float(request.form.get('cur_price'))
    sell_num = int(request.form.get('sell_num'))
    num = int(request.form.get('num'))
    if sell_num >= num:
        db.delete(conn, 'own_stk', {'aid': aid, 'sid': request.form.get('sid')})
    else:
        new_num = num - sell_num
        new_price = (old_price * num - cur_price * sell_num) / new_num
        db.update(conn, 'own_stk', {"=": {'price': new_price, 'num': new_num}}, {'sid': sid, 'aid': aid})
    return redirect(url_for(".own_stock"))
