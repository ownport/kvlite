import unittest

from kvlite import cPickleSerializer as cps
from kvlite import CompressedJsonSerializer as cjs

class KvliteSerializersTests(unittest.TestCase):

    def test_cpickle_serializer(self):
        
        v = 'string'
        self.assertEqual(cps.loads(cps.dumps(v)), v)

        v = u'unicode'
        self.assertEqual(cps.loads(cps.dumps(v)), v)

        v = (1,2,3)
        self.assertEqual(cps.loads(cps.dumps(v)), v)

        v = [1,2,3]
        self.assertEqual(cps.loads(cps.dumps(v)), v)

        v = {'a':1, 'b':2, 'c':3}
        self.assertEqual(cps.loads(cps.dumps(v)), v)


    def test_compressed_json_serializer(self):
        
        v = 'string'
        self.assertEqual(cjs.loads(cjs.dumps(v)), v)

        v = u'unicode'
        self.assertEqual(cjs.loads(cjs.dumps(v)), v)

        v = (1,2,3)
        self.assertEqual(cjs.loads(cjs.dumps(v)), list(v))

        v = [1,2,3]
        self.assertEqual(cjs.loads(cjs.dumps(v)), v)

        v = {'a':1, 'b':2, 'c':3}
        self.assertEqual(cjs.loads(cjs.dumps(v)), v)

        
if __name__ == '__main__':
    unittest.main()        

