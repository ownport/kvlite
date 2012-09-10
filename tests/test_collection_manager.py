import unittest

from kvlite import CollectionManager

class KvliteCollectionManagerTests(unittest.TestCase):

    def test_manager(self):
        
        URI = 'mysql://kvlite_test:eixaaghiequ6ZeiBahn0@localhost/kvlite_test'
        collection = 'kvlite_test'
        
        manager = CollectionManager(URI)

        if collection in manager.collections():
            manager.remove(collection)
            
        self.assertNotIn(collection, manager.collections())

        manager.create(collection)
        self.assertIn(collection, manager.collections())

        manager.remove(collection)
        self.assertNotIn(collection, manager.collections())
        
        
if __name__ == '__main__':
    unittest.main()        

