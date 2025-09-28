import sys,os
sys.path.append(os.path.relpath(".."))
import dotenv
import unittest

class envTest(unittest.TestCase):
    def test_creds(self):
        config = dotenv.dotenv_values("usr/local/APAScraper/.env")
        print(config)
        self.assertIsNotNone(config)

if __name__=="__main__":
    #print(filepath)
    example = envTest()
    print(example.test_creds())