import kvlite
import unittest

from kvlite import MysqlCollection
from kvlite import MysqlCollectionManager

class KvliteMysqlTests(unittest.TestCase):

    def setUp(self):
        URI = 'mysql://kvlite_test:eixaaghiequ6ZeiBahn0@localhost/kvlite_test'
        collection_name = 'kvlite_test'
        
        manager = MysqlCollectionManager(URI)
        self.collection = manager.get_collection(collection_name)

    def tearDown(self):
        
        self.collection.close()
    
    def test_mysql_get_uuid(self):
        
        uuids = [self.collection.get_uuid() for i in range(1000)]
        self.assertEqual(len(set(uuids)), 1000)

    def test_put_one(self):
        
        k = self.collection.get_uuid()
        self.collection.put(k, 'test_put_one')
        k, v = self.collection.get(k)
        print k,v
        
if __name__ == '__main__':
    unittest.main()        

