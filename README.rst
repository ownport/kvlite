======
kvlite
======

kvlite is small open-source library for storing documents in SQL databases. Only three methods are needed to manipulate documents in database: get(), put(), delete(). At the moment supported MySQL and SQLite databases only. A document can be string, list/tuple or dictionary. Default serialization is based on cPickleSerializer methods but of course it is possible to define own serialization to store data in kvlite databases. 

A ``document`` is a string, list/tuple, dictionary or any structure which can be serialized by cPickle or JSON

A ``collection`` is a group of documents stored in kvlite. It can be thought of as roughly the equivalent of a table in a relational database.

The format of ``uri`` (uniform resource identifier) for databases:

 * for mysql: 'mysql://username:password@hostname:port/database.collection_name'
 * for sqlite: 'sqlite://path-to-sqlite-file:collection_name' or 'sqlite://memory:collection_name'
 
In case when sqlite is in use two variants of collection is possible: store data in file or store data in memory.

Examples of use
===============

    >>> import kvlite
    >>> collection = kvlite.open('sqlite://memory:test')
    >>> collection
    <kvlite.SqliteCollection object at 0x14cb350>
    >>> collection.count
    0
    >>> key1 = collection.get_uuid()
    >>> key1
    '00000000594d699229ac4f46b2deee895e5683dc'    
    >>> document1 = {'id': 1, 'name': 'Example1', 'description': 'First example of usage kvlite database',}
    >>> collection.put(key1, document1)
    >>>
    >>> key2 = collection.get_uuid()
    >>> document2 = {'id': 2, 'name': 'Example2', 'description': 'Second example of usage kvlite database',}
    >>> collection.put(key2, document2)
    >>>
    >>> key3 = collection.get_uuid()
    >>> document3 = {'id': 3, 'name': 'Example3', 'description': 'Third example of usage kvlite database',}
    >>> collection.put(key3, document3)
    >>>
    >>> collection.count
    3
    >>>
    >>> for k,v in collection.get(): print k,v
    ... 
    00000000594d699229ac4f46b2deee895e5683dc {'description': 'First example of usage kvlite database', 'name': 'Example1', 'id': 1}
    000000007dfb322f91a64e5eafe91b73d041be1c {'description': 'Second example of usage kvlite database', 'name': 'Example2', 'id': 2}
    00000000971b2b077bc244bcaf54960299aec500 {'description': 'Third example of usage kvlite database', 'name': 'Example3', 'id': 3}
    >>>
    >>> collection.get({'_key': key1})
    ('00000000594d699229ac4f46b2deee895e5683dc', {'description': 'First example of usage kvlite database', 'name': 'Example1', 'id': 1})
    >>>
    >>> for k,v in collection.get({'_key': [key1, key2, key3]}): print k,v
    ... 
    00000000594d699229ac4f46b2deee895e5683dc {'description': 'First example of usage kvlite database', 'name': 'Example1', 'id': 1}
    000000007dfb322f91a64e5eafe91b73d041be1c {'description': 'Second example of usage kvlite database', 'name': 'Example2', 'id': 2}
    00000000971b2b077bc244bcaf54960299aec500 {'description': 'Third example of usage kvlite database', 'name': 'Example3', 'id': 3}    >>>
    >>> for k in [key1, key2, key3]: collection.delete(k)
    >>> collection.count
    0
    >>> collection.close()
    >>>

Installation
============

please check installation guideline <https://github.com/ownport/kvlite/blob/v0.5/docs/install.md>

Usage
=====
 - Search criterias <https://github.com/ownport/kvlite/blob/v0.5/docs/search-criterias.md>
 - Pagination

Developer interface
===================
 - Utils <https://github.com/ownport/kvlite/blob/v0.5/docs/api.md#collection-utils>
 - Collection <https://github.com/ownport/kvlite/blob/v0.5/docs/api.md#collection>
 - CollectionManager <https://github.com/ownport/kvlite/blob/v0.5/docs/api.md#collectionmanager>
 - Serializers <https://github.com/ownport/kvlite/blob/v0.5/docs/api.md#serializers>
 - kvlite diagram <https://raw.github.com/ownport/kvlite/v0.5/docs/kvlite.png>

Articles
========
 - How FriendFeed uses MySQL to store schema-less data <https://github.com/ownport/kvlite/blob/v0.5/docs/articles/friendfeed-mysql-datastore.md>
 
Links
=====
 - Links <https://github.com/ownport/kvlite/blob/v0.5/docs/links.md> 


