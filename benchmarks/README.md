# Benchmarking

### Setup

The only requirement is installing the benchmarking dependencies:

```bash
pip install .[benchmarking]
```

### Running a Benchmark

1. Run a benchmark:

```bash
python -m benchmarks.<name>
```

2. View the outputs in:

```
benchmarks/<name>
```

### Creating Custom Benchmarks

A `benchmarker.py` module is provided to create custom benchmarks. Here’s how to use it:

1. Import the `benchmarker` module:

```python
import benchmarks.benchmarker as benchmarker
```

> **Important:** You must import the benchmarker **before importing extro**.

2. Start tracking by calling `benchmarker.start_tracking()` with the desired output path and benchmark duration:

```python
benchmarker.start_tracking("./path/to/benchmark", 15)  # duration in seconds
```

3. Import and run your project as usual. The benchmarker will automatically stop after the specified duration, generate a report, and exit the engine:

```python
import extro
```
