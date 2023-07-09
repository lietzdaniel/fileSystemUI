install:
	poetry install
	
test:
	poetry run pytest

make benchmark folder=gui:
	
	/bin/sh ./benchmarking/benchmark.sh $(folder)

run: 
	poetry run python main.py