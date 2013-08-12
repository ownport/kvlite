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
	@ echo "remove old builds"
	@ test -d build && rm -R build || echo "No old builds"
	@ echo "remove old dist"
	@ test -d dist && rm -R dist || echo "No old dist"
	@ echo "remove old kvlite.egg-info"
	@ test -d kvlite.egg-info && rm -R kvlite.egg-info || echo "No old kvlite.egg-info"
	@ python setup.py sdist


