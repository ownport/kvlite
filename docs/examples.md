# Examples

## kvlite as library

```python
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
>>> for k,v in collection: print k,v
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
00000000971b2b077bc244bcaf54960299aec500 {'description': 'Third example of usage kvlite database', 'name': 'Example3', 'id': 3}    
>>>
>>> for k in [key1, key2, key3]: collection.delete(k)
>>> collection.count
0
>>> collection.close()
>>>
```

## kvlite.cli

`kvlite.cli` module is used for get access to kvlite databases via console

```
$ python -m kvlite.cli
kvlite>
kvlite> ?

   help <command>	show <command> help
   version		show kvlite version
   licence		show licence
   history		show commands history 
   exit			exit from console 

   create <name> <uri>		    create new collection (if not exists)
   use <collection_name>	    use the collection as the default (current) collection
   show collections <details>	list of available collections
   remove <collection_name>	    remove collection
   import <filename>		    import collection configuration from JSON file
   export <filename>		    export collection configurations to JSON file
   copy <source> <target>	    copy data from source kvlite database to target kvlite database
                                <source> - reference name to source database
                                <target> - reference name to target database
                                for creating reference name, use `create` command

   hash [string]	    generate sha1 hash, random if string is not defined
   items		        list of collection's items 
   get <key>		    show collection entry by key
   put <key> <value>	store entry to collection, where <value> is data in JSON format
   delete <key>		    delete entry by key 
   count		        show the amount of entries in collection 
   scheme		        show structure of collection
   index <details>	    make index for current collection

kvlite> 
```

## kvlite.webui

`kvlite.webui` module is used for get access to kvlite databases via web interface

```
$ python -m kvlite.webui
Bottle v0.11.6 server starting up (using WSGIRefServer())...
Listening on http://127.0.0.1:8080/
Hit Ctrl-C to quit.

```
then open url `http://127.0.0.1:8080` in your browser

## Bulk put()

When you need to insert many documents to kvlite database

```python
import kvlite
collection = kvlite.open('sqlite://memory:test')
kvs = [(k,'value:%d' % k) for k in xrange(100)]
collection.put(kvs)
collection.commit()
```

## Pagination

The examples how to use pagination with kvlite please see code for `webui`

## Migration data

### Copy data from database (v0.4.5) to database (v0.5.1)

Most simple way to migrate data from v0.4.5 database to v0.5.1 database is copy data

```python
>>> import kvlite
>>> source = kvlite.open('sqlite://tests/db/test1.kvlite', cPickleSerializer)
>>> target = kvlite.open('sqlite://tests/db/test2.kvlite', cPickleSerializer)
>>> kvlite.copy(source, target)
>>>
```

