# TODO generate final testing report

test-unittest:
	@ echo '***************************'
	@ echo '*       Unittests         *'
	@ echo '***************************'
	python tests/test_kvlite_utils.py
	python tests/test_selectdb.py

test-doctest:
	@ echo '***************************'
	@ echo '*       Doctests          *'
	@ echo '***************************'
	python -m doctest tests/specs.md
	python -m doctest tests/mysql.md
	python -m doctest tests/sqlite.md

test-all:
	make test-unittest
	make test-doctest

graph:
	@ dot -T png docs/kvlite.gv -o docs/kvlite.png && eog docs/kvlite.png

todo:
	@ echo 
	@ awk '/# TODO/ { gsub(/^ /, ""); print }' kvlite.py
	@ echo 
	
	
