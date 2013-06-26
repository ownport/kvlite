import kvlite

from kvlite.settings import KEY_LENGTH
from kvlite.settings import ITEMS_PER_REQUEST

from kvlite.serializers import cPickleSerializer
from kvlite.serializers import CompressedJsonSerializer

# -----------------------------------------------------------------
# BaseCollection class
# -----------------------------------------------------------------
class BaseCollection(object):
    ''' BaseCollection
    '''
    def __init__(self, connection, collection_name, serializer=cPickleSerializer):
        ''' __init__
        '''
        self._conn = connection
        self._cursor = self._conn.cursor()
        self._collection = collection_name
        self._serializer = serializer

        self._uuid_cache = list()
        self._ZEROS_KEY = self.prepare_key(0)

    @staticmethod
    def prepare_key(key):
        ''' prepare key
        
        - convert key to string if it's integer
        - zero fill key
        '''
        _key = key
        if isinstance(_key, int):
            _key = str(key)
        if len(_key) > KEY_LENGTH:
            raise RuntimeError('The length of key is more than %d bytes' % (KEY_LENGTH))
        return _key.zfill(KEY_LENGTH)
    
    def prepare_kv(self, k, v, backend='sqlite'):
        ''' prepare key/value pair before insert to database
        
        backend can be 'mysql' or 'sqlite'
        '''
        
        k = self.prepare_key(k)
        if k == self._ZEROS_KEY:
            v = cPickleSerializer.dumps(v)
        else:
            v = self._serializer.dumps(v)
        
        if backend == 'sqlite':
            return (k,v) 
        elif backend == 'mysql':
            return (binascii.a2b_hex(k), v, v)
        else:
            raise RuntimeError('Uknown backend: %s' % backend)
                
    @property
    def meta(self):
        ''' return meta information from zero's key
        '''
        return self.get({'_key': self._ZEROS_KEY})[1]

    @meta.setter
    def meta(self, info):
        ''' set metadata to zero'skey
        '''
        if not isinstance(info, dict):
            raise RuntimeError('Metadata should be dictionary')
        self.put(self._ZEROS_KEY, info)

    @property
    def count(self):
        ''' return amount of documents in collection
        '''
        SQL = 'SELECT count(*) FROM %s' % self._collection
        self._cursor.execute(SQL + ' WHERE k <> ?;', (self._ZEROS_KEY,))
        return int(self._cursor.fetchone()[0])

    def get(self, criteria=None, offset=None, limit=ITEMS_PER_REQUEST):
        ''' returns documents selected from collection by criteria.
        
        - If the criteria is not defined, get() returns all documents.
        - Hint: the combination `offset` and `limit` paramters can be 
        used for pagination
        
        offset  - starts with this position in database
        limit   - how many document will be returned
        '''
        if criteria is None:
            if offset >=0 and limit > 0:
                return self._get_paged(offset=offset, limit=limit)
            else:
                return self._get_all()
            
        if not isinstance(criteria, dict):
            raise RuntimeError('Incorrect criteria format')
        
        if '_key' in criteria:
            if isinstance(criteria['_key'], (str, unicode)):
                return self._get_one(self.prepare_key(criteria['_key']))
            elif isinstance(criteria['_key'], (list, tuple)):
                criteria['_key'] = map(self.prepare_key, criteria['_key'])
                return self._get_many(*criteria['_key'])

    def commit(self):
        ''' commit
        '''
        self._conn.commit()

    def close(self):
        ''' close connection to database 
        '''
        try:
            self._conn.close()
        except:
            pass
    
# -----------------------------------------------------------------
# MysqlCollection class
# -----------------------------------------------------------------
class MysqlCollection(BaseCollection):
    ''' Mysql Connection 
    '''
    def get_uuid(self, amount=100):
        ''' 
        return one uuid. 
        
        By `amount` argument you can define how many UUIDs will be generated and 
        stored in cache if it's empty. By default 100 UUIDs will be generated.
        
        For mysql connection, the generation of UUIDs is more fast than kvlite.get_uuid()
        '''

        if not self._uuid_cache:
            self._cursor.execute('SELECT %s;' % ','.join(['uuid()' for _ in range(int(amount))]))
            for uuid in self._cursor.fetchone():
                u = uuid.split('-')
                u.reverse()
                u = ("%040s" % ''.join(u)).replace(' ','0')
                self._uuid_cache.append(u)
        return self._uuid_cache.pop()

    def _get_one(self, _key):
        ''' return document by _key 
        '''        
        _key = self.prepare_key(_key)
        SQL = 'SELECT k,v FROM %s WHERE k = ' % self._collection
        try:
            self._cursor.execute(SQL + "%s", binascii.a2b_hex(_key))
        except Exception, err:
            raise RuntimeError(err)
        result = self._cursor.fetchone()
        if result:
            try:
                v = self._serializer.loads(result[1])
            except Exception, err:
                raise RuntimeError('key %s, %s' % (_key, err))
            return (binascii.b2a_hex(result[0]), v)
        else:
            return (None, None)

    def _get_many(self, *_keys):
        ''' return docs by keys 
        '''        
        if _keys:
            if isinstance(_keys, (list, tuple)):
                bin_keys = [binascii.a2b_hex(k) for k in _keys if k <> self._ZEROS_KEY]
                SQL_SELECT_MANY = 'SELECT k,v FROM {} WHERE k IN ({})'
                SQL_SELECT_MANY = SQL_SELECT_MANY.format(self._collection,','.join(['%s']*len(bin_keys)));
                self._cursor.execute(SQL_SELECT_MANY, tuple(bin_keys))
                result = self._cursor.fetchall()
                if not result:
                    return
                for r in result:
                    k = binascii.b2a_hex(r[0])
                    try:
                        v = self._serializer.loads(r[1])
                    except Exception, err:
                        raise RuntimeError('key %s, %s' % (k, err))
                    yield (k, v)

    def _get_all(self):
        ''' return all docs 
        '''
        rowid = 0
        while True:
            SQL_SELECT_ALL = 'SELECT __rowid__, k,v FROM %s WHERE __rowid__ > %d LIMIT %s;'
            SQL_SELECT_ALL %=  (self._collection, rowid, ITEMS_PER_REQUEST)
            self._cursor.execute(SQL_SELECT_ALL)
            result = self._cursor.fetchall()
            if not result:
                break
            for r in result:
                rowid = r[0]
                k = binascii.b2a_hex(r[1])
                if k == self._ZEROS_KEY:
                    continue
                try:
                    v = self._serializer.loads(r[2])
                except Exception, err:
                    raise RuntimeError('key %s, %s' % (k, err))
                yield (k, v)
                
    __iter__ = _get_all

    def _get_paged(self, offset=None, limit=ITEMS_PER_REQUEST):
        ''' return docs by offset and limit
        
        offset and limit are used for pagination, for details 
        see BaseCollection.get()
        '''
        
        if not offset and not limit:
            return
        
        SQL_SELECT_MANY = 'SELECT k,v FROM %s WHERE k <> ? LIMIT %d, %d ;'
        SQL_SELECT_MANY %= (self._collection, int(offset), int(limit))
        self._cursor.execute(SQL_SELECT_MANY, (self._ZEROS_KEY, ))
        result = self._cursor.fetchall()
        if not result:
            return
        for r in result:
            k = binascii.b2a_hex(r[0])
            if k == self._ZEROS_KEY:
                continue
            try:
                v = self._serializer.loads(r[1])
            except Exception, err:
                raise RuntimeError('key %s, %s' % (k, err))
            yield (k, v)


    def put(self, k, v):
        ''' put document in collection 
        '''        
        kv_insert = list()
        if not isinstance(kv, (list,tuple)):
            raise RuntimeError('key/value should be packed in the list or tuple')
        
        # put([(k1,v1), (k2,v2)])
        if len(kv) == 1 \
            and isinstance(kv[0], (list, tuple)):
            
            kv_insert = [self.prepare_kv(*kvs, backend='mysql') for kvs in kv[0]]

        # put(k,v)
        elif len(kv) == 2 \
            and not isinstance(kv[0], (list, tuple)) \
            and not isinstance(kv[1], (list, tuple)):
            
            kv_insert.append(self.prepare_kv(*kv, backend='mysql'))

        else:
            raise RuntimeError('Incorrect format of key/values, %s' % kv)

        k = self.prepare_key(k)
        SQL_INSERT = 'INSERT INTO %s (k,v) ' % self._collection
        SQL_INSERT += 'VALUES (%s,%s) ON DUPLICATE KEY UPDATE v=%s;;'

        self._cursor.execute(SQL_INSERT, kv_insert)

    def delete(self, k):
        ''' delete document by k 
        '''
        _key = self.prepare_key(k)
        if _key == self._ZEROS_KEY:
            raise RuntimeError('Metadata cannot be deleted')
        SQL_DELETE = '''DELETE FROM %s WHERE k = ''' % self._collection
        self._cursor.execute(SQL_DELETE + "%s;", binascii.a2b_hex(_key))

# -----------------------------------------------------------------
# SqliteCollection class
# -----------------------------------------------------------------
class SqliteCollection(BaseCollection):
    ''' Sqlite Collection
    '''    
    def get_uuid(self):
        ''' return id based on uuid 
        '''
        if not self._uuid_cache:
            for uuid in kvlite.utils.get_uuid():
                self._uuid_cache.append(uuid)
        return self._uuid_cache.pop()

    def put(self, *kv):
        ''' put document(s) in collection 
        
        kv is list of key/value
        
        put(k,v) or put([(k1,v1), (k2,v2)])
        '''
        kv_insert = list()
        if not isinstance(kv, (list,tuple)):
            raise RuntimeError('key/value should be packed in the list or tuple')
        
        # put([(k1,v1), (k2,v2)])
        if len(kv) == 1 \
            and isinstance(kv[0], (list, tuple)):
            
            kv_insert = [self.prepare_kv(*kvs, backend='sqlite') for kvs in kv[0]]

        # put(k,v)
        elif len(kv) == 2 \
            and not isinstance(kv[0], (list, tuple)) \
            and not isinstance(kv[1], (list, tuple)):
            
            kv_insert.append(self.prepare_kv(*kv, backend='sqlite'))

        else:
            raise RuntimeError('Incorrect format of key/values, %s' % kv)

        SQL_INSERT = 'INSERT OR REPLACE INTO %s (k,v) ' % self._collection
        SQL_INSERT += 'VALUES (?,?)'
        self._cursor.executemany(SQL_INSERT, kv_insert)

    def _get_one(self, _key):
        ''' return document by _key 
        '''        
        _key = self.prepare_key(_key)
        SQL = 'SELECT k,v FROM %s WHERE k = ?;' % self._collection
        try:
            self._cursor.execute(SQL, (_key,))
        except Exception, err:
            raise RuntimeError(err)
        result = self._cursor.fetchone()
        if result:
            try:
                if _key == self._ZEROS_KEY:
                    v = cPickleSerializer.loads(result[1])
                else:
                    v = self._serializer.loads(result[1])
            except Exception, err:
                raise RuntimeError('key %s, %s' % (_key, err))
            return (result[0], v)
        else:
            return (None, None)

    def _get_many(self, *_keys):
        ''' return docs by keys or all docs if keys are not defined 
        '''        
        if _keys:
            if isinstance(_keys, (list, tuple)):
                # check if keys are even
                for key in _keys:
                    if key == self._ZEROS_KEY:
                        continue
                    key = self.prepare_key(key)
                SQL_SELECT_MANY = 'SELECT k,v FROM %s WHERE k IN ({seq})';
                SQL_SELECT_MANY %= (self._collection)
                SQL_SELECT_MANY = SQL_SELECT_MANY.format(seq=','.join(['?']*len(_keys)))
                self._cursor.execute(SQL_SELECT_MANY, _keys)
                result = self._cursor.fetchall()
                if not result:
                    return
                for r in result:
                    k = r[0]
                    if k == self._ZEROS_KEY:
                        continue
                    try:
                        v = self._serializer.loads(r[1])
                    except Exception, err:
                        raise RuntimeError('key %s, %s' % (k, err))
                    yield (k, v)

    def _get_all(self):
        ''' return all docs 
        '''        
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
                if k == self._ZEROS_KEY:
                    continue
                try:
                    v = self._serializer.loads(r[2])
                except Exception, err:
                    raise RuntimeError('key %s, %s' % (k, err))
                yield (k, v)

    __iter__ = _get_all

    def _get_paged(self, offset=None, limit=ITEMS_PER_REQUEST):
        ''' return docs by offset and limit
        
        offset and limit are used for pagination, for details 
        see BaseCollection.get()
        '''        
        if not offset and not limit:
            return
        
        SQL_SELECT_MANY = 'SELECT k,v FROM %s WHERE k <> ? LIMIT %d, %d ;'
        SQL_SELECT_MANY %= (self._collection, int(offset), int(limit))
        self._cursor.execute(SQL_SELECT_MANY, (self._ZEROS_KEY, ))
        result = self._cursor.fetchall()
        if not result:
            return
        for r in result:
            k = r[0]
            if k == self._ZEROS_KEY:
                continue
            try:
                v = self._serializer.loads(r[1])
            except Exception, err:
                raise RuntimeError('key %s, %s' % (k, err))
            yield (k, v)

    def delete(self, k):
        ''' delete document by k 
        '''
        _key = self.prepare_key(k)
        if _key == self._ZEROS_KEY:
            raise RuntimeError('Metadata cannot be deleted')
        SQL_DELETE = '''DELETE FROM %s WHERE k = ?;''' % self._collection
        self._cursor.execute(SQL_DELETE, (_key,))
                    
 
