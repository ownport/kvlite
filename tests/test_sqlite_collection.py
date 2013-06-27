import sys
if '' not in sys.path:
    sys.path.append('')

import kvlite 
import unittest
import test_collection_common

class KvliteSqliteTests(test_collection_common.CommonCollectionTests):

    @classmethod
    def setUpClass(self):
        self.URI = 'sqlite://tests/db/testdb.sqlite:{}'

    @classmethod
    def tearDownClass(self):
        
        # delete all temporary tables after tests
        manager = kvlite.managers.CollectionManager(self.URI)
        for collection in manager.collections():
            manager.remove(collection)
        
if __name__ == '__main__':
    unittest.main()        

