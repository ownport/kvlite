#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#   Simple key-value datastore

#   - support only mysql database
#   - console support added
#
#   some ideas taked from PyMongo interface http://api.mongodb.org/python/current/index.html
#   kvlite2 tutorial http://code.google.com/p/kvlite/wiki/kvlite2
#
__author__ = 'Andrey Usov <https://github.com/ownport/kvlite>'
__version__ = '0.4.5'
__license__ = """
Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice,
  this list of conditions and the following disclaimer.
* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS 'AS IS'
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE."""

import os
import sys
import json
import zlib
import uuid
import types
import sqlite3
import binascii
import cPickle as pickle

__all__ = ['open', 'remove',]

try:
    import MySQLdb
except ImportError:
    pass

# ITEMS_PER_REQUEST is used in Collection._get_many()
ITEMS_PER_REQUEST = 1000
    
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

'''
A collection is a group of documents stored in kvlite2, 
and can be thought of as roughly the equivalent of a 
table in a relational database.

For using JSON as serialization

>>> import json
>>> collection = open('sqlite://test.sqlite:test', serializer=json)
>>>

'''
# -----------------------------------------------------------------
# cPickleSerializer class
# -----------------------------------------------------------------

class cPickleSerializer(object):
    ''' cPickleSerializer '''

    @staticmethod
    def dumps(v):
        ''' dumps value '''
        if isinstance(v, unicode):
            v = str(v)
        return pickle.dumps(v)

    @staticmethod
    def loads(v):
        ''' loads value  '''
        return pickle.loads(v)

# -----------------------------------------------------------------
# CompressedJsonSerializer class
# -----------------------------------------------------------------

class CompressedJsonSerializer(object):
    ''' CompressedJsonSerializer '''

    @staticmethod
    def dumps(v):
        ''' dumps value '''
        return zlib.compress(json.dumps(v))

    @staticmethod
    def loads(v):
        ''' loads value  '''
        return json.loads(zlib.decompress(v))

# -----------------------------------------------------------------
# SERIALIZERS 
# -----------------------------------------------------------------

SERIALIZERS = {
    'pickle': cPickleSerializer,
    'completed_json': CompressedJsonSerializer,
}


# -----------------------------------------------------------------
# KVLite utils
# -----------------------------------------------------------------
def open(uri, serializer=cPickleSerializer):
    ''' 
    open collection by URI, 
    if collection does not exist kvlite will try to create it
    
    in case of successful opening or creation new collection 
    return Collection object
    
    serializer: the class or module to serialize msgs with, must have
    methods or functions named ``dumps`` and ``loads``,
    `pickle <http://docs.python.org/library/pickle.html>`_ is the default,
    use ``None`` to store messages in plain text (suitable for strings,
    integers, etc)
    '''
    
    manager = CollectionManager(uri)
    params = manager.parse_uri(uri)
    if params['collection'] not in manager.collections():
        manager.create(params['collection'])
    return manager.collection_class(manager.connection, params['collection'], serializer)

def remove(uri):
    '''
    remove collection by URI
    ''' 
    manager = CollectionManager(uri)
    params = manager.parse_uri(uri)
    if params['collection'] in manager.collections():
        manager.remove(params['collection'])

def get_uuid(amount=100):
    ''' return UUIDs '''
    
    uuids = list()
    for _ in xrange(amount):
        u = str(uuid.uuid4()).replace('-', '')
        uuids.append(("%040s" % u).replace(' ','0'))
    return uuids

def dict2flat(root_name, source, removeEmptyFields=False):
    ''' returns a simplified "flat" form of the complex hierarchical dictionary '''
    
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
    ''' returns structure for all documents in the list '''
    
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

# -----------------------------------------------------------------
# CollectionManager class
# -----------------------------------------------------------------
class CollectionManager(object):
    ''' Collection Manager'''
    
    def __init__(self, uri):
    
        self.backend_manager = None
        
        if not uri or uri.find('://') <= 0:
            raise RuntimeError('Incorrect URI definition: {}'.format(uri))
        backend, rest_uri = uri.split('://')
        if backend in SUPPORTED_BACKENDS:
            if backend == 'mysql':
                self.backend_manager = MysqlCollectionManager(uri)
            elif backend == 'sqlite':
                self.backend_manager = SqliteCollectionManager(uri)
        else:
            raise RuntimeError('Unknown backend: {}'.format(backend))

    def parse_uri(self, uri):
        ''' parse_uri '''
        return self.backend_manager.parse_uri(uri)

    def create(self, name):
        ''' create collection '''
        self.backend_manager.create(name)
    
    @property
    def collection_class(self):
        ''' return object MysqlCollection or SqliteCollection '''
        return self.backend_manager.collection_class
    
    @property
    def connection(self):
        ''' return reference to backend connection '''
        return self.backend_manager.connection
    
    def collections(self):
        ''' return list of collections '''
        return self.backend_manager.collections()
    
    def remove(self, name):
        ''' remove collection '''
        self.backend_manager.remove(name)

# -----------------------------------------------------------------
# BaseCollectionManager class
# -----------------------------------------------------------------
class BaseCollectionManager(object):

    def __init__(self, connection):
        ''' init '''
        self._conn = connection
        self._cursor = self._conn.cursor()

    @property
    def connection(self):
        ''' return connection '''
        return self._conn
    
    def _collections(self, sql):
        ''' return collection list'''
        self._cursor.execute(sql)
        return [t[0] for t in self._cursor.fetchall()]

    def _create(self, sql_create_table, name):
        ''' create collection by name '''
        self._cursor.execute(sql_create_table % name)
        self._conn.commit()

    def remove(self, name):
        ''' remove collection '''
        if name in self.collections():
            self._cursor.execute('DROP TABLE %s;' % name)
            self._conn.commit()
        else:
            raise RuntimeError('No collection with name: {}'.format(name))

    def close(self):
        ''' close connection to database '''
        self._conn.close()

# -----------------------------------------------------------------
# MysqlCollectionManager class
# -----------------------------------------------------------------
class MysqlCollectionManager(BaseCollectionManager):
    ''' MysqlCollectionManager '''
    
    def __init__(self, uri):
        
        params = self.parse_uri(uri) 
        
        try:
            self._conn = MySQLdb.connect(
                                host=params['host'], port = params['port'], 
                                user=params['username'], passwd=params['password'], 
                                db=params['db'])
        except MySQLdb.OperationalError,err:
            raise RuntimeError(err)
        
        super(MysqlCollectionManager, self).__init__(self._conn)

    @staticmethod
    def parse_uri(uri):
        '''parse URI 
        
        return driver, user, password, host, port, database, table
        '''
        parsed_uri = dict()
        parsed_uri['backend'], rest_uri = uri.split('://', 1)
        parsed_uri['username'], rest_uri = rest_uri.split(':', 1)
        parsed_uri['password'], rest_uri = rest_uri.split('@', 1)
        
        if ':' in rest_uri:
            parsed_uri['host'], rest_uri = rest_uri.split(':', 1)
            parsed_uri['port'], rest_uri = rest_uri.split('/', 1)
            parsed_uri['port'] = int(parsed_uri['port'])
        else:
            parsed_uri['host'], rest_uri = rest_uri.split('/')
            parsed_uri['port'] = 3306

        if '.' in rest_uri:
            parsed_uri['db'], parsed_uri['collection'] = rest_uri.split('.', 1)     
        else:
            parsed_uri['db'] = rest_uri
            parsed_uri['collection'] = None
        return parsed_uri
        
    def create(self, name):
        ''' create collection '''

        SQL_CREATE_TABLE = '''CREATE TABLE IF NOT EXISTS %s (
                                __rowid__ INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                                k BINARY(20) NOT NULL, 
                                v MEDIUMBLOB,
                                UNIQUE KEY (k) ) ENGINE=InnoDB;'''
                                
        self._create(SQL_CREATE_TABLE, name)

    @property
    def collection_class(self):
        ''' return MysqlCollection object'''
        return MysqlCollection
    
    def collections(self):
        ''' return collection list'''
        return self._collections('SHOW TABLES;')

# -----------------------------------------------------------------
# SqliteCollectionManager class
# -----------------------------------------------------------------
class SqliteCollectionManager(BaseCollectionManager):
    ''' Sqlite Collection Manager '''
    def __init__(self, uri):
        
        params = self.parse_uri(uri) 
        
        self._conn = sqlite3.connect(params['db'])       
        self._conn.text_factory = str

        super(SqliteCollectionManager, self).__init__(self._conn)

    @staticmethod
    def parse_uri(uri):
        '''parse URI 
        
        return driver, database, collection
        '''
        parsed_uri = dict()
        parsed_uri['backend'], rest_uri = uri.split('://', 1)
        if ':' in rest_uri:
            parsed_uri['db'], parsed_uri['collection'] = rest_uri.split(':',1)
        else:
            parsed_uri['db'] = rest_uri
            parsed_uri['collection'] = None
        if parsed_uri['db'] == 'memory':
            parsed_uri['db'] = ':memory:'
        return parsed_uri

    @property
    def collection_class(self):
        ''' return SqliteCollection object'''
        return SqliteCollection

    def collections(self):
        ''' return collection list'''

        return self._collections('SELECT name FROM sqlite_master WHERE type="table";')

    def create(self, name):
        ''' create collection '''

        SQL_CREATE_TABLE = '''CREATE TABLE IF NOT EXISTS %s (
                                k NOT NULL, v, UNIQUE (k) );'''
        self._create(SQL_CREATE_TABLE, name)


# -----------------------------------------------------------------
# BaseCollection class
# -----------------------------------------------------------------
class BaseCollection(object):

    def __init__(self, connection, collection_name, serializer=cPickleSerializer):

        self._conn = connection
        self._cursor = self._conn.cursor()
        self._collection = collection_name
        self._serializer = serializer

        self._uuid_cache = list()

    @property
    def count(self):
        ''' return amount of documents in collection'''
        self._cursor.execute('SELECT count(*) FROM %s;' % self._collection)
        return int(self._cursor.fetchone()[0])

    def commit(self):
        self._conn.commit()

    def close(self):
        ''' close connection to database '''
        self._conn.close()
    
# -----------------------------------------------------------------
# MysqlCollection class
# -----------------------------------------------------------------
class MysqlCollection(BaseCollection):
    ''' Mysql Connection '''

    def get_uuid(self):
        """ 
        if mysql connection is available more fast way to use this method 
        than global function - get_uuid()
        
        return id based on uuid """

        if not self._uuid_cache:
            self._cursor.execute('SELECT %s;' % ','.join(['uuid()' for _ in range(100)]))
            for uuid in self._cursor.fetchone():
                u = uuid.split('-')
                u.reverse()
                u = ("%040s" % ''.join(u)).replace(' ','0')
                self._uuid_cache.append(u)
        return self._uuid_cache.pop()

    def _get_many(self):
        ''' return all docs '''
        rowid = 0
        while True:
            SQL_SELECT_MANY = 'SELECT __rowid__, k,v FROM %s WHERE __rowid__ > %d LIMIT %s;'
            SQL_SELECT_MANY %=  (self._collection, rowid, ITEMS_PER_REQUEST)
            self._cursor.execute(SQL_SELECT_MANY)
            result = self._cursor.fetchall()
            if not result:
                break
            for r in result:
                rowid = r[0]
                k = binascii.b2a_hex(r[1])
                try:
                    v = self._serializer.loads(r[2])
                except Exception, err:
                    raise RuntimeError('key %s, %s' % (k, err))
                yield (k, v)

    def get(self, k=None):
        ''' 
        return document by key from collection 
        return documents if key is not defined
        '''
        if k:
            if len(k) > 40:
                raise RuntimeError('The key length is more than 40 bytes')
            SQL = 'SELECT k,v FROM %s WHERE k = ' % self._collection
            try:
                self._cursor.execute(SQL + "%s", binascii.a2b_hex(k))
            except Exception, err:
                raise RuntimeError(err)
            result = self._cursor.fetchone()
            if result:
                v = self._serializer.loads(result[1])
                return (binascii.b2a_hex(result[0]), v)
            else:
                return (None, None)
        else:
            return self._get_many()            

    def put(self, k, v):
        ''' put document in collection '''
        
        if len(k) > 40:
            raise RuntimeError('The length of key is more than 40 bytes')
        SQL_INSERT = 'INSERT INTO %s (k,v) ' % self._collection
        SQL_INSERT += 'VALUES (%s,%s) ON DUPLICATE KEY UPDATE v=%s;;'
        v = self._serializer.dumps(v)
        self._cursor.execute(SQL_INSERT, (binascii.a2b_hex(k), v, v))

    def delete(self, k):
        ''' delete document by k '''
        if len(k) > 40:
            raise RuntimeError('The length of key is more than 40 bytes')

        SQL_DELETE = '''DELETE FROM %s WHERE k = ''' % self._collection
        self._cursor.execute(SQL_DELETE + "%s;", binascii.a2b_hex(k))

    def keys(self):
        ''' return document keys in collection'''
        rowid = 0
        while True:
            SQL_SELECT_MANY = 'SELECT __rowid__, k FROM %s WHERE __rowid__ > %d LIMIT %d ;'
            SQL_SELECT_MANY %= (self._collection, rowid, ITEMS_PER_REQUEST)
            self._cursor.execute(SQL_SELECT_MANY)
            result = self._cursor.fetchall()
            if not result:
                break
            for r in result:
                rowid = r[0]
                k = binascii.b2a_hex(r[1])
                yield k

# -----------------------------------------------------------------
# SqliteCollection class
# -----------------------------------------------------------------
class SqliteCollection(BaseCollection):
    ''' Sqlite Collection'''
    
    def get_uuid(self):
        """ return id based on uuid """

        if not self._uuid_cache:
            for uuid in get_uuid():
                self._uuid_cache.append(uuid)
        return self._uuid_cache.pop()

    def put(self, k, v):
        ''' put document in collection '''
        
        if len(k) > 40:
            raise RuntimeError('The length of key is more than 40 bytes')
        SQL_INSERT = 'INSERT OR REPLACE INTO %s (k,v) ' % self._collection
        SQL_INSERT += 'VALUES (?,?)'
        v = self._serializer.dumps(v)
        self._cursor.execute(SQL_INSERT, (k, v))

    def _get_many(self):
        ''' return all docs '''
        rowid = 0
        while True:
            SQL_SELECT_MANY = 'SELECT rowid, k,v FROM %s WHERE rowid > %d LIMIT %d ;'
            SQL_SELECT_MANY %= (self._collection, rowid, ITEMS_PER_REQUEST)
            self._cursor.execute(SQL_SELECT_MANY)
            result = self._cursor.fetchall()
            if not result:
                break
            for r in result:
                rowid = r[0]
                k = r[1]
                try:
                    v = self._serializer.loads(r[2])
                except Exception, err:
                    raise RuntimeError('key %s, %s' % (k, err))
                yield (k, v)

    def get(self, k=None):
        ''' 
        return document by key from collection 
        return documents if key is not defined
        '''
        if k:
            if len(k) > 40:
                raise RuntimeError('The key length is more than 40 bytes')
            SQL = 'SELECT k,v FROM %s WHERE k = ?;' % self._collection
            try:
                self._cursor.execute(SQL, (k,))
            except Exception, err:
                raise RuntimeError(err)
            result = self._cursor.fetchone()
            if result:
                try:
                    v = self._serializer.loads(result[1])
                except Exception, err:
                    raise RuntimeError('key %s, %s' % (k, err))
                return (result[0], v)
            else:
                return (None, None)
        else:
            return self._get_many()            

    def keys(self):
        ''' return document keys in collection'''
        rowid = 0
        while True:
            SQL_SELECT_MANY = 'SELECT rowid, k FROM %s WHERE rowid > %d LIMIT %d ;'
            SQL_SELECT_MANY %= (self._collection, rowid, ITEMS_PER_REQUEST)
            self._cursor.execute(SQL_SELECT_MANY)
            result = self._cursor.fetchall()
            if not result:
                break
            for r in result:
                rowid = r[0]
                yield r[1]

    def delete(self, k):
        ''' delete document by k '''
        if len(k) > 40:
            raise RuntimeError('The key length is more than 40 bytes')
        SQL_DELETE = '''DELETE FROM %s WHERE k = ?;''' % self._collection
        self._cursor.execute(SQL_DELETE, (k,))
                    
    def find(self, criteria=None, offset=0, limit=ITEMS_PER_REQUEST):
        ''' return the result of search by criteria.
        if the criteria is not defined the find() returns all documents.
        The combination `offset` and `limit` paramters can be used for 
        pagination'''
        
        pass
        
