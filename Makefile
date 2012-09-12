# TODO generate final testing report

test-unittest:
	@ echo '***************************'
	@ echo '*       Unittests         *'
	@ echo '***************************'
	python tests/test_serializers.py
	python tests/test_mysql_collection.py
	python tests/test_sqlite_collection.py
	python tests/test_mysql_collection_manager.py
	python tests/test_sqlite_collection_manager.py
	python tests/test_collection_manager.py
	python tests/test_utils.py

test-doctest:
	@ echo '***************************'
	@ echo '*       Doctests          *'
	@ echo '***************************'
	python -m doctest tests/specs.md
	python -m doctest tests/mysql.md
	python -m doctest tests/sqlite.md

test-unittest-with-coverage:
	@ python-coverage -e
	@ python-coverage -x tests/test_serializers.py
	@ python-coverage -x tests/test_mysql_collection.py
	@ python-coverage -x tests/test_sqlite_collection.py
	@ python-coverage -x tests/test_mysql_collection_manager.py
	@ python-coverage -x tests/test_sqlite_collection_manager.py
	@ python-coverage -x tests/test_collection_manager.py
	@ python-coverage -x tests/test_utils.py
	@ python-coverage -rm kvlite.py

test-performance:
	@ echo 'Performance tests'

test-all:
	make test-unittest
	make test-doctest

graph:
	@ dot -T png docs/kvlite.gv -o docs/kvlite.png && eog docs/kvlite.png

todo:
	@ echo 
	@ echo "*** TODOs for kvlite.py ***"
	@ echo 
	@ awk '/# TODO/ { gsub(/^ /, ""); print }' kvlite.py
	@ echo 
	@ echo "*** TODOs for kvlite-cli.py ***"
	@ echo 
	@ awk '/# TODO/ { gsub(/^ /, ""); print }' kvlite-cli.py
	@ echo 

	
