======
kvlite
======

kvlite is small library for storing documents in SQL databases. At the moment supported MySQL and SQLite. A document can be string, list/tuple or dictionary. But of course it possible to define own serialization to store data in kvlite database.

A collection is a group of documents stored in kvlite, and it can be thought of as roughly the equivalent of a  table in a relational database.

Installation
============

To install kvlite you just need to copy two files: kvlite.py and kvlite-cli.py. Second one is optional and it will be needed only if you need to have access to kvlite collections via console. Also kvlite-cli.p can be used as example how to use kvlite library.

Examples of use
===============

    >>> import kvlite
    >>> collection = open('sqlite://memory:test_collection')
    >>> collection
    <kvlite.SqliteCollection object at 0x14cb350>
    >>> collection.count
    0
    >>> collection.put('1', 'first document')
    >>> collection.put('2', ('second', 'document'))
    >>> collection.put('3', {'third': 'document'})
    >>> collection.count
    3
    >>> collection.get('1')
    ('1', 'first document')
    >>> collection.get('2')
    ('2', ('second', 'document'))
    >>> collection.get('3')
    ('3', {'third': 'document'})
    >>>
    >>> [k for k in collection.keys() ]
    ['1', '2', '3']
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

Another topics
==============

.. _kvlite structure: https://github.com/ownport/kvlite/blob/master/docs/kvlite.png
 .. _Link collection to similar projects or where the ideas were taken: https://github.com/ownport/kvlite/blob/master/docs/links.md

