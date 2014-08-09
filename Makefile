clean:
	rm -rf build
	rm -rf dist
	rm -rf gitime.egg-info
	rm -rf docs/_build/doctrees
	rm -rf docs/_build/html

reinstall:
	pip uninstall -y gitime
	python setup.py install

3install:
	python3 setup.py install

uninstall:
	pip uninstall -y gitime

test:
	python -Wall -3 -m unittest discover tests/ '*test.py' --failfast
	python3 -Wall -m unittest discover tests/ '*test.py' --failfast

publish:
	python setup.py sdist upload