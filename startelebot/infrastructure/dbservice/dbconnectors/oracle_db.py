# -*- coding: utf-8 -*-
import cx_Oracle
import logging
from datetime import date
from startelebot.infrastructure.config import settings


class OracleDB:
    # logging.basicConfig(filename=f'..\\..\\log\\oracle_{str(date.today())}.log',
    #                     level=logging.ERROR,
    #                     format='%(asctime)s %(levelname)s %(funcName)s => %(message)s')

    def __init__(self):
        """
        Constructor method that create the connection.
        """
        try:
            self.con = cx_Oracle.connect(user=settings.oracle_username,
                                         password=settings.oracle_password,
                                         dsn=settings.oracle_host,
                                         encoding='utf-8')

            self.cursor = self.con.cursor()
        except Exception as error:
            logging.exception(f'Error at OracleDB() while connecting at database -> {error}')

    def __del__(self):
        self.close()

    def execute(self, sql, *args, **kwargs):
        try:
            self.cursor.execute(sql, *args, **kwargs)
        except Exception as error:
            self.rollback()
            logging.exception(f'Error at OracleDB() while executing a query({sql}) with that params ({args or kwargs}) -> {error}')
            raise Exception(f'Error at OracleDB() while executing a query({sql}) with that params ({args or kwargs}) -> {error}')

    def fetchall(self):
        try:
            self.cursor.rowfactory = self._make_dict_factory()  # calls the method to convert all result rows in a dict.
            return self.cursor.fetchall()
        except Exception as error:
            logging.exception(f'Error at OracleDB() while fetching a query({self.cursor.statement}) -> {error}')
            raise Exception(f'Error at OracleDB() while fetching a query -> {error}')

    def fetchone(self):
        try:
            self.cursor.rowfactory = self._make_dict_factory()  # calls the method to convert all result rows in a dict.
            return self.cursor.fetchone()
        except Exception as error:
            logging.exception(f'Error at OracleDB() while fetching a query({self.cursor.statement}) -> {error}')
            raise Exception(f'Error at OracleDB() while fetching a query -> {error}')

    def fetchone_teste(self):
        try:
            return self.cursor.fetchone()
        except Exception as error:
            logging.exception(f'Error at OracleDB() while fetching a query({self.cursor.statement}) -> {error}')
            raise Exception(f'Error at OracleDB() while fetching a query -> {error}')

    def set_schema(self, schema):
        self.con.current_schema = schema

    def close(self):
        self.con.close()

    def commit(self):
        self.con.commit()

    def rollback(self):
        self.con.rollback()

    def _make_dict_factory(self):
        if self.cursor.description:
            column_names = [d[0] for d in self.cursor.description]

            def create_row(*args):  # create a row as a dict
                return dict(zip(column_names, args))
            return create_row

    @property
    def rowcount(self):
        return self.cursor.rowcount

    @property
    def col_names(self):
        # For each column in the column list, bring the column name (first field of column).
        return [column[0] for column in self.cursor.description]


if __name__ == '__main__':
    oracledb = OracleDB()
    oracledb.set_schema(settings.oracle_schema)
    query = '''SELECT * FROM F0101'''
    oracledb.execute(query)
    result = oracledb.fetchone()
    print(result.get("ABALPH"))
