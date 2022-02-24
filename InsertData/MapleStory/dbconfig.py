import pymysql

class DataBase():
    def __init__(self):
        self.db = pymysql.connect(host="(데이터베이스 서버 IP)", port=(데이터베이스 서버 포트), user="(데이터베이스 서버 아이디)", password="(데이터베이스 서버 비밀번호)", database="MapleStoryAPI", charset="utf8")
        self.cursor = self.db.cursor(pymysql.cursors.DictCursor)

    def execute(self, query, args = []):
        self.cursor.execute(query, args)

    def executeOne(self, query, args = []):
        self.cursor.execute(query, args)
        row = self.cursor.fetchone()
        return row

    def executeAll(self, query, args = []):
        self.cursor.execute(query, args)
        row = self.cursor.fetchall()
        return row

    def commit(self):
        self.db.commit()

    def close(self):
        self.db.close()