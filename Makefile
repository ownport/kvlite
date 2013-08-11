# TODO generate final testing report

test-all:
	@ touch tests/db/none.kvlite
	@ touch tests/db/none.sqlite
	@ rm tests/db/*.kvlite	
	@ rm tests/db/*.sqlite
	@ nosetests

test-all-with-coverage:
	@ touch tests/db/none.kvlite
	@ touch tests/db/none.sqlite
	@ rm tests/db/*.kvlite	
	@ rm tests/db/*.sqlite
	@ nosetests --with-coverage

test-performance:
	@ echo 'Performance tests'

graph:
	@ dot -T png docs/kvlite.gv -o docs/kvlite.png && eog docs/kvlite.png

distrib:
	@ rm -R build/
	@ rm -R dist/
	@ rm -R kvlite.egg-info/
	@ python setup.py sdist


