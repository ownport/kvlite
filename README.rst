======
kvlite
======

kvlite is small open-source library for storing documents in SQL databases. Only three methods are needed to manipulate documents in database: get(), put(), delete(). At the moment supported MySQL and SQLite databases only. A document can be string, list/tuple or dictionary. Default serialization is based on cPickleSerializer methods but of course it is possible to define own serialization to store data in kvlite databases. 

Terminology: 
- A document is a string, list/tuple, dictionary or any structure which can be serialized by cPickle or JSON
- A collection is a group of documents stored in kvlite. It can be thought of as roughly the equivalent of a table in a relational database.

Installation
============

To install kvlite you just need to copy two files: kvlite.py and kvlite-cli.py. Second one is optional and it's needed only if you need to have access to kvlite collections via console. Feel free to use kvlite-cli.py as example how to work with kvlite library.

If `pip <http://www.pip-installer.org/>` installed in your system, you can install kvlite via

    pip install kvlite

Examples of use
===============

    >>> import kvlite
    >>> collection = kvlite.open('sqlite://memory:test')
    >>> collection
    <kvlite.SqliteCollection object at 0x14cb350>
    >>> collection.count
    0
    >>> doc_key1 = '00dc4937d674754942b516a3a96d81415d'
    >>> document1 = {'id': 1, 'name': 'Example1', 'description': 'First example of usage kvlite database',}
    >>> collection.put(doc_key1, document1)
    >>>
    >>> doc_key2 = '00dc4937d674754942b516a3a96d81416e'
    >>> document2 = {'id': 2, 'name': 'Example2', 'description': 'Second example of usage kvlite database',}
    >>> collection.put(doc_key2, document2)
    >>>
    >>> doc_key3 = '00dc4937d674754942b516a3a96d81417f'
    >>> document3 = {'id': 3, 'name': 'Example3', 'description': 'Third example of usage kvlite database',}
    >>> collection.put(doc_key3, document3)
    >>>
    >>> collection.count
    3
    >>>
    >>> for k,v in collection.get(): print k,v
    ... 
    00dc4937d674754942b516a3a96d81415d {'description': 'First example of usage kvlite database', 'name': 'Example1', 'id': 1}
    00dc4937d674754942b516a3a96d81416e {'description': 'Second example of usage kvlite database', 'name': 'Example2', 'id': 2}
    00dc4937d674754942b516a3a96d81417f {'description': 'Third example of usage kvlite database', 'name': 'Example3', 'id': 3}
    >>>
    >>> collection.get({'_key': doc_key1})
    ('00dc4937d674754942b516a3a96d81415d', {'description': 'First example of usage kvlite database', 'name': 'Example1', 'id': 1})
    >>>
    >>> for k,v in collection.get({'_key': [doc_key1, doc_key2, doc_key3]}): print k,v
    ... 
    00dc4937d674754942b516a3a96d81415d {'description': 'First example of usage kvlite database', 'name': 'Example1', 'id': 1}
    00dc4937d674754942b516a3a96d81416e {'description': 'Second example of usage kvlite database', 'name': 'Example2', 'id': 2}
    00dc4937d674754942b516a3a96d81417f {'description': 'Third example of usage kvlite database', 'name': 'Example3', 'id': 3}
    >>>
    >>> collection.delete('1')
    >>> collection.delete('2')
    >>> collection.delete('3')
    >>> collection.count
    0
    >>> collection.close()
    >>>

Collection Utils
================

 - open(uri)        - open collection
 - remove(uri)      - remove collection
 - get_uuid(amount) - get list of uuid 
 
To get started just open() function is needed.

URI format is:

 - for mysql: `mysql://username:password@hostname:port/database.collection_name`
 - for sqlite: `sqlite://path-to-sqlite-file:collection_name` or `sqlite://memory:collection_name`
 
In case when sqlite is in use two variants of collection is possible: in file and in memory.

The function open(uri) returns MysqlCollection or SqliteCollection object

Collection
==========

MysqlCollection and SqliteCollection have the same methods:

 - get_uuid()   - in case of mysql use, this function will be working faster than for sqlite
 - get(k)       - if k(key) is not defined, the function get() returns the list of all documents in collection. Otherwise key/value pair is returned for defined k(key)
 - put(k,v)     - put key/value to storage. The key has limitation - only 40 bytes length. The value can be string, list or tuple, dictionary
 - delete(k)    - delete key/value pair
 - keys()       - returns the list of all keys in collection
 - count()      - returns the amount of documents in collection
 - commit()     - as kvlite based on transactional databases, commit() is used for commitment changes in collection
 - close()      - close connection to database

CollectionManager
=================

Sometimes it will needed to manage collections: create, check if exists, remove. For these operations you can use CollectionManager. This class has the next methods:

 - parse_uri(uri)   - depends on type of database, the function parse_uri() can returns deferent result based on which backend is used
 - create(name)     - create collection
 - connection       - returns refernce to database collection
 - collection_class - returns class MysqlCollection or SqliteCollection depend on backend parameter in URI
 - collections()    - returns the list of collections in database
 - remove(name)     - remove collection
 - close()          - close connection to database

Serializers
===========

 - cPickleSerializer (by default)
 - CompressedJsonSerializer

Serializer can be defined via open function

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

For using JSON as serialization

    >>> collection = open('sqlite://test.kvlite:test', serializer=json)
    >>>


Another topics
==============

 - kvlite structure <https://github.com/ownport/kvlite/blob/master/docs/kvlite.png>
 - Link collection to similar projects or where the ideas were taken <https://github.com/ownport/kvlite/blob/master/docs/links.md>

