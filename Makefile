install:
	poetry install
	
test:
	poetry run pytest

benchmark:
	/bin/sh ./benchmarking/benchmark.sh

run: 
	poetry run python main.py