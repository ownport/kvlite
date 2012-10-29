import sys
if '' not in sys.path:
    sys.path.append('')

import kvlite
import unittest

from kvlite import MysqlCollection
from kvlite import MysqlCollectionManager

from kvlite import cPickleSerializer
from kvlite import CompressedJsonSerializer


class KvliteMysqlTests(unittest.TestCase):

    def setUp(self):
        URI = 'mysql://kvlite_test:eixaaghiequ6ZeiBahn0@localhost/kvlite_test'

        self.collection_name = 'kvlite_test'
        self.manager = MysqlCollectionManager(URI)
        
        if self.collection_name not in self.manager.collections():
            self.manager.create(self.collection_name)
            
        collection_class = self.manager.collection_class
        self.collection = collection_class(self.manager.connection, self.collection_name)

    def tearDown(self):
        
        if self.collection_name in self.manager.collections():
            self.manager.remove(self.collection_name)
        self.collection.close()
    
    def test_mysql_get_uuid(self):
        
        uuids = [self.collection.get_uuid() for i in range(1000)]
        self.assertEqual(len(set(uuids)), 1000)

    def test_put_get_delete_count_one(self):
        
        k = self.collection.get_uuid()
        v = 'test_put_one'
        self.collection.put(k, v)
        self.assertEqual(self.collection.get(k), (k,v))
        self.assertEqual(self.collection.count, 1)
        self.collection.delete(k)
        self.assertEqual(self.collection.count, 0)
        self.collection.commit()

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
        self.collection.commit()

    def test_long_key(self):
        
        self.assertRaises(RuntimeError, self.collection.get, '1'*41)
        self.assertRaises(RuntimeError, self.collection.put, '1'*41, 'long_key')
        self.assertRaises(RuntimeError, self.collection.delete, '1'*41)
    
    def test_absent_key(self):
        
        self.assertEqual(self.collection.get(u'a1b2c3'), (None,None))
    
    def test_incorrect_key(self):

        self.assertRaises(RuntimeError, self.collection.get, '12345')
        
    def test_use_different_serializators_for_many(self):
        URI = 'mysql://kvlite_test:eixaaghiequ6ZeiBahn0@localhost/kvlite_test'
        collection_name = 'diffser'

        manager = MysqlCollectionManager(URI)
        if collection_name not in manager.collections():
            manager.create(collection_name)

        collection_class = manager.collection_class
        collection = collection_class(manager.connection, collection_name, CompressedJsonSerializer)
        
        collection.put(u'11', u'diffser1')
        collection.put(u'22', u'diffser2')
        collection.put(u'33', u'diffser3')
        collection.commit()
        collection.close()

        manager = MysqlCollectionManager(URI)
        collection_class = manager.collection_class
        collection = collection_class(manager.connection, collection_name, cPickleSerializer)
        with self.assertRaises(RuntimeError):
            res = [(k,v) for k,v in collection.get()]
        
        collection.put(u'11', u'diffser1')
        collection.put(u'22', u'diffser2')
        collection.put(u'33', u'diffser3')
        collection.commit()
        collection.close()

        manager = MysqlCollectionManager(URI)
        collection_class = manager.collection_class
        collection = collection_class(manager.connection, collection_name, CompressedJsonSerializer)
        
        with self.assertRaises(RuntimeError):
            res = [(k,v) for k,v in collection.get()]
        collection.close()
        
                
if __name__ == '__main__':
    unittest.main()        

