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
    >>> for k in [doc_key1, doc_key2, doc_key3]: collection.delete(k)
    >>> collection.count
    0
    >>> collection.close()
    >>>

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


