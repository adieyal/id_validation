clean:
	rm -rf dist

build: clean
	python -m build

check: build
	twine check dist/*

test: check
	twine upload -r testpypi dist/*

publish: check
	twine upload dist/*
