import pymysql
import os
import dotenv


dotenv.load_dotenv()


class DBHelper:
    def __init__(self):
        self.host = os.environ['MYSQL_HOST']
        self.user = os.environ['MYSQL_USER']
        self.password = os.environ['MYSQL_PASS']
        self.db = os.environ['MYSQL_DATABASE']

    def __connect__(self):
        self.con = pymysql.connect(host=self.host,
                                   user=self.user,
                                   password=self.password,
                                   db=self.db)
        self.cur = self.con.cursor()

    def __disconnect__(self):
        self.con.close()

    def fetch(self, sql):
        self.__connect__()
        self.cur.execute(sql)
        result = self.cur.fetchall()
        self.__disconnect__()
        return result

    def execute(self, sql):
        self.__connect__()
        self.cur.execute(sql)
        self.__disconnect__()

    def insert(self, sql, val):
        self.__connect__()
        try:
            # inserting the values into the table
            self.cur.execute(sql, val)
            # commit the transaction
            self.con.commit()
        except:
            self.con.rollback()
        print(self.cur.rowcount, "record inserted!")
        self.con.close()
