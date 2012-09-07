import kvlite
import unittest

class KvliteUtilsTests(unittest.TestCase):
        
    def test_parse_uri_sqlite(self):
        print kvlite.parse_uri('sqlite://')

        
if __name__ == '__main__':
    unittest.main()        

