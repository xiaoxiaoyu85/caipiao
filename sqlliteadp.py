#-*- encoding: utf-8 -*-

import os
import sys
import sqlite3

def GetConn(strDBFileName):
    BIN_DIR = os.path.dirname(__file__)
    strDBPath = os.path.join(BIN_DIR, strDBFileName)
    conn = sqlite3.connect(strDBPath)
    return conn

def get_cursor(conn):
    if conn is not None:
        return conn.cursor()
    else:
        return get_conn('').cursor()

def CreateTable(conn, sql):
    if sql is not None and sql != '':
        cu = get_cursor(conn)
        cu.execute(sql)
        conn.commit()
        cu.close()
    else:
        #print('the [{}] is empty or equal None!'.format(sql))
        return False
    return True

def InsertData(conn, sql):

    return True
 