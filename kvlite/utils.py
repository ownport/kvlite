import uuid
import kvlite
import random
import string


from kvlite.settings import SERIALIZERS
from kvlite.settings import SUPPORTED_VALUE_TYPES

from kvlite.managers import CollectionManager
from kvlite.collections import MysqlCollection
from kvlite.collections import SqliteCollection

# -----------------------------------------------------------------
# KVLite utils
# -----------------------------------------------------------------
def open(uri, serializer_name='pickle'):
    ''' open collection by URI, 
    
    if collection does not exist kvlite will try to create it
        
    serializer_name: see details in SERIALIZERS section

    returns MysqlCollection or SqliteCollection object in case of successful 
    opening or creation new collection    
    '''
    # TODO use `None` for serializer to store messages in plain text, suitable for strings, integers, etc

    manager = CollectionManager(uri)
    params = manager.parse_uri(uri)
    if params['collection'] not in manager.collections():
        manager.create(params['collection'])
        
    collection = manager.collection_class(manager.connection, 
                                        params['collection'], 
                                        serializer_name)
    return collection

def remove(uri):
    ''' remove collection by URI
    ''' 
    manager = CollectionManager(uri)
    params = manager.parse_uri(uri)
    if params['collection'] in manager.collections():
        manager.remove(params['collection'])

def copy(source, target):
    ''' copy data from source to target
    
    where
        source = Collection object to source
        target = Collection object to target
    '''
    if not isinstance(source, (MysqlCollection, SqliteCollection)):
        raise RuntimeError('The source should be MysqlCollection or SqliteCollection object, not %s', type(source))
    if not isinstance(target, (MysqlCollection, SqliteCollection)):
        raise RuntimeError('The source should be MysqlCollection or SqliteCollection object, not %s', type(target))
    
    data = [kv for kv in source]
    target.put(data)
    target.commit()

def get_uuid(amount=100):
    ''' return UUIDs 
    '''
    
    uuids = list()
    for _ in xrange(amount):
        u = str(uuid.uuid4()).replace('-', '')
        uuids.append(("%040s" % u).replace(' ','0'))
    return uuids

def dict2flat(root_name, source, removeEmptyFields=False):
    ''' returns a simplified "flat" form of the complex hierarchical dictionary 
    '''
    
    def is_simple_elements(source):
        ''' check if the source contains simple element types,
        not lists, tuples, dicts
        '''
        for i in source:
            if isinstance(i, (list, tuple, dict)):
                return False
        return True
    
    flat_dict = {}
    if isinstance(source, (list, tuple)):
        if not is_simple_elements(source):
            for i,e in enumerate(source):
                new_root_name = "%s[%d]" % (root_name,i)
                for k,v in dict2flat(new_root_name,e).items():
                    flat_dict[k] = v
        else:
            flat_dict[root_name] = source
    elif isinstance(source, dict):
        for k,v in source.items():
            if root_name:
                new_root_name = "%s.%s" % (root_name, k)
            else:
                new_root_name = "%s" % k
            for kk, vv in dict2flat(new_root_name,v).items():
                flat_dict[kk] = vv
    else:
        if source is not None:
            flat_dict[root_name] = source
    return flat_dict

def docs_struct(documents):
    ''' returns structure for all documents in the list 
    '''
    
    def seq_struct(items):
        struct = dict()
        for item in items:
            item_type = SUPPORTED_VALUE_TYPES[type(item)]['name']
            
            if item_type in struct:
                struct[item_type] += 1
            else:
                struct[item_type] = 1
        return struct
    
    def doc_struct(document):
        struct = list()
        for name, value in dict2flat('', document).items():
            field = dict()
            field['name'] = name
            field_type = SUPPORTED_VALUE_TYPES[type(value)]['name']
            field['types'] = { field_type: 1 }
            
            if field_type == 'list_type':
                field['types'][field_type] = seq_struct(value)
            if field_type == 'tuple_type':
                field['types'][field_type] = seq_struct(value)
            struct.append(field)
        return struct
    
    struct = list()
    total_documents = 0
    for k,document in documents:
        total_documents += 1

        for s in doc_struct(document):
            names = [f['name'] for f in struct]
            if s['name'] in names:
                idx = names.index(s['name'])
                for t in s['types']:
                    if t in struct[idx]['types']:
                        if t == 'list_type':
                            list_types = set(s['types'][t]) | set(struct[idx]['types'][t])
                            for n in list_types:
                                struct[idx]['types'][t][n] = struct[idx]['types'][t].get(n, 0) + s['types'][t].get(n,0)
                        else:
                            struct[idx]['types'][t] += s['types'][t]
                    else:
                        struct[idx]['types'][t] = s['types'][t]
            else:
                struct.append(s)
    return { 
        'total_documents': total_documents,
        'structure': struct,
    }

def tmp_name(size = 10):
    ''' generate temporary collection name 
    '''
    name = ''.join(random.choice(string.ascii_lowercase) for x in range(int(size * .8)))
    name += ''.join(random.choice(string.digits) for x in range(int(size * .2))) 
    return name
 
