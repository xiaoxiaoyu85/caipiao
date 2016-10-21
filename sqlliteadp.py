#-*- encoding: utf-8 -*-

import os
import sys
import sqlite3

class SqliteAdp():
    def __init__(self, strDBFileName):
        BIN_DIR = os.path.dirname(__file__)
        strDBPath = os.path.join(BIN_DIR, strDBFileName)
        self.conn = sqlite3.connect(strDBPath)

    def GetConn(self):
        return self.conn

    def CreateTable(self, strSql):
        if strSql is not None and strSql != '':
            cu = get_cursor(self.conn)
            cu.execute(strSql)
            self.conn.commit()
            cu.close()
        else:
            return False
        return True

    def ExecuSql(self, strSql):
        try:
            if strSql is not None and strSql != '':
                cu = self.conn.cursor()
                cu.execute(strSql)
                self.conn.commit()
                cu.close()
            else:
                return False
        except Exception , e:
            return False
        return True
    
    def ExecuSearch(self, strSql):
        try:
            listRes = []
            if strSql is not None and strSql != '':
                cu = self.conn.cursor()
                cu.execute(strSql)
                self.conn.commit()
                listRes = cu.fetchall()
                cu.close()
            else:
                return listRes
        except Exception , e:
            return listRes
        return listRes












def InsertData(conn, sql):

    return True



 