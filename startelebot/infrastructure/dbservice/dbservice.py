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

    def get_client_data(self, document):
        try:
            sql = '''
                SELECT 
                    ABALPH AS "name",
                    ABAN8 AS "client_code"
                FROM F0101
                WHERE TRIM(ABTAX) = :document
                AND TRIM(ABAT1) IN ('E','C')
                AND TRIM(ABSIC) = 'A'
            '''
            params = {
                "document": document,
            }
            self.oracle_db.set_schema(settings.oracle_schema)
            self.oracle_db.execute(sql, params)
            result = self.oracle_db.fetchone()
            return result
        except Exception as error:
                    pass
        
    def get_unpaid_invoices(self, client_code):
        try:
            sql = '''
                SELECT
                    SUBSTR(RPDOC,0,LENGTH(RPDOC)-2) AS "invoice_number",
                    SUBSTR(RPDOC,-2,2) AS "invoice_series" 
                FROM PRODDTA.F03B11
                WHERE RPAN8 = :client_code
                AND RPPST = 'A'
                AND RPDCT = 'RI'
                GROUP BY RPDOC, RPKCOO 
                ORDER BY RPDOC DESC
            '''                 
            params = {
                "client_code": client_code,
            }
            self.oracle_db.set_schema(settings.oracle_schema)
            self.oracle_db.execute(sql, params)
            result = self.oracle_db.fetchall()
            return result
        except Exception as error:
                    pass

    def get_unpaid_ticket(self, client_document, invoice):
        try:
            sql = '''
                SELECT DISTINCT 
                    '237' 			AS "BANCO", 
                    COMPANY.ABTAX 	AS "CNPJCED",     
                    COMPANY.ABALPH 	AS "NOMECED", 
                    LPAD(SUBSTR(ACCOUNT.AYTNST,5,4),4,0) AS "BANCOAGCED", 
                    SUBSTR(ACCOUNT.AYTNST,10,1) 			AS "DIGBANCOCED", 
                    TRIM(ACCOUNT.AYCBNK ) 				AS "CONTACED4", 
                    TRIM(ACCOUNT.AYCBNK ) ||'-'|| ACCOUNT.AYCHKD  	AS "CONTACED",     
                    TO_CHAR(DTI.JD2DT(BOTRDJ),'DD/MM/YYYY') 	AS "DATA_EMISSAO", 
                    TO_CHAR(DTI.JD2DT(BODDJ),'DD/MM/YYYY') 	AS "DATA_VENCIMENTO", 
                    ROUND((BOAAP/100),2) 				AS "VL_BOLETO", 
                    '09' 								AS "CARTEIRA", 
                    SUBSTR(LPAD(TRIM(BOBBDN),11,0),1,11) AS "NOSSO_NUMERO", 
                    '/'||SUBSTR(BOBBDN,1,2)||'/'|| SUBSTR(BOBBDN,3,9) || '-' || SUBSTR(BOBBDN,12,1) AS "NOSSONROFORMAT",      
                    5 AS "DIAS_PROTESTO", 
                    'Protestar 5 dias corridos após vencimento' AS "INF_PROTESTO", 
                    TRIM(BOBNNF)||TRIM(BOBSER) AS "DOC",      
                    CLIENT.ABTAX  AS "CNPJSAC", 
                    CLIENT.ABALPH AS "NOMESAC", 
                    CONCAT(CONCAT(TRIM(CLIENT_ADDRESS.ALADD1),' Nº'),TRIM(CLIENT_ADDRESS.ALADD3)) AS "ENDSAC", 
                    CLIENT_ADDRESS.ALADD4 AS "NROSAC", 
                    CLIENT_ADDRESS.ALADD2 AS "BAIRROSAC", 
                    CLIENT_ADDRESS.ALCOUN AS "CIDADESAC", 
                    CLIENT_ADDRESS.ALADDZ AS "CEPSAC", 
                    CLIENT_ADDRESS.ALADDS AS "UFSAC", 
                    BOSFX, SHAN8, BOKCO , BOBNNF ,     
                    CONCAT(CONCAT(TRIM(COMPANY_ADDRESS.ALADD1),' Nº'),TRIM(COMPANY_ADDRESS.ALADD3)) AS "ENDCE1", 
                    TRIM(COMPANY_ADDRESS.ALADD2)||','||TRIM(COMPANY_ADDRESS.ALCOUN)||'-'||TRIM(COMPANY_ADDRESS.ALADDS) AS "ENDCE2" 
                FROM  PRODDTA.F55BOLET TICKET 
                    JOIN PRODDTA.F4201 HEADER ON HEADER.SHDOCO = TICKET.BODOCO AND HEADER.SHDCTO = TICKET.BOPDCT AND HEADER.SHKCOO = BOKCO  
                    JOIN PRODDTA.F0101 CLIENT ON HEADER.SHAN8 = CLIENT.ABAN8  
                    JOIN PRODDTA.F0116 CLIENT_ADDRESS ON HEADER.SHAN8 = CLIENT_ADDRESS.ALAN8  
                    JOIN PRODDTA.F0101 COMPANY ON TICKET.BOKCO = COMPANY.ABAN8 AND COMPANY.ABAT1 = 'O'  
                    JOIN PRODDTA.F0030 ACCOUNT ON ACCOUNT.AYAN8 = TICKET.BOKCO              
                    JOIN PRODDTA.F0116 COMPANY_ADDRESS ON TICKET.BOKCO = COMPANY_ADDRESS.ALAN8  
                WHERE TRIM(CLIENT.ABTAX) = :client_document
                    AND BOBNNF = :invoice
                    AND HEADER.SHRYIN IN('Y')
                    AND HEADER.SHDCTO IN('SO','VG','ED')
                    AND HEADER.SHKCOO IN('00010','00050','00030')
            '''
            params = {
                "client_document": client_document,
                "invoice": invoice
            }
            self.oracle_db.set_schema(settings.oracle_schema)
            self.oracle_db.execute(sql, params)
            result = self.oracle_db.fetchall()
            return result
        except Exception as error:
                    pass