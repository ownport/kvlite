import unittest

from kvlite import CollectionManager

class KvliteCollectionManagerTests(unittest.TestCase):

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
        
        
        
if __name__ == '__main__':
    unittest.main()        
