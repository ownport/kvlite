# Developer interface

## Collection Utils

- open(uri)        - open collection
- remove(uri)      - remove collection
- get_uuid(amount) - get list of uuid 
 
To get started just open() function is needed.

URI format is:

- for mysql: `mysql://username:password@hostname:port/database.collection_name`
- for sqlite: `sqlite://path-to-sqlite-file:collection_name` or `sqlite://memory:collection_name`
 
In case when sqlite is in use two variants of collection is possible: in file and in memory.

The function open(uri) returns MysqlCollection or SqliteCollection object

## Collection

MysqlCollection and SqliteCollection have the same methods:

- get_uuid()   - in case of mysql use, this function will be working faster than for sqlite
- get(k)       - if k(key) is not defined, the function get() returns the list of all documents in collection. Otherwise key/value pair is returned for defined k(key)
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
Please note that there's no way to store which serializer was used for collection. The collision is possible when during putting data to collection was used one serializer but during getting data was used another one.

For using JSON as serialization
```python
>>> collection = open('sqlite://test.kvlite:test', serializer=json)
>>>
```

To create custom serializer you need to create new class with static methods: `dumps(v)` and `loads(v)`

