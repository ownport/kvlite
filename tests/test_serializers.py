import sys
if '' not in sys.path:
    sys.path.append('')

import unittest

class KvliteSerializersTests(unittest.TestCase):

    def test_cpickle_serializer(self):
        
        from kvlite.serializers import cPickleSerializer as cps

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


    def test_cpickle_zip_serializer(self):
        
        from kvlite.serializers import cPickleZipSerializer as cpzs

        v = 'string'
        self.assertEqual(cpzs.loads(cpzs.dumps(v)), v)

        v = u'unicode'
        self.assertEqual(cpzs.loads(cpzs.dumps(v)), v)

        v = (1,2,3)
        self.assertEqual(cpzs.loads(cpzs.dumps(v)), v)

        v = [1,2,3]
        self.assertEqual(cpzs.loads(cpzs.dumps(v)), v)

        v = {'a':1, 'b':2, 'c':3}
        self.assertEqual(cpzs.loads(cpzs.dumps(v)), v)


    def test_compressed_json_serializer(self):
        
        from kvlite.serializers import CompressedJsonSerializer as cjs

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

