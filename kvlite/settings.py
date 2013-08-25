import types

from kvlite.serializers import cPickleSerializer
from kvlite.serializers import CompressedPickleSerializer
from kvlite.serializers import CompressedJsonSerializer

# ITEMS_PER_REQUEST is used in Collection._get_many()
ITEMS_PER_REQUEST = 100

# the length of key 
KEY_LENGTH = 40
    
SUPPORTED_BACKENDS = ['mysql', 'sqlite', ]

SUPPORTED_VALUE_TYPES = {
    types.NoneType: {
        'name': 'none_type',
    },
    types.BooleanType: {
        'name': 'boolean_type',
    },
    types.IntType: {
        'name': 'integer_type',
    },
    types.LongType: {
        'name': 'long_type',
    },
    types.FloatType: {
        'name': 'float_type',
    },
    types.ComplexType: {
        'name': 'complex_type',
    },
    types.StringType: {
        'name': 'string_type',
    },
    types.UnicodeType: {
        'name': 'unicode_type',
    },
    types.TupleType: {
        'name': 'tuple_type',
    },
    types.ListType: {
        'name': 'list_type',
    },
    types.DictType: {
        'name': 'dict_type',
    },
}

# -----------------------------------------------------------------
# SERIALIZERS 
# -----------------------------------------------------------------
''' the name of class or module to serialize msgs with, must have methods or 
functions named ``dumps`` and ``loads``, cPickleSerializer is the default
'''
SERIALIZERS = {
    'pickle': cPickleSerializer,
    'compressed_pickle': CompressedPickleSerializer,
    'compressed_json': CompressedJsonSerializer,
}

