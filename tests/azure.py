import sys, os
sys.path.append(os.path.relpath(".."))
##TODO: import code from scripts in parent directory
from AzureConnection import getConnString
from PetConnect import getTotal
from sqlalchemy import create_engine, text
import unittest, pytest

class connectionTest(unittest.TestCase):
    def test_connection(self):
        creds = getConnString()
        result = False
        try:
            eng = create_engine("postgresql+psycopg2://"+creds['user']+":"+creds['password']+"@"+creds ['host']+":5432/"+creds['database'], connect_args={'sslmode': "allow"})
            conn = eng.connect()
            conn.close()
            result = True
        except Exception as err:
            result = False
        assert result == True
"""    def test_activeCount():
        creds = getConnString()
        result = False
        try:
            eng = create_engine("postgresql+psycopg2://"+creds['user']+":"+creds['password']+"@"+creds['host']+":5432/"+creds['database'], connect_arg={'sslmode': "allow"})
            conn = eng.connect()
            conn.execute(text('SELECT COUNT("Animal_id") FROM dogs WHERE "Status" = \'Active\';'))
"""
if __name__=="__main__":
    unittest.main()