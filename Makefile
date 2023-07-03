install:
	poetry install
	
test:
	poetry run pytest

benchmark:
	g++ benchmarking/benchmarking.cpp -o ./benchmarking/cppBenchmark
	poetry run python benchmarking/benchmarking.py