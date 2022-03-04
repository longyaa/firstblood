import pymysql
from dbutils.pooled_db import PooledDB
class PoolDB():
    def __init__(self, host="127.0.0.1", port=3306, user="data_group",
                 password="123456",
                 database="spider", charset='utf8', creator=pymysql, maxconnections=6, mincached=2, maxcached=5,
                 maxshared=3,
                 blocking=True, maxusage=None, setsession=None, ping=0):
        if setsession is None:
            setsession = []
        self.coon = PooledDB(host=host, port=port, database=database, user=user, password=password, charset=charset,
                             creator=creator, maxconnections=maxconnections, mincached=mincached, maxcached=maxcached,
                             maxshared=maxshared, blocking=blocking, maxusage=maxusage, setsession=setsession,
                             ping=ping)
        self.coon = self.coon.connection()
        self.cur = self.coon.cursor(cursor=pymysql.cursors.DictCursor)
        # DictCursor可以返回字典表示的记录，包含列名和他的值.如果不用DictCursor则返回列表，只有值

    def __enter__(self):
        return self.cur

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.coon.commit()
        self.cur.close()
        self.coon.close()
