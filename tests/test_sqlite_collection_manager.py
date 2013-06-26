import sys
if '' not in sys.path:
    sys.path.append('')


import unittest

from kvlite.managers import SqliteCollectionManager

class KvliteSqliteCollectionManagerTests(unittest.TestCase):

    def test_parse_uri_with_collection(self):
        params = SqliteCollectionManager.parse_uri('sqlite://tests/db/testdb.sqlite:kvlite_test')
        self.assertEqual(params['backend'], 'sqlite')
        self.assertEqual(params['db'], 'tests/db/testdb.sqlite')
        self.assertEqual(params['collection'], 'kvlite_test')

    def test_parse_uri_without_collection(self):
        params = SqliteCollectionManager.parse_uri('sqlite://tests/db/testdb.sqlite')
        self.assertEqual(params['backend'], 'sqlite')
        self.assertEqual(params['db'], 'tests/db/testdb.sqlite')
        self.assertEqual(params['collection'], None)

    def test_manager(self):
        
        URI = 'sqlite://tests/db/testdb.sqlite'
        collection = 'kvlite_test'
        
        manager = SqliteCollectionManager(URI)

        if collection in manager.collections():
            manager.remove(collection)
            
        self.assertNotIn(collection, manager.collections())

        manager.create(collection)
        self.assertIn(collection, manager.collections())

        manager.remove(collection)
        self.assertNotIn(collection, manager.collections())

        manager.close()

    def test_manager_get_collection(self):
        URI = 'sqlite://tests/db/testdb.sqlite'
        collection = 'kvlite_test'

        manager = SqliteCollectionManager(URI)
        self.assertEqual(manager.collection_class.__name__, 'SqliteCollection')

    def test_manager_in_memory(self):

        URI = 'sqlite://memory'
        collection = 'kvlite_test'
        
        manager = SqliteCollectionManager(URI)

        if collection in manager.collections():
            manager.remove(collection)
            
        self.assertNotIn(collection, manager.collections())

        manager.create(collection)
        self.assertIn(collection, manager.collections())

        manager.remove(collection)
        self.assertNotIn(collection, manager.collections())

        manager.close()
    
    def test_incorrect_uri_wrong_collection_in_remove(self):

        URI = 'sqlite://memory'
        collection_name = 'unknown_collection'

        manager = SqliteCollectionManager(URI)
        self.assertRaises(RuntimeError, manager.remove, (collection_name))
        
if __name__ == '__main__':
    unittest.main()        

