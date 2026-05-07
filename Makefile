.PHONY: run clean test

run:
	python main.py sample.lua

test:
	python main.py sample.lua

clean:
	rm -f benchmarks.txt
	rm -rf __pycache__
