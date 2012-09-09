import unittest

from kvlite import MysqlCollectionManager

class KvliteMysqlManagerTests(unittest.TestCase):

    def test_parse_url(self):

        params = MysqlCollectionManager._parse_uri('mysql://kvlite_test:eixaaghiequ6ZeiBahn0@localhost/kvlite_test.kvlite_test')
        self.assertEqual(params['backend'], 'mysql')
        self.assertEqual(params['username'], 'kvlite_test')
        self.assertEqual(params['password'], 'eixaaghiequ6ZeiBahn0')
        self.assertEqual(params['host'], 'localhost')
        self.assertEqual(params['port'], 3306)
        self.assertEqual(params['db'], 'kvlite_test')
        self.assertEqual(params['collection'], 'kvlite_test')

        params = MysqlCollectionManager._parse_uri('mysql://kvlite_test:eixaaghiequ6ZeiBahn0@localhost:3307/kvlite_test.kvlite_test')
        self.assertEqual(params['backend'], 'mysql')
        self.assertEqual(params['username'], 'kvlite_test')
        self.assertEqual(params['password'], 'eixaaghiequ6ZeiBahn0')
        self.assertEqual(params['host'], 'localhost')
        self.assertEqual(params['port'], 3307)
        self.assertEqual(params['db'], 'kvlite_test')
        self.assertEqual(params['collection'], 'kvlite_test')

    def test_manager(self):
        URI = 'mysql://kvlite_test:eixaaghiequ6ZeiBahn0@localhost/kvlite_test.kvlite_test'
        manager = MysqlCollectionManager(URI)

        if manager.collection in manager.collections():
            manager.remove(manager.collection)
            
        self.assertNotIn(manager.collection, manager.collections())

        manager.create(manager.collection)
        self.assertIn(manager.collection, manager.collections())

        manager.remove(manager.collection)
        self.assertNotIn(manager.collection, manager.collections())

        manager.close()
        
if __name__ == '__main__':
    unittest.main()        

