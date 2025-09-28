from sqlalchemy import engine, create_engine, text
import sys, os
sys.path.append(os.path.relpath("config"))
import pandas as pd
from dotenv import dotenv_values
#from socket import gethostname, gethostbyname

def getConnString():
    config = dotenv_values("/usr/local/APAScraper/.env")
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

"""def AzureGetTables():
    config = getConnString()
    eng = create_engine("postgresql+psycopg2://"+config['user']+":"+config['password']+"@"+config['host']+":5432/"+config['database'], connect_args={'sslmode': "allow"})
    with eng.connect().execution_options(isolation_level="AUTOCOMMIT", schema_translate_map={None:'public'}) as conn:
        try:
            results = conn.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';"))
            conn.close()
            return results.fetchall()
        except Exception as err:
            print("Error with table pull: " + err.args)

def AzureGetSchemas(tables = AzureGetTables()):
    config = getConnString()
    eng = create_engine("postgresql+psycopg2://"+config['user']+":"+config['password']+"@"+config['host']+":5432/"+config['database'], connect_args={'sslmode': "allow"})
    totalStorage = []
    with eng.connect().execution_options(isolation_level="AUTOCOMMIT", schema_translate_map={None:'public'}) as conn:
        for t in tables:
            tableName = t[0]
            results = conn.execute(text("SELECT table_name, column_name, is_nullable, data_type, character_maximum_length FROM information_schema.columns WHERE table_name = '"+tableName+"' ORDER BY ordinal_position;"))
            tempStorage=results.fetchall()
            totalStorage += tempStorage
        conn.close()
    final =  pd.DataFrame(totalStorage, columns=["table", "name", "nullable", "type", "charLength"])
    return final"""

def AzureGetFunctions():
    config = getConnString()
    try:
        eng = create_engine("postgresql+psycopg2://"+config['user']+":"+config['password']+"@"+config['host']+":5432/"+config['database'], connect_args={'sslmode': "allow"})
        with eng.connect().execution_options(isolation_level="AUTOCOMMIT", schema_translate_map={None:'public'}) as conn:
                results = conn.execute(text("\df "))
                return results
    except Exception as err:
        print("Error with function pull: " + err.args )

def AzureGetAllWithStatus(status):
    config = getConnString()
    try:
        eng = create_engine("postgresql+psycopg2://"+config['user']+":"+config['password']+"@"+config['host']+":5432/"+config['database'], connect_args={'sslmode': "allow"})
        with eng.connect().execution_options(isolation_level="AUTOCOMMIT", schema_translate_map={None:'public'}) as conn:
            results = conn.execute(text('SELECT d.*, s.* FROM dogs d LEFT JOIN stay s ON d."Animal_id" = s.animal_id WHERE d."Status" = \''+status+'\';'))
            conn.close()
        resultsdf = pd.DataFrame(results.fetchall())
        return resultsdf
    except Exception as err:
        print("Error with "+status+" records pull: " + err.args)

if __name__ == "__main__":
    print(dotenv_values(".env"))
    df = pd.read_csv("output/dogData_20250907_1046.csv", sep=";")
    config = getConnString()
    eng = create_engine("postgresql+psycopg2://"+config['user']+":"+config['password']+"@"+config['host']+":5432/"+config['database'], connect_args={'sslmode': "allow"})
    with eng.connect().execution_options(isolation_level="AUTOCOMMIT", schema_translate_map={None:'public'}) as conn:
        df.to_sql('dogs', eng, index=False, if_exists='append')
        conn.close()
