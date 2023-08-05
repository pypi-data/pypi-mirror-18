TARGET?=tests

SRC_PATH := django_pypiwik

VERSION := $(shell grep -Po '"(.*)"' $(SRC_PATH)/__init__.py | sed -e 's/"//g')

#test_default_python:
#	PYTHONPATH="." python tests/ -v
#
#test_py2:
#	@echo Executing test with python2
#	PYTHONPATH="." python2 tests/ -v
#
#test_py3:
#	@echo Executing test with python3
#	PYTHONPATH="." python3 tests/ -v
#
#test: test_py2 test_py3

compile:
	@echo Compiling python code
	python -m compileall $(SRC_PATH)/

compile_optimized:
	@echo Compiling python code optimized
	python -O -m compileall $(SRC_PATH)/

coverage:
	coverage erase
	PYTHONPATH="." coverage run --source='$(SRC_PATH)' --branch tests/__main__.py
	coverage xml -i
	coverage report -m

sonar:
	/usr/local/bin/sonar-scanner/bin/sonar-scanner -Dsonar.projectVersion=$(VERSION)

clean:
	find -name "*.py?" -delete
	rm -f coverage.xml testresults.xml
	rm -fr htmlcov dist build *.egg-info

release:
	python setup.py sdist upload -r pypi

travis: compile compile_optimized # test_default_python coverage

jenkins: travis sonar
