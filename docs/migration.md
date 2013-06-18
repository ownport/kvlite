# Migration data

## Copy data from database (v0.4.5) to database (v0.5.1)

Most simple way to migrate data from v0.4.5 database to v0.5.1 database is copy data

```python
>>> import kvlite
>>> kvlite.copy(
...     'sqlite://tests/db/test1.kvlite', cPickleSerializer, 
...     'sqlite://tests/db/test2.kvlite', cPickleSerializer)

>>>
```
