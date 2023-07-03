install:
	poetry install
	
test:
	poetry run pytest

benchmark:
	poetry run python benchmarking/benchmarking.py