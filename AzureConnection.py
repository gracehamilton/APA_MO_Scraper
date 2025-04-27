from sqlalchemy import engine, create_engine, text
import sys, os
sys.path.append(os.path.relpath("config"))
from config import load_config # type: ignore
import pandas as pd
#from socket import gethostname, gethostbyname

def getConnString():
    config = load_config(section='azure')
    config['sslmode'] = 'require'
    return config

def AzureLoad(df):
    config = getConnString()
    eng = create_engine("postgresql+psycopg2://"+config['user']+":"+config['password']+"@"+config['host']+":5432/"+config['database'], connect_args={'sslmode': "allow"})
    with eng.connect().execution_options(isolation_level="AUTOCOMMIT", schema_translate_map={None:'public'}) as conn:
        try: 
            df.to_sql('dogs', eng, index=False, if_exists='append')
            conn.close()
        except Exception as err: #TODO: log errors if unable to connect to SQL DB
            print(err.args)