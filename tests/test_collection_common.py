import sys
if '' not in sys.path:
    sys.path.append('')

import kvlite
import unittest

class CommonCollectionTests(unittest.TestCase):

    def setUp(self):
        
        self.URI = 'sqlite://tests/db/{}.kvlite:kvlite_test'

    def test_get_uuid(self):
        
        collection = kvlite.open(self.URI.format(kvlite.utils.tmp_name()))
        uuids = [collection.get_uuid() for i in range(1000)]
        self.assertEqual(len(set(uuids)), 1000)
        collection.close()

    def test_put_get_delete_count_one(self):
        
        collection = kvlite.open(self.URI.format(kvlite.utils.tmp_name()))

        k = collection.get_uuid()
        v = 'test_put_one'
        collection.put(k, v)
        self.assertEqual(collection.get({'_key': k}), (k,v))
        self.assertEqual(collection.count, 1)
        collection.delete(k)
        self.assertEqual(collection.count, 0)
        collection.commit()
        collection.close()

    def test_put_wrong_oldformat_kv(self):
        
        collection = kvlite.open(self.URI.format(kvlite.utils.tmp_name()))
        collection.put(collection.get_uuid(), 'value')
        collection.close()
        
    def test_get_many_by_keys(self):
        
        collection = kvlite.open(self.URI.format(kvlite.utils.tmp_name()))
        kvs = [(collection.get_uuid(), 'test') for _ in range(10)]
        collection.put(kvs)
        collection.commit()
        
        # keys are in database
        result = [kv for kv in collection.get({'_key': [kv[0] for kv in kvs[0:3]]})]
        self.assertEqual(len(kvs[0:3]), len(result))
        for res in result:
            self.assertIn(res, kvs[0:3])
        # keys are not in database
        result = [kv for kv in collection.get({'_key': ['00' for kv in range(3)]})]
        self.assertNotEqual(len(kvs[0:3]), len(result))
        collection.close()

    def test_put_get_delete_count_many(self):
        
        collection = kvlite.open(self.URI.format(kvlite.utils.tmp_name()))
        ks = [(collection.get_uuid(), 'test_{}'.format(i)) for i in xrange(100)]
        collection.put(ks)
        
        self.assertEqual(collection.count, 100)
        for k in ks:
            collection.delete(k[0])
        self.assertEqual(collection.count, 0)
        collection.commit()
        collection.close()

    def test_long_key(self):
        
        collection = kvlite.open(self.URI.format(kvlite.utils.tmp_name()))
        
        self.assertRaises(RuntimeError, collection.get, {'_key':'1'*41})
        self.assertRaises(RuntimeError, collection.put, '1'*41, 'long_key')
        self.assertRaises(RuntimeError, collection.delete, '1'*41)
    
        collection.close()

    def test_diff_key_length(self):
        ''' test for different key length
        '''
        collection = kvlite.open(self.URI.format(kvlite.utils.tmp_name()))
        collection.put(1, 'key-01')
        self.assertEqual(collection.get({'_key': '1'}), ('1'.zfill(kvlite.settings.KEY_LENGTH), 'key-01'))
        self.assertEqual(collection.get({'_key': '01'}), ('1'.zfill(kvlite.settings.KEY_LENGTH), 'key-01'))
        self.assertEqual(collection.get({'_key': '001'}), ('1'.zfill(kvlite.settings.KEY_LENGTH), 'key-01'))
        
        collection.close()

    def test_absent_key(self):
        
        collection = kvlite.open(self.URI.format(kvlite.utils.tmp_name()))
        self.assertEqual(collection.get({'_key':u'a1b2c3'}), (None,None))
        collection.close()

    def test_pagination(self):

        collection = kvlite.open(self.URI.format(kvlite.utils.tmp_name()))
        PAGE_SIZE=10
        kvs = [(collection.get_uuid(), 'test') for _ in range(100)]
        collection.put(kvs)
        # first page
        result = [kv for kv in collection.get(offset=0,limit=PAGE_SIZE)] 
        self.assertEqual(len(result), len(kvs[0:PAGE_SIZE]))
        for res in result:
            self.assertIn(res, kvs[0:PAGE_SIZE])
        # second page
        result = [kv for kv in collection.get(offset=2*PAGE_SIZE,limit=PAGE_SIZE)] 
        self.assertEqual(len(result), len(kvs[2*PAGE_SIZE:2*PAGE_SIZE+PAGE_SIZE]))
        for res in result:
            self.assertIn(res, kvs[2*PAGE_SIZE:2*PAGE_SIZE+PAGE_SIZE])
        collection.close()

    def test_use_different_serializators_for_many(self):

        URI = self.URI.format(kvlite.utils.tmp_name())
        collection = kvlite.open(URI, serializer_name='compressed_json')
        collection.put(u'11', u'diffser1')
        collection.put(u'22', u'diffser2')
        collection.put(u'33', u'diffser3')
        collection.commit()
        collection.close()

        collection = kvlite.open(URI, serializer_name='pickle')
        with self.assertRaises(RuntimeError):
            res = [(k,v) for k,v in collection]

        collection.put(u'11', u'diffser1')
        collection.put(u'22', u'diffser2')
        collection.put(u'33', u'diffser3')
        collection.commit()
        collection.close()

        collection = kvlite.open(URI, serializer_name='compressed_json')        
        with self.assertRaises(RuntimeError):
            res = [(k,v) for k,v in collection]
        collection.close()        

    def test_metadata(self):
        ''' test metadata
        '''
        URI = self.URI.format(kvlite.utils.tmp_name())
        collection = kvlite.open(URI, serializer_name='pickle')
        self.assertEqual(
            collection.meta, 
            {
                'name': 'kvlite_test',
                'kvlite-version': kvlite.__version__,
                'serializer': 'pickle',
            })
        collection.close()
        
        
        
