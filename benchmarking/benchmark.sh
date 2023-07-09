
folderName=$1
echo "Processing folder: $folderName"
start=$(date +%s.%N)
poetry run python benchmarking/py/benchmarking.py $folderName
end=$(date +%s.%N)
runtime=$(python -c "print(${end} - ${start})")
echo "Runtime Python was: ${runtime}"

g++ benchmarking/cpp/benchmarking.cpp -o ./benchmarking/cpp/cppBenchmark

start=$(date +%s.%N)
./benchmarking/cpp/cppBenchmark $folderName
end=$(date +%s.%N)
runtime=$(python -c "print(${end} - ${start})")
echo "Runtime C++ was: ${runtime}"

cargo build --release --manifest-path ./benchmarking/rust/benchmark/Cargo.toml
start=$(date +%s.%N)
./benchmarking/rust/benchmark/target/release/benchmark $folderName
end=$(date +%s.%N)
runtime=$(python -c "print(${end} - ${start})")
echo "Runtime Rust was: ${runtime}"