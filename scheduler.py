from airflow import DAG
import datetime, sys, os
sys.path.append(os.path.relpath("tests"))
from tests.azure_test import connectionTest
from tests.files_test import envTest
from sqlalchemy import Engine, create_engine, text
from AzureConnection import getConnString

with DAG(
    dag_id="genericRun",
    start_date=datetime.datetime(2025, 9, 7, 12, 0),
    schedule="@daily"
):
    def runtest():
        envTest.test_creds()
        connectionTest.test_connection()
    
    def retirement():
        config = getConnString()
        eng = create_engine("postgresql+psycopg2://"+config['user']+":"+config['password']+"@"+config['host']+":5432/"+config['database'], connect_args={'sslmode': "allow"})
        try:
            with eng.connect().execution_options(isolation_level="AUTOCOMMIT", schema_translate_map={None:'public'}) as conn:
                result = conn.execute(text('SELECT retireexpiredrecords();'))
                return result
        except Exception as err:
            print("Error with function pull: " + err.args )