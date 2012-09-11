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
#   TODO autocommit for put()
#   TODO synchronise documents between few datastores
#
#
__author__ = 'Andrey Usov <http://devel.ownport.net>'
__version__ = '0.3'
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
import cmd
import sys
import json
import zlib
import uuid
import pprint
import sqlite3
import binascii

__all__ = ['open', 'remove',]

try:
    import MySQLdb
except ImportError:
    print >> sys.stderr, 'Error! MySQLdb package is not installed, please install python-mysqldb'
    sys.exit()

try:
    import cPickle as pickle
except ImportError:
    import pickle
# TODO add test cases for serializers
# TODO add support user specific serializators

SUPPORTED_BACKENDS = ['mysql', 'sqlite', ]

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
        if isinstance(v, unicode):
            v = str(v)
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
    # TODO save kvlite configuration in database
    
    manager = CollectionManager(uri)
    params = manager.parse_uri(uri)
    if params['collection'] not in manager.collections():
        manager.create(params['collection'])
    return manager.collection_class(manager.connection, params['collection'], serializer)

def remove(uri):
    '''
    remove collection by URI
    ''' 
    backend, rest_uri = uri.split('://')
    if backend in SUPPORTED_BACKENDS:
        if backend == 'mysql':
            MysqlCollection(uri).remove()
        elif backend == 'sqlite':
            SqliteCollection(uri).remove()
        else:
            raise NotImplementedError('unknown backend: {}'.format(uri))
    else:
        raise RuntimeError('Unknown backend: {}'.format(backend))

def get_uuid(amount=100):
    ''' return UUIDs '''
    
    # TODO check another approach for generation UUIDs, more fast
    # TODO get uuids from file as approach to speedup UUIDs generation
    
    uuids = list()
    for _ in xrange(amount):
        u = str(uuid.uuid4()).replace('-', '')
        uuids.append(("%040s" % u).replace(' ','0'))
    return uuids

# -----------------------------------------------------------------
# CollectionManager class
# -----------------------------------------------------------------
class CollectionManager(object):
    ''' Collection Manager'''
    
    def __init__(self, uri):
    
        self.backend_manager = None
        
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
# MysqlCollectionManager class
# -----------------------------------------------------------------
class MysqlCollectionManager(object):
    ''' MysqlCollectionManager '''
    
    def __init__(self, uri):
        
        params = self.parse_uri(uri) 
        
        try:
            self.__conn = MySQLdb.connect(
                                host=params['host'], port = params['port'], 
                                user=params['username'], passwd=params['password'], 
                                db=params['db'])
        except MySQLdb.OperationalError,err:
            raise RuntimeError(err)
        self.__cursor = self.__conn.cursor()

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

        self.__cursor.execute(SQL_CREATE_TABLE % name)
        self.__conn.commit()

    @property
    def connection(self):
        ''' return connection '''
        return self.__conn

    @property
    def collection_class(self):
        ''' return MysqlCollection object'''
        return MysqlCollection
    
    def collections(self):
        ''' return collection list'''
        self.__cursor.execute('SHOW TABLES;')
        return [t[0] for t in self.__cursor.fetchall()]
    

    def remove(self, name):
        ''' remove collection '''
        if name in self.collections():
            self.__cursor.execute('DROP TABLE %s;' % name)
            self.__conn.commit()
        else:
            raise RuntimeError('No collection with name: {}'.format(name))

    def close(self):
        ''' close connection to database '''
        self.__conn.close()

# -----------------------------------------------------------------
# MysqlCollection class
# -----------------------------------------------------------------
class MysqlCollection(object):
    ''' Mysql Connection '''

    def __init__(self, connection, collection_name, serializer=cPickleSerializer):

        self.__conn = connection
        self.__cursor = self.__conn.cursor()
        self.__collection = collection_name
        self.__serializer = serializer

        self.__uuid_cache = list()

    def get_uuid(self):
        """ 
        if mysql connection is available more fast way to use this method 
        than global function - get_uuid()
        
        return id based on uuid """

        if not self.__uuid_cache:
            self.__cursor.execute('SELECT %s;' % ','.join(['uuid()' for _ in range(100)]))
            for uuid in self.__cursor.fetchone():
                u = uuid.split('-')
                u.reverse()
                u = ("%040s" % ''.join(u)).replace(' ','0')
                self.__uuid_cache.append(u)
        return self.__uuid_cache.pop()

    def __get_many(self):
        ''' return all docs '''
        rowid = 0
        while True:
            SQL_SELECT_MANY = 'SELECT __rowid__, k,v FROM %s WHERE __rowid__ > %d LIMIT 1000 ;' % (self.__collection, rowid)
            self.__cursor.execute(SQL_SELECT_MANY)
            result = self.__cursor.fetchall()
            if not result:
                break
            for r in result:
                rowid = r[0]
                k = binascii.b2a_hex(r[1])
                try:
                    v = self.__serializer.loads(r[2])
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
                raise WronKeyValue()
            SQL = 'SELECT k,v FROM %s WHERE k = ' % self.__collection
            try:
                self.__cursor.execute(SQL + "%s", binascii.a2b_hex(k))
            except TypeError, err:
                raise WronKeyValue(err)
            result = self.__cursor.fetchone()
            if result:
                try:
                    v = self.__serializer.loads(result[1])
                except Exception, err:
                    raise RuntimeError('key %s, %s' % (k, err))
                return (binascii.b2a_hex(result[0]), v)
            else:
                return (None, None)
        else:
            return self.__get_many()            

    def put(self, k, v):
        ''' put document in collection '''
        
        # TODO many k/v in put()
        
        if len(k) > 40:
            raise RuntimeError('The length of key is more than 40 bytes')
        SQL_INSERT = 'INSERT INTO %s (k,v) ' % self.__collection
        SQL_INSERT += 'VALUES (%s,%s) ON DUPLICATE KEY UPDATE v=%s;;'
        v = self.__serializer.dumps(v)
        try:
            self.__cursor.execute(SQL_INSERT, (binascii.a2b_hex(k), v, v))
        except TypeError, err:
            raise RuntimeError(err)

    def delete(self, k):
        ''' delete document by k '''
        if len(k) > 40:
            raise WronKeyValue()
        SQL_DELETE = '''DELETE FROM %s WHERE k = ''' % self.__collection
        try:
            self.__cursor.execute(SQL_DELETE + "%s;", binascii.a2b_hex(k))
        except TypeError, err:
            raise WronKeyValue(err)

    def keys(self):
        ''' return document keys in collection'''
        rowid = 0
        while True:
            SQL_SELECT_MANY = 'SELECT __rowid__, k FROM %s WHERE __rowid__ > %d LIMIT 1000 ;' % (self.__collection, rowid)
            self.__cursor.execute(SQL_SELECT_MANY)
            result = self.__cursor.fetchall()
            if not result:
                break
            for r in result:
                rowid = r[0]
                k = binascii.b2a_hex(r[1])
                yield k

    @property
    def count(self):
        ''' return amount of documents in collection'''
        self.__cursor.execute('SELECT count(*) FROM %s;' % self.__collection)
        return int(self.__cursor.fetchone()[0])

    def commit(self):
        self.__conn.commit()

    def close(self):
        ''' close connection to database '''
        self.__conn.close()

# -----------------------------------------------------------------
# SqliteCollectionManager class
# -----------------------------------------------------------------
class SqliteCollectionManager(object):
    ''' Sqlite Collection Manager '''
    def __init__(self, uri):
        
        params = self.parse_uri(uri) 
        
        self.__conn = sqlite3.connect(params['db'])       
        self.__cursor = self.__conn.cursor()

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
    def connection(self):
        ''' return connection '''
        return self.__conn

    @property
    def collection_class(self):
        ''' return SqliteCollection object'''
        return SqliteCollection

    def collections(self):
        ''' return collection list'''

        self.__cursor.execute('SELECT name FROM sqlite_master WHERE type="table";')
        return [t[0] for t in self.__cursor.fetchall()]

    def create(self, name):
        ''' create collection '''

        SQL_CREATE_TABLE = '''CREATE TABLE IF NOT EXISTS %s (
                                k NOT NULL, v, UNIQUE (k) );'''

        self.__cursor.execute(SQL_CREATE_TABLE % name)
        self.__conn.commit()

    def remove(self, name):
        ''' remove collection '''
        if name in self.collections():
            self.__cursor.execute('DROP TABLE %s;' % name)
            self.__conn.commit()
        else:
            raise RuntimeError('No collection with name: {}'.format(name))

    def close(self):
        ''' close connection to database '''
        self.__conn.close()
    
# -----------------------------------------------------------------
# SqliteCollection class
# -----------------------------------------------------------------
class SqliteCollection(object):
    ''' Sqlite Collection'''
    
    def __init__(self, connection, collection_name, serializer=cPickleSerializer):

        self.__conn = connection
        self.__cursor = self.__conn.cursor()
        self.__collection = collection_name
        self.__serializer = serializer

        self.__uuid_cache = list()

    def get_uuid(self):
        """ return id based on uuid """

        if not self.__uuid_cache:
            for uuid in get_uuid():
                self.__uuid_cache.append(uuid)
        return self.__uuid_cache.pop()

    def put(self, k, v):
        ''' put document in collection '''
        
        # TODO many k/v in put()
        
        if len(k) > 40:
            raise RuntimeError('The length of key is more than 40 bytes')
        SQL_INSERT = 'INSERT OR REPLACE INTO %s (k,v) ' % self.__collection
        SQL_INSERT += 'VALUES (?,?)'
        v = self.__serializer.dumps(v)
        try:
            self.__cursor.execute(SQL_INSERT, (k, v))
        except TypeError, err:
            raise RuntimeError(err)

    def __get_many(self):
        ''' return all docs '''
        rowid = 0
        while True:
            SQL_SELECT_MANY = 'SELECT rowid, k,v FROM %s WHERE rowid > %d LIMIT 1000 ;' % (self.__collection, rowid)
            self.__cursor.execute(SQL_SELECT_MANY)
            result = self.__cursor.fetchall()
            if not result:
                break
            for r in result:
                rowid = r[0]
                k = r[1]
                try:
                    v = self.__serializer.loads(r[2])
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
            SQL = 'SELECT k,v FROM %s WHERE k = ?;' % self.__collection
            try:
                self.__cursor.execute(SQL, (k,))
            except TypeError, err:
                raise WronKeyValue(err)
            result = self.__cursor.fetchone()
            if result:
                try:
                    v = self.__serializer.loads(result[1])
                except Exception, err:
                    raise RuntimeError('key %s, %s' % (k, err))
                return (result[0], v)
            else:
                return (None, None)
        else:
            return self.__get_many()            

    def keys(self):
        ''' return document keys in collection'''
        rowid = 0
        while True:
            SQL_SELECT_MANY = 'SELECT rowid, k FROM %s WHERE rowid > %d LIMIT 1000 ;' % (self.__collection, rowid)
            self.__cursor.execute(SQL_SELECT_MANY)
            result = self.__cursor.fetchall()
            if not result:
                break
            for r in result:
                rowid = r[0]
                yield r[1]

    def delete(self, k):
        ''' delete document by k '''
        if len(k) > 40:
            raise RuntimeError('The key length is more than 40 bytes')
        SQL_DELETE = '''DELETE FROM %s WHERE k = ?;''' % self.__collection
        try:
            self.__cursor.execute(SQL_DELETE, (k,))
        except TypeError, err:
            raise WronKeyValue(err)

    @property
    def count(self):
        ''' return amount of documents in collection'''
        self.__cursor.execute('SELECT count(*) FROM %s;' % self.__collection)
        return int(self.__cursor.fetchone()[0])

    def commit(self):
        self.__conn.commit()

    def close(self):
        ''' close connection to database '''
        self.__conn.close()
                    
# -----------------------------------------------------------------
# Console class
# -----------------------------------------------------------------
class Console(cmd.Cmd):
    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = "kvlite> "
        self.ruler = '-'

        self.__history_size = 20
        self.__history = list()
        self.__kvlite_colls = dict()
        self.__current_coll_name = 'kvlite'
        self.__current_coll = None

    def emptyline(self):
        return False
    
    def do_help(self, arg):
        '''   help <command>\tshow <command> help'''
        if arg:
            try:
                func = getattr(self, 'help_' + arg)
            except AttributeError:
                try:
                    doc=getattr(self, 'do_' + arg).__doc__
                    if doc:
                        self.stdout.write("%s\n"%str(doc))
                        return
                except AttributeError:
                    pass
                self.stdout.write("%s\n"%str(self.nohelp % (arg,)))
                return
        else:
            names = [
                '', 'do_help', 'do_version', 'do_licence', 'do_history', 'do_exit', '',
                'do_create', 'do_use', 'do_show', 'do_remove', 'do_import', 'do_export', '',
                'do_hash', 'do_keys', 'do_items', 'do_get', 'do_put', 'do_delete', 'do_count', ''
            ]
            for name in names:
                if not name:
                    print
                else:
                    print getattr(self, name).__doc__

    def do_history(self,line):
        '''   history\t\tshow commands history '''
        for i, line in enumerate(self.__history):
            print "0%d. %s" % (i+1, line) 

    def precmd(self, line):
        if len(self.__history) == self.__history_size:
            prev_line = self.__history.pop(0)
        if line and line not in self.__history:
            self.__history.append(line)
        return line

    def do_version(self, line):
        '''   version\t\tshow kvlite version'''
        print 'version: %s' % __version__

    def do_licence(self, line):
        '''   licence\t\tshow licence'''
        print __license__
        print

    def do_exit(self, line):
        '''   exit\t\t\texit from console '''
        return True

    def do_import(self, filename):
        '''   import <filename>\timport collection configuration from JSON file'''
        import os
        
        if not filename:
            print getattr(self, 'do_import').__doc__
            return
        filename = filename.rstrip().lstrip()
        
        if os.path.isfile(filename):
            for k, v in json_decode(open(filename).read()).items():
                self.__kvlite_colls[k] = v
            print 'Import completed'
        else:
            print 'Error! File %s does not exists' % filename

    def do_export(self, filename):
        '''   export <filename>\texport collection configurations to JSON file'''
        # TODO check if file exists. If yes, import about it
        if not filename:
            print getattr(self, 'do_import').__doc__
            return
        filename = filename.rstrip().lstrip()
        json_file = open(filename, 'w')
        json_file.write(json_encode(self.__kvlite_colls))
        json_file.close()
        print 'Export completed to file: %s' % filename

    def do_show(self, line):
        '''   show collections\tlist of available collections (defined in settings.py)'''
        if line == 'collections':
            for coll in self.__kvlite_colls:
                print '   %s' % coll
        else:
            print 'Unknown argument: %s' % line
    
    def do_use(self, collection_name):
        '''   use <collection>\tuse the collection as the default (current) collection'''
        if collection_name in self.__kvlite_colls:
            self.prompt = '%s>' % collection_name
            self.__current_coll_name = collection_name
            self.__current_coll = Collection(self.__kvlite_colls[self.__current_coll_name])
            return
        else:
            print 'Error! Unknown collection: %s' % collection_name

    def do_create(self, line):
        '''   create <name> <uri>\tcreate new collection (if not exists)'''
        try:
            name, uri = [i for i in line.split(' ') if i <> '']
        except ValueError:
            print getattr(self, 'do_create').__doc__
            return
            
        if name in self.__kvlite_colls:
            print 'Warning! Collection name already defined: %s, %s' % (name, self.__kvlite_colls[name]) 
            print 'If needed please change collection name'
            return
        try:
            if is_collection_exists(uri):
                self.__kvlite_colls[name] = uri
                print 'Connection exists, the reference added to collection list'
                return
            else:
                create_collection(uri)
                self.__kvlite_colls[name] = uri
                print 'Collection created and added to collection list'
                return
        except WrongURIException:
            print 'Error! Incorrect URI'
            return
        except ConnectionError, err:
            print 'Connection Error! Please check URI, %s' % str(err)
            return

    def do_remove(self, name):
        '''   remove <collection>\tremove collection'''
        if name not in self.__kvlite_colls:
            print 'Error! Collection name does not exist: %s' % name
            return
        try:
            if is_collection_exists(self.__kvlite_colls[name]):
                delete_collection(self.__kvlite_colls[name])
                del self.__kvlite_colls[name]
                print 'Collection %s deleted' % name
                return
            else:
                print 'Error! Collection does not exist, %s' % self.__kvlite_colls[name]
        except WrongURIException:
            print 'Error! Incorrect URI'
            return
        except ConnectionError, err:
            print 'Connection Error! Please check URI, %s' % str(err)
            return

    def do_hash(self, line):
        '''   hash [string]\tgenerate sha1 hash, random if string is not defined'''        
        import hashlib
        import datetime
        if not line:
            str_now = str(datetime.datetime.now())
            print 'Random sha1 hash:', hashlib.sha1(str_now).hexdigest()
        else:
            line = line.rstrip().lstrip()
            print 'sha1 hash:', hashlib.sha1(line).hexdigest()
        
    def do_keys(self, line):
        '''   keys\t\t\tlist of keys '''        
        if not self.__current_coll_name in self.__kvlite_colls:
            print 'Error! Unknown collection: %s' % self.__current_coll_name
            return
        for k,v in self.__current_coll.get():
            print k

    def do_items(self, line):
        '''   items\t\tlist of collection's items '''        
        if not self.__current_coll_name in self.__kvlite_colls:
            print 'Error! Unknown collection: %s' % self.__current_coll_name
            return
        for k,v in self.__current_coll.get():
            print k
            pprint.pprint(v)
            print
        
    def do_count(self, args):
        '''   count\t\tshow the amount of entries in collection '''        
        if self.__current_coll:
            print self.__current_coll.count()

    def do_get(self, key):
        '''   get <key>\t\tshow collection entry by key'''    
        if not key:
            print getattr(self, 'do_get').__doc__
            return
        for key in [k for k in key.split(' ') if k <> '']:
            if self.__current_coll:
                k, v = self.__current_coll.get(key)
                print k
                pprint.pprint(v)
                print
            else:
                print 'Error! The collection is not selected, please use collection'
                return
    
    def do_put(self, line):
        '''   put <key> <value>\tstore entry to collection'''
        try:
            k,v = [i for i in line.split(' ',1) if i <> '']
        except ValueError:
            print getattr(self, 'do_put').__doc__
            return

        try:    
            v = json_decode(v)
        except ValueError, err:
            print 'Value decoding error!', err
            return

        if self.__current_coll:
            try:
                self.__current_coll.put(k, v)
                self.__current_coll.commit()
                print 'Done'
                return
            except WronKeyValue, err:
                print 'Error! Incorrect key/value,', err
                return 
        else:
            print 'Error! The collection is not selected, please use collection'
            return


    def do_delete(self, key):
        '''   delete <key>\t\tdelete entry by key '''
        key = key.rstrip().lstrip()
        if self.__current_coll.get(key) <> (None, None):
            self.__current_coll.delete(key)
            self.__current_coll.commit()
            print 'Done'
            return
        else:
            print 'Error! The key %s does not exist' % key
            return        
        
# ----------------------------------
#   main
# ----------------------------------
if __name__ == '__main__':
    console = Console()
    console.cmdloop()


