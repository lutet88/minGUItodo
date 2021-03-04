import sqlite3
import os
import time

def commit(self):
    self.conn.commit()



class Database:
    def __init__(self, filename, tablename):
        self.conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), filename))
        self.tablename = tablename
        self.cursor = self.conn.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS " + tablename +
                            " (ID INTEGER PRIMARY KEY AUTOINCREMENT,"
                            " TIME INTEGER, NAME TEXT, COMMENT TEXT, DUE INTEGER, COMPLETE BOOLEAN default 0);")
        self.conn.commit()
        self.insertElements = " (TIME, NAME, COMMENT, DUE) "
        # current config:
        # [0] - ID
        # [1] - TIME
        # [2] - NAME
        # [3] - COMMENT
        # [4] - DUE
        # [5] - COMPLETE (0 or 1)


    def addValue(self, timestamp, name, comment, due=0):
        cmd = "INSERT INTO " + self.tablename + self.insertElements + "VALUES ("\
              + str(timestamp) + ", '"+ name + "','"\
              + comment + "',"+ str(due) + ")"
        # print(cmd)
        self.cursor.execute(cmd)
        commit(self)

    def queryTasks(self, minval, maxval):
        # print("SELECT * FROM " + self.tablename +" WHERE TIME BETWEEN " + str(minval) + " AND " + str(maxval))
        self.cursor.execute("SELECT * FROM " + self.tablename +" WHERE TIME BETWEEN " + str(minval) + " AND " + str(maxval))
        commit(self)
        return self.cursor.fetchall()

    def deleteBefore(self, val):
        self.cursor.execute("DELETE FROM "+self.tablename+" WHERE TIME < "+str(val))
        commit(self)

    def getEarliestTimestamp(self):
        self.cursor.execute("SELECT MIN(TIME) FROM "+self.tablename)
        commit(self)
        fetch = self.cursor.fetchone()
        return 0 if not fetch[0] else fetch[0]

    def getLatestTimestamp(self):
        self.cursor.execute("SELECT MAX(TIME) FROM "+self.tablename)
        commit(self)
        fetch = self.cursor.fetchone()
        # print(fetch)
        return 2**63 if not fetch[0] else fetch[0]

    def setComplete(self, id, complete=True):
        complete = 1 if complete else 0
        self.cursor.execute("UPDATE "+self.tablename+" SET COMPLETE = "+str(complete)+" WHERE ID = "+str(id) + ";")
        commit(self)

    def delete(self, id):
        self.cursor.execute("DELETE FROM "+self.tablename+" WHERE ID = "+str(id) + ";")
        commit(self)

    def close(self):
        commit(self)
        self.conn.close()


def test():
    db = Database("test.db", "the_table")
    db.addValue(int(time.time()), "Do A", "at this time please do this")
    print(db.queryTasks(0, 2**63))
    db.deleteBefore(2**63)
