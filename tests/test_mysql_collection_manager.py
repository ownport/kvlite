import unittest

from kvlite import MysqlCollectionManager

class KvliteMysqlCollectionManagerTests(unittest.TestCase):

    def test_parse_uri_without_port(self):

        params = MysqlCollectionManager.parse_uri('mysql://kvlite_test:eixaaghiequ6ZeiBahn0@localhost/kvlite_test.kvlite_test')
        self.assertEqual(params['backend'], 'mysql')
        self.assertEqual(params['username'], 'kvlite_test')
        self.assertEqual(params['password'], 'eixaaghiequ6ZeiBahn0')
        self.assertEqual(params['host'], 'localhost')
        self.assertEqual(params['port'], 3306)
        self.assertEqual(params['db'], 'kvlite_test')
        self.assertEqual(params['collection'], 'kvlite_test')

    def test_parse_uri_with_port(self):

        params = MysqlCollectionManager.parse_uri('mysql://kvlite_test:eixaaghiequ6ZeiBahn0@localhost:3307/kvlite_test.kvlite_test')
        self.assertEqual(params['backend'], 'mysql')
        self.assertEqual(params['username'], 'kvlite_test')
        self.assertEqual(params['password'], 'eixaaghiequ6ZeiBahn0')
        self.assertEqual(params['host'], 'localhost')
        self.assertEqual(params['port'], 3307)
        self.assertEqual(params['db'], 'kvlite_test')
        self.assertEqual(params['collection'], 'kvlite_test')

    def test_parse_url_no_collection(self):

        params = MysqlCollectionManager.parse_uri('mysql://kvlite_test:eixaaghiequ6ZeiBahn0@localhost:3307/kvlite_test')
        self.assertEqual(params['backend'], 'mysql')
        self.assertEqual(params['username'], 'kvlite_test')
        self.assertEqual(params['password'], 'eixaaghiequ6ZeiBahn0')
        self.assertEqual(params['host'], 'localhost')
        self.assertEqual(params['port'], 3307)
        self.assertEqual(params['db'], 'kvlite_test')
        self.assertEqual(params['collection'], None)

    def test_manager(self):
        
        URI = 'mysql://kvlite_test:eixaaghiequ6ZeiBahn0@localhost/kvlite_test'
        collection = 'kvlite_test'
        
        manager = MysqlCollectionManager(URI)

        if collection in manager.collections():
            manager.remove(collection)
            
        self.assertNotIn(collection, manager.collections())

        manager.create(collection)
        self.assertIn(collection, manager.collections())

        manager.remove(collection)
        self.assertNotIn(collection, manager.collections())

        manager.close()

    def test_manager_get_collection(self):
        URI = 'mysql://kvlite_test:eixaaghiequ6ZeiBahn0@localhost/kvlite_test'
        collection = 'kvlite_test'

        manager = MysqlCollectionManager(URI)
        self.assertEqual(manager.collection_class.__name__, 'MysqlCollection')
        
        
if __name__ == '__main__':
    unittest.main()        

