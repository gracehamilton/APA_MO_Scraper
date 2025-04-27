from sqlalchemy import engine, create_engine, text
import sys, os
sys.path.append(os.path.relpath("config"))
from config import load_config # type: ignore
import pandas as pd

def SQLLoad(df):
    config = load_config(section='sql')
    eng = create_engine("postgresql+psycopg2://"+config['user']+":"+config['password']+"@"+config['host']+":5432/dogdata")
    with eng.connect().execution_options(isolation_level="AUTOCOMMIT", schema_translate_map={None:'private_temp'}) as conn:
        try: 
            df.to_sql('alldata', eng, index=False, if_exists='append')
            conn.close()
        except Exception as err: #TODO: log errors if unable to connect to SQL DB
            print(err.args)