import sys
if '' not in sys.path:
    sys.path.append('')

import unittest

from kvlite.managers import CollectionManager

class KvliteCollectionManagerTests(unittest.TestCase):

    def test_wrong_uri(self):
        
        URI = None
        self.assertRaises(RuntimeError, CollectionManager, URI)

    def test_mysql_manager(self):
        
        URI = 'mysql://kvlite_test:eixaaghiequ6ZeiBahn0@localhost/kvlite_test'
        collection_name = 'kvlite_test'
        
        manager = CollectionManager(URI)

        if collection_name in manager.collections():
            manager.remove(collection_name)
            
        self.assertNotIn(collection_name, manager.collections())

        manager.create(collection_name)
        self.assertIn(collection_name, manager.collections())

        manager.remove(collection_name)
        self.assertNotIn(collection_name, manager.collections())

    def test_sqlite_manager(self):
        
        URI = 'sqlite://tests/db/testdb.sqlite'
        collection_name = 'kvlite_test'
        
        manager = CollectionManager(URI)

        if collection_name in manager.collections():
            manager.remove(collection_name)
            
        self.assertNotIn(collection_name, manager.collections())

        manager.create(collection_name)
        self.assertIn(collection_name, manager.collections())

        manager.remove(collection_name)
        self.assertNotIn(collection_name, manager.collections())

    def test_unsupported_backend(self):
    
        URI = 'backend://database'
        self.assertRaises(RuntimeError, CollectionManager, (URI))        
        
        
if __name__ == '__main__':
    unittest.main()        

