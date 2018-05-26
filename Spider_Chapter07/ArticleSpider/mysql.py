# -*- coding:utf-8 -*-

import pymysql
from config import *



class MySQL(object):
    def __init__(self):
        self.db = pymysql.connect(MYSQL_HOST,MYSQL_USER,MYSQL_PASSWD,MYSQL_DB,charset="utf8",port=MYSQL_PORT)
        self.cursor = self.db.cursor()
    
    


    def insert(self,table,data):
        '''
        keys = ', '.join(data.keys())
        vales = list(data.values())
        print(vales)
        sql = "insert into {}({}) values('{}','{}','{}','{}','{}')".format(table,keys,vales[0],\
                        vales[1],vales[2],vales[3],vales[4])
        print(sql)
        try:
            self.cursor.execute(sql)
            flag = self.db.commit()
            if flag != 0:
                print("Insert Successfully")
        except Exception as e:
            _ = e
            print(e)
            self.db.rollback()
        '''


        keys = ','.join(data.keys())
        values = ','.join(['%s'] * len(data))
        sql_query = "insert into {} ({}) values ({}) ".format(table,keys,values)
        print(sql_query)
        print(type(data.values()))
        print(data.values())
        print(type(tuple(data.values())))
        try:
            self.cursor.execute(sql_query,tuple(data.values()))
            flag = self.db.commit()
            if flag != 0:
                print("insert successfully")
            pass
        except Exception as e:
            _ = e
            print(e.args)
            self.db.rollback()
        



if __name__ == '__main__':
    test = ['%s'] * 10
    print(test)