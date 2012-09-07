import kvlite
import unittest

class KvliteUtilsTests(unittest.TestCase):

    def test_kvlite_open(self):
        print kvlite.open('sqlite://memory:test')                
        print kvlite.open('sqlite://tests/db/test.sqlite:test')                
        # print kvlite.open('mysql://memory:test')                
        
    def test_parse_uri_sqlite(self):
        pass

        
if __name__ == '__main__':
    unittest.main()        

