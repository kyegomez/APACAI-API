.PHONY: build upload

build:
	APACAI_UPLOAD=y python setup.py sdist

upload:
	APACAI_UPLOAD=y twine upload dist/*
