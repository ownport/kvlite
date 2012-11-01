import sys
if '' not in sys.path:
    sys.path.append('')

import kvlite
import unittest

class KvliteUtilsTests(unittest.TestCase):

    def test_get_uuid(self):
        
        uuids = kvlite.get_uuid(1000)
        self.assertEqual(len(set(uuids)), 1000)

    def test_sqlite_open(self):
        
        collection = kvlite.open('sqlite://tests/db/testdb.sqlite:kvlite_test')
        collection.put('a',1)
        self.assertEqual(collection.count,1)
        self.assertEqual(collection.get('a'), ('a',1))
        collection.delete('a')
        self.assertEqual(collection.count,0)
        self.assertEqual(collection.get('a'), (None,None))
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
        
        import types
        
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
                
        print type(none_value) is types.NoneType
        print type(boolean_value) is types.BooleanType
        
if __name__ == '__main__':
    unittest.main()        

