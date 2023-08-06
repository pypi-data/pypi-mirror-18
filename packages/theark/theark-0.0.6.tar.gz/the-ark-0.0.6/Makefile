test: lint unittest

unittest:
	@nosetests --with-coverage --cover-html --cover-erase --cover-branches --cover-package=the_ark

lint:
	@find . -name '*.py' -exec flake8 {} \;

verboselint:
	@find . -name '*.py' -exec flake8 --show-pep8 --show-source {} \;

clean:
	@find . -name "*.pyc" -delete

.PHONY: test unittest lint verboselint clean
