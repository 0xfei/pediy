__author__ = '0x01f'

import sqlite3

class Cache:

    @staticmethod
    def create_database(filename='pediy.db'):
        try:
            conn = sqlite3.connect(filename)
            conn.execute(
                '''CREATE TABLE PEDIY_ARTICLES(TID INT NOT NULL PRIMARY KEY ,
                                              TITLE TEXT NOT NULL);''')
            conn.close()
        except Exception, e:
            print e.message
            return ''

    def __init__(self, filename='pediy.db'):
        self.conn = sqlite3.connect(filename)

    def __del__(self):
        self.conn.close()

    def lookup(self, tid):
        try:
            cursor = self.conn.execute("SELECT TID, TITLE from PEDIY_ARTICLES WHERE TID == %d" % int(tid))
            return cursor.fetchall()
        except Exception, e:
            print e.message
            return ''

    def insert(self, tid, title):
        try:
            s = "INSERT INTO PEDIY_ARTICLES (TID, TITLE) VALUES (%d, '%s')" % (int(tid), title)
            self.conn.execute(s)
            self.conn.commit()
            return 'Insert ' + tid + ' ' + title + ' success'
        except Exception, e:
            print e.message
            return ''

    def delete(self, tid):
        try:
            self.conn.execute("DELETE from PEDIY_ARTICLES where TID=%d;" % int(tid))
            self.conn.commit()
            return 'Delete ' + tid + ' success'
        except Exception, e:
            print e.message
            return ''

    def display_all(self):
        count = self.conn.execute("SELECT COUNT(*) FROM PEDIY_ARTICLES")
        print 'Number of items: ' + str(count.fetchall()[0][0])
        cursor = self.conn.execute("SELECT TID, TITLE from PEDIY_ARTICLES")
        for i in cursor.fetchall():
            print i[0], i[1]
