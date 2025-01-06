PYPI=https://artifactory.jpl.nasa.gov/artifactory/api/pypi/pypi


build: clean
	python3 setup.py sdist bdist_wheel

upload: repository ?= develop
upload:
	twine upload \
		--verbose \
		--repository-url "$(PYPI)-$(repository)-local" \
		dist/*

clean:
	rm -rf .pytest_cache
	rm -rf build
	rm -rf dist
	rm -rf *.egg-info
	rm -rf __pycache__
	find . | grep -E "(__pycache__|\.pyc$$)" | xargs rm -rf