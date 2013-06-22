import sys
if '' not in sys.path:
    sys.path.append('')

import pprint
import kvlite
import unittest

class KvliteUtilsTests(unittest.TestCase):

    def setUp(self):
        
        self.URI = 'sqlite://tests/db/{}.kvlite:kvlite_test'

    def test_get_uuid(self):
        
        uuids = kvlite.get_uuid(1000)
        self.assertEqual(len(set(uuids)), 1000)

    def test_sqlite_open(self):
        
        _key = kvlite.get_uuid(1)[0]
        collection = kvlite.open('sqlite://tests/db/testdb.sqlite:kvlite_test')
        collection.put(_key,1)
        self.assertEqual(collection.count,1)
        self.assertEqual(collection.get({'_key': _key}), (_key,1))
        collection.delete(_key)
        self.assertEqual(collection.count,0)
        self.assertEqual(collection.get({'_key': _key}), (None,None))
        collection.close()
    
    def test_sqlite_remove(self):
        
        kvlite.remove('sqlite://tests/db/testdb.sqlite:kvlite_test')

    def test_mysql_open(self):
        pass

    def test_mysql_remove(self):
        pass

    def test_dict2plain(self):
        
        # simple 
        source = {
            'string': 'str', 
            'unicode': u'unicode', 
            'integer': 10,
            'double': 10.,
        }
        self.assertEqual(
                kvlite.dict2flat('root', source),
                {
                    'root.string':'str',
                    'root.unicode':u'unicode',
                    'root.integer':10,
                    'root.double': 10.,
                }
        )
        
        # compound
        source = {
            'list': ['a1', 'b2', 'c3'],
            'tuple': ('a1', 'b2', 'c3'),
            'dict1': {'a':1,'b':2,'c':3},
            'dict2': {'a': ['b2', 'c3'], 'b': ('b2', 'c3'), 'c': {'b':2, 'c':3}}
        }
        self.assertEqual(
                kvlite.dict2flat('root', source),
                {
                    'root.list':['a1', 'b2', 'c3'],
                    'root.tuple':('a1', 'b2', 'c3'),
                    'root.dict1.a':1,
                    'root.dict1.b':2,
                    'root.dict1.c':3,
                    'root.dict2.a':['b2','c3'],
                    'root.dict2.b':('b2','c3'),
                    'root.dict2.c.b':2,
                    'root.dict2.c.c':3,
                }
        )
    
    def test_basic_types(self):
        
        none_value = None
        boolean_value = True
        integer_value = 1
        longinteger_value = 1L
        float_value = 0.1
        complex_value = -1+0j
        string_value = 'str'
        unicode_value = u'unicode'
        tuple_value = (1,2,3)
        list_value = [1,2,3]
        dict_value = {'a':1,'b':2,'c':3}
                
        self.assertEqual(kvlite.SUPPORTED_VALUE_TYPES[type(none_value)]['name'], 'none_type')
        self.assertEqual(kvlite.SUPPORTED_VALUE_TYPES[type(boolean_value)]['name'], 'boolean_type')
        self.assertEqual(kvlite.SUPPORTED_VALUE_TYPES[type(integer_value)]['name'], 'integer_type')
        self.assertEqual(kvlite.SUPPORTED_VALUE_TYPES[type(longinteger_value)]['name'], 'long_type')
        self.assertEqual(kvlite.SUPPORTED_VALUE_TYPES[type(float_value)]['name'], 'float_type')
        self.assertEqual(kvlite.SUPPORTED_VALUE_TYPES[type(complex_value)]['name'], 'complex_type')
        self.assertEqual(kvlite.SUPPORTED_VALUE_TYPES[type(string_value)]['name'], 'string_type')
        self.assertEqual(kvlite.SUPPORTED_VALUE_TYPES[type(unicode_value)]['name'], 'unicode_type')
        self.assertEqual(kvlite.SUPPORTED_VALUE_TYPES[type(tuple_value)]['name'], 'tuple_type')
        self.assertEqual(kvlite.SUPPORTED_VALUE_TYPES[type(list_value)]['name'], 'list_type')
        self.assertEqual(kvlite.SUPPORTED_VALUE_TYPES[type(dict_value)]['name'], 'dict_type')

    def test_docs_struct(self):
        
        import json
        documents = [
            ('id1', {
                'title': 'title1', 'pages': 1, 'description': u'Description1',
                'keywords': ['a1', 'b1', 'c1', u'd1', 1] 
            }),
            ('id2', {
                'title': 'title2', 'pages': 2, 'description': u'Description2',
                'keywords': ['a2', 'b2', 'c2', u'd2', 2 ] 
            }),
            ('id3', {
                'title': 'title1', 'pages': 3, 'description': u'Description3',
                'keywords': ['a3', 'b3', 3] 
            }),            
            ('id4', {
                'title': u'title4', 'pages': '4', 'description': u'Description4',
                'keywords': ['a4', 'b4', 'c4',  u'd4'] 
            }),            
        ] 
        result = [
            {
                'name': 'keywords',
                'types': {'list_type': { 'string_type': 11, 'unicode_type': 3, 'integer_type':3 }}
            },
            {
                'name': 'title', 
                'types': { 'string_type': 3, 'unicode_type': 1},
            },
            {
                'name': 'description',
                'types': { 'unicode_type': 4},
            },
            { 
                'name': 'pages',
                'types': { 'integer_type': 3, 'string_type': 1},
            },
        ]
        
        for s in kvlite.docs_struct(documents)['structure']:
            if json.dumps(s) not in [json.dumps(r) for r in result]:
                raise RuntimeError('Incorrect document structure')

    def test_copy(self):
        ''' test_copy
        '''
        
        COPIED_ITEMS = 250
        
        source_uri = self.URI.format(kvlite.tmp_name())
        source = kvlite.open(source_uri, kvlite.cPickleSerializer)

        target_uri = self.URI.format(kvlite.tmp_name())        
        target = kvlite.open(target_uri, kvlite.cPickleSerializer)

        for k in range(COPIED_ITEMS):
            source.put('%04d' % k, 'value: %d' % k)
        source.commit()
            
        kvlite.copy(source, target)
        
        self.assertEqual(target.count, COPIED_ITEMS)
        
        source.close()    
        target.close()
        
if __name__ == '__main__':
    unittest.main()        

