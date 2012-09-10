import unittest

import kvlite 
from kvlite import SqliteCollection
from kvlite import SqliteCollectionManager

class KvliteSqliteTests(unittest.TestCase):

    def setUp(self):
        URI = 'sqlite://tests/db/testdb.sqlite'

        self.collection_name = 'kvlite_test'
        self.manager = SqliteCollectionManager(URI)
        
        if self.collection_name not in self.manager.collections():
            self.manager.create(self.collection_name)
            
        collection_class = self.manager.collection_class
        self.collection = collection_class(self.manager.connection, self.collection_name)

    def tearDown(self):
        
        if self.collection_name in self.manager.collections():
            self.manager.remove(self.collection_name)
        self.collection.close()
    
    def test_put_get_delete_count_one(self):
        
        k = self.collection.get_uuid()
        v = 'test_put_one'
        self.collection.put(k, v)
        self.assertEqual(self.collection.get(k), (k,v))
        self.assertEqual(self.collection.count, 1)
        self.collection.delete(k)
        self.assertEqual(self.collection.count, 0)

    def test_put_get_delete_count_many(self):
        
        ks = list()
        for i in xrange(100):
            k = self.collection.get_uuid()
            v = 'test_{}'.format(i)
            self.collection.put(k, v)
            ks.append(k)
        
        kvs = [kv[0] for kv in self.collection.get()]
        self.assertEqual(len(kvs), 100)

        kvs = [kv for kv in self.collection.keys()]
        self.assertEqual(len(kvs), 100)

        self.assertEqual(self.collection.count, 100)
        for k in ks:
            self.collection.delete(k)
        self.assertEqual(self.collection.count, 0)

        
if __name__ == '__main__':
    unittest.main()        

