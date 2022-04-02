test:
	python -m pytest -s tests/
install:
	chmod +x *.py
	cp -fv *.py ./bin/