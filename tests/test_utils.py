import kvlite
import unittest

class KvliteUtilsTests(unittest.TestCase):

    def test_get_uuid(self):
        
        uuids = kvlite.get_uuid(1000)
        self.assertEqual(len(set(uuids)), 1000)

    def test_sqlite_open(self):
        collection = kvlite.open('sqlite://tests/db/testdb.sqlite:kvlite_test')
        collection.put('a',1)
        self.assertEqual(collection.count,1)
        self.assertEqual(collection.get('a'), ('a',1))
        collection.delete('a')
        self.assertEqual(collection.count,0)
        self.assertEqual(collection.get('a'), (None,None))
        collection.close()
    
    def test_sqlite_remove(self):
        pass

    def test_mysql_open(self):
        pass

    def test_mysql_remove(self):
        pass

        
if __name__ == '__main__':
    unittest.main()        

