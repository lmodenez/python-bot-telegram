#!/usr/bin/python
# -*- coding: UTF-8 -*-
from datetime import date, timedelta
from startelebot.infrastructure.dbservice.dbconnectors.oracle_db import OracleDB
from startelebot.infrastructure.config import settings


class DbService():

    def __init__(self):
        self.oracle_db = OracleDB()

    def get_user_login_data(self, user_id):
        try:
            sql = '''
                SELECT 
                    TLPRSID             AS user_id,
                    TLAN8               AS an8,
                    trim(TLCPWD)        AS password,
                    dti.jd2dt(TLCMPX)   AS expiration_date,
                    TLEDTM              AS expiration_time
                FROM PRODDTA.F55LOGTL
                WHERE TLPRSID = :id
            '''
            params = {
                "id": user_id
            }
            self.oracle_db.set_schema(settings.oracle_schema)
            self.oracle_db.execute(sql, params)
            return self.oracle_db.fetchone()
        except Exception as error:
            pass
    
    def increase_expiration_date(self, user_id, increase_days):
        try:
            sql = '''
                UPDATE F55LOGTL 
                SET TLCMPX = dti.dt2jd(:data)
                WHERE TLPRSID = :user_id
            '''
            params = {
                "user_id": user_id,
                "data": date.today() + timedelta(increase_days) 
            }
            self.oracle_db.set_schema(settings.oracle_schema)
            self.oracle_db.execute(sql, params)
            self.oracle_db.commit()
            return
        except Exception as error:
            pass



        


