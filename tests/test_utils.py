import kvlite
import unittest

from kvlite import get_uuid

class KvliteUtilsTests(unittest.TestCase):

    def test_get_uuid(self):
        
        uuids = get_uuid(1000)
        self.assertEqual(len(set(uuids)), 1000)

        
if __name__ == '__main__':
    unittest.main()        

