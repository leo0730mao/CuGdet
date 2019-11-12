import schedule
import time
import random
import string

import db.db
from db.db import conn
from datetime import datetime


letters = [s for s in string.ascii_lowercase]
numbers = [str(i) for i in range(10)]


def check_time(start_time, cycle):
    days = {"week": 1, "month": 30, "quarter": 90, "half-year": 180, "year": 365}
    start_time = start_time.split(" ")[0]
    d1 = datetime.strptime(start_time, '%Y-%m-%d')
    d2 = datetime.strptime(time.strftime("%Y-%m-%d", time.localtime()), '%Y-%m-%d')
    interval = (d2 - d1).days
    if interval % days[cycle] == 0:
        return True
    else:
        return False


def check_defaults():
    cur_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    sql = "select * from defaults where ending < '%s';" % cur_time
    defaults = db.special_select(sql)
    for default in defaults:
        if check_time(default['starting'], default['cycle']):
            record = dict()
            record['name'] = default['name']
            record['be_from'] = default['be_from']
            record['be_to'] = default['be_to']
            record['amt'] = default['amt']
            record['tag'] = default['tag']
            record['time'] = default['time']
            record['remark'] = default['remark']
            record['aid'] = default['aid']

            reids = db.select(conn, 'records', ['reid'], dict())
            reids = [t['reid'] for t in reids]

            record['reid'] = ''.join(random.choice(letters + numbers) for j in range(10))
            while record['reid'] in reids:
                record['reid'] = ''.join(random.choice(letters + numbers) for j in range(10))
            db.insert(conn, 'records', record)


if __name__ == '__main__':
    schedule.every().day.at("00:00").do(check_defaults)
    while True:
        schedule.run_pending()
        time.sleep(1)
