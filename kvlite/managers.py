import sqlite3

try:
    import MySQLdb
except ImportError:
    pass

from kvlite.settings import SUPPORTED_BACKENDS

from kvlite.collections import MysqlCollection
from kvlite.collections import SqliteCollection

# -----------------------------------------------------------------
# CollectionManager class
# -----------------------------------------------------------------
class CollectionManager(object):
    ''' Collection Manager
    '''
    
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
        ''' parse_uri 
        '''
        return self.backend_manager.parse_uri(uri)

    def create(self, name):
        ''' create collection 
        '''
        self.backend_manager.create(name)
    
    @property
    def collection_class(self):
        ''' return object MysqlCollection or SqliteCollection 
        '''
        return self.backend_manager.collection_class
    
    @property
    def connection(self):
        ''' return reference to backend connection 
        '''
        return self.backend_manager.connection
    
    def collections(self):
        ''' return list of collections 
        '''
        return self.backend_manager.collections()
    
    def remove(self, name):
        ''' remove collection 
        '''
        self.backend_manager.remove(name)

# -----------------------------------------------------------------
# BaseCollectionManager class
# -----------------------------------------------------------------
class BaseCollectionManager(object):

    def __init__(self, connection):
        ''' init 
        '''
        self._conn = connection
        self._cursor = self._conn.cursor()

    @property
    def connection(self):
        ''' return connection 
        '''
        return self._conn
    
    def _collections(self, sql):
        ''' return collection list
        '''
        self._cursor.execute(sql)
        return [t[0] for t in self._cursor.fetchall()]

    def _create(self, sql_create_table, name):
        ''' create collection by name 
        '''
        self._cursor.execute(sql_create_table % name)
        self._conn.commit()

    def remove(self, name):
        ''' remove collection 
        '''
        if name in self.collections():
            self._cursor.execute('DROP TABLE %s;' % name)
            self._conn.commit()
        else:
            raise RuntimeError('No collection with name: {}'.format(name))

    def close(self):
        ''' close connection to database 
        '''
        try:
            self._conn.close()
        except:
            pass

# -----------------------------------------------------------------
# MysqlCollectionManager class
# -----------------------------------------------------------------
class MysqlCollectionManager(BaseCollectionManager):
    ''' MysqlCollectionManager 
    '''    
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
        ''' create collection 
        '''
        SQL_CREATE_TABLE = '''CREATE TABLE IF NOT EXISTS %s (
                                __rowid__ INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                                k BINARY(20) NOT NULL, 
                                v MEDIUMBLOB,
                                UNIQUE KEY (k) ) ENGINE=InnoDB DEFAULT CHARSET utf8;'''
                                
        self._create(SQL_CREATE_TABLE, name)

    @property
    def collection_class(self):
        ''' return MysqlCollection object
        '''
        return MysqlCollection
    
    def collections(self):
        ''' return collection list
        '''
        return self._collections('SHOW TABLES;')

# -----------------------------------------------------------------
# SqliteCollectionManager class
# -----------------------------------------------------------------
class SqliteCollectionManager(BaseCollectionManager):
    ''' Sqlite Collection Manager 
    '''
    def __init__(self, uri):
        
        params = self.parse_uri(uri) 
        
        self._conn = sqlite3.connect(params['db'])       
        self._conn.text_factory = str

        super(SqliteCollectionManager, self).__init__(self._conn)

    @staticmethod
    def parse_uri(uri):
        ''' parse URI 
        
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
        ''' return SqliteCollection object
        '''
        return SqliteCollection

    def collections(self):
        ''' return collection list
        '''
        return self._collections('SELECT name FROM sqlite_master WHERE type="table";')

    def create(self, name):
        ''' create collection 
        '''
        SQL_CREATE_TABLE = '''CREATE TABLE IF NOT EXISTS %s (
                                k NOT NULL, v, UNIQUE (k) );'''
        self._create(SQL_CREATE_TABLE, name)

