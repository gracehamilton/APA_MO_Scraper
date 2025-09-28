import sys, os
sys.path.append(os.path.relpath(".."))

from AzureConnection import getConnString
from sqlalchemy import create_engine, text
from PetConnect import getTotal
import unittest

class connectionTest(unittest.TestCase):
    def test_credentials(self):
        creds=getConnString()
        self.assertIsNotNone(creds)
    def test_connection(self):
        creds = getConnString()
        result = False
        try:
            eng = create_engine("postgresql+psycopg2://"+creds['user']+":"+creds['password']+"@"+creds ['host']+":5432/"+creds['database'], connect_args={'sslmode': "allow"})
            conn = eng.connect()
            conn.close()
            result = True
        except Exception as err:
            print(err.args)
        self.assertTrue(result)
    def test_activeCount(self):
        creds = getConnString()
        try:
            eng = create_engine("postgresql+psycopg2://"+creds['user']+":"+creds['password']+"@"+creds ['host']+":5432/"+creds['database'], connect_args={'sslmode': "allow"})
            conn = eng.connect()
            dbcount = conn.execute(text('SELECT COUNT("Animal_id") FROM dogs WHERE "Status" = \'Active\';')).fetchone()[0]
            conn.close()
            inPetConnect = getTotal()
            if dbcount > inPetConnect:
                raise Exception("Database has more active records than live data. Will need to retire some records")
            self.assertEqual(getTotal(), dbcount)
        except Exception as err:
            self.fail(err.args)

if __name__=="__main__":
    #unittest.main()
    creds = getConnString()
    eng = create_engine("postgresql+psycopg2://"+creds['user']+":"+creds['password']+"@"+creds ['host']+":5432/"+creds['database'], connect_args={'sslmode': "allow"})
    conn = eng.connect()
    arr = conn.execute(text('SELECT COUNT("Animal_id") FROM dogs WHERE "Status" = \'Active\';'))
    conn.close()
    print(arr.fetchone()[0])
    print(getTotal())