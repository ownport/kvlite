import sys
if '' not in sys.path:
    sys.path.append('')

import kvlite


def test_serializer_performance():
    ''' test_serializer_performance
    '''
    value = {
        'library': 'kvlite',
        'version': 'v0.6.2',
        'description': 'kvlite is small open-source library for storing documents in SQL databases.',
        'url': 'https://github.com/ownport/kvlite',
        'keywords': 'key-value python database mysql sqlite wrapper',
    }
    
    orig_size = len(str(value))
    assert orig_size  == 242, 'size of: %d, value: %s' % (orig_size, value)

    cpickle_value = kvlite.serializers.cPickleSerializer.dumps(value)
    cpickle_size = len(cpickle_value)
    assert cpickle_size == 285, 'size of: %d, value: %s' % (cpickle_size, cpickle_value)
    
    cpickle_zip_value = kvlite.serializers.CompressedPickleSerializer.dumps(value)
    cpickle_zip_size = len(cpickle_zip_value)
    assert cpickle_zip_size == 207, 'size of: %d, value: %s' % (cpickle_zip_size, cpickle_zip_value)
    
    compressed_json_value = kvlite.serializers.CompressedJsonSerializer.dumps(value)
    compressed_json_size = len(compressed_json_value)
    assert compressed_json_size == 176, 'size of: %d, value: %s' % (compressed_json_size, compressed_json_value)
        
