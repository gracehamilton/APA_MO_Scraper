from sqlalchemy import engine, create_engine, text
import sys, os
sys.path.append(os.path.relpath("config"))
from config import load_config # type: ignore
from pandas import DataFrame
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

def AzureGetTables():
    config = getConnString()
    eng = create_engine("postgresql+psycopg2://"+config['user']+":"+config['password']+"@"+config['host']+":5432/"+config['database'], connect_args={'sslmode': "allow"})
    with eng.connect().execution_options(isolation_level="AUTOCOMMIT", schema_translate_map={None:'public'}) as conn:
        try:
            results = conn.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';"))
            conn.close()
            return results.fetchall()
        except Exception as err:
            print("Error with table pull: " + err.args)

def AzureGetSchemas():
    config = getConnString()
    eng = create_engine("postgresql+psycopg2://"+config['user']+":"+config['password']+"@"+config['host']+":5432/"+config['database'], connect_args={'sslmode': "allow"})
    tables = AzureGetTables()
    totalStorage = []
    with eng.connect().execution_options(isolation_level="AUTOCOMMIT", schema_translate_map={None:'public'}) as conn:
        for t in tables:
            tableName = t[0]
            results = conn.execute(text("SELECT table_name, column_name, is_nullable, data_type, character_maximum_length FROM information_schema.columns WHERE table_name = '"+tableName+"' ORDER BY ordinal_position;"))
            tempStorage=results.fetchall()
            totalStorage += tempStorage
        conn.close()
    return totalStorage

if __name__ == "__main__":
    print(AzureGetSchemas())