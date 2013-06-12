# Developer interface

## URI

The format of ``URI`` (uniform resource identifier) for databases:

- for mysql: 'mysql://username:password@hostname:port/database.collection_name'
- for sqlite: 'sqlite://path-to-sqlite-file:collection_name' or 'sqlite://memory:collection_name'
 
In case when sqlite is in use two variants of collection is possible: store data in file or store data in memory.


## Serializers

It used for serialization data in kvlite databases. Default serializer is cPickleSerializer. 
Serializer is the class or module to serialize documents with, must have methods or functions named 
``dumps`` and ``loads``. Select which serializer use in database can be defined via `open(uri, serializer=cPickleSerializer)` function

- **class cPickleSerializer(object)**

    standard Python module `cPickle` is used for data serialization 

- **class CompressedJsonSerializer(object)**

    JSON format, compressed by zlib module is used for data serialization


## Collection Utils

- **open(uri, serializer=cPickleSerializer)**

    open collection by URI, 
    
    if collection does not exist kvlite will try to create it
    
    serializer: cPickleSerializer is the default,

    returns MysqlCollection or SqliteCollection object in case of successful opening or creation new collection 
    
- **remove(uri)**

    remove collection by URI

- **get_uuid(amount=100)**

    return the list of uuids. By `amount` argument you can define how many UUIDs will be generated and returned. By default `get_uuid` returns 100 UUIDs
 
- **dict2flat(root_name, source, removeEmptyFields=False)**

    returns a simplified "flat" form of the complex hierarchical dictionary

    Example of complex dictionary:
    ```python
    >>> import kvlite
    >>> kvlite.dict2flat('dict',{'a': [1,2,3,4],'b':5,'c':{'d':1,'e':2}})
    {'dict.c.e': 2, 'dict.c.d': 1, 'dict.a': [1, 2, 3, 4], 'dict.b': 5}
    >>>
    ```

- **docs_struct(documents)**

    returns structure for all documents in the list

    As example you can build structure of documents in your kvlite database
    ```python
    >>> docs_struct(collection.get())
    ```
- **tmp_name()**

    generate temporary collection name
    ```python
    >>> kvlite.tmp_name()
    'attjhhxv22'
    >>>
    ```

## Collection

Classes MysqlCollection and SqliteCollection inherited from BaseCollection class and have the same methods. No needs to create these classes directly, all access to required collection can be provided via `kvlite.open()` function. 

- **get_uuid()**

return one uuid. 
        
By `amount` argument you can define how many UUIDs will be generated and stored in cache if it's empty. By default 100 UUIDs will be generated.
        
If mysql connection is available more fast way to use this method than global function - get_uuid()

- **get(self, criteria=None, offset=None, limit=ITEMS_PER_REQUEST)**

returns documents selected from collection by criteria. How to define searching criterias please read <https://github.com/ownport/kvlite/blob/v0.5/docs/search-criterias.md>
        
If the criteria is not defined, get() returns all documents.

Hint: the combination `offset` and `limit` paramters can be used for pagination
        
`offset` - starts with this position in database
`limit` - how many document will be returned

- put(k,v)     - put key/value to storage. The key has limitation - only 40 bytes length. The value can be string, list or tuple, dictionary
- delete(k)    - delete key/value pair
- keys()       - returns the list of all keys in collection
- count()      - returns the amount of documents in collection
- commit()     - as kvlite based on transactional databases, commit() is used for commitment changes in collection
- close()      - close connection to database

## CollectionManager

Sometimes it will needed to manage collections: create, check if exists, remove. For these operations you can use CollectionManager. This class has the next methods:

- parse_uri(uri)   - depends on type of database, the function parse_uri() can returns deferent result based on which backend is used
- create(name)     - create collection
- connection       - returns refernce to database collection
- collection_class - returns class MysqlCollection or SqliteCollection depend on backend parameter in URI
- collections()    - returns the list of collections in database
- remove(name)     - remove collection
- close()          - close connection to database

## Serializers

- cPickleSerializer (used by default)
- CompressedJsonSerializer

Serializer can be defined for collection via open function. 
```python
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
```
For using JSON as serialization
```python
>>> collection = kvlite.open('sqlite://test.kvlite:test', serializer=kvlite.CompressedJsonSerializer)
>>>
```

To create custom serializer you need to create the class or module to serialize msgs with, must have methods or functions named `dumps(v)` and `loads(v)`

Please note that there's no way to store which serializer was used for collection. The collision is possible when during putting data to collection was used one serializer but during getting data was used another one.


