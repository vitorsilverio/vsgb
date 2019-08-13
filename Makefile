.PHONY: build clean run

all: build

PY := python3

build:
	@echo "Building..."
	CFLAGS='-w' ${PY} setup.py build_ext --inplace

clean:
	@echo "Cleaning..."
	find . -name "*.pyo" -delete
	find . -name "*.pyc" -delete
	find . -name "*.so" -delete
	find . -name "*.c" -delete
	find . -name "*.h" -delete
	find . -name "__pycache__" -d -delete
	rm -rf ./build
	rm -rf ./dist
	rm -rf ./pygb.egg-info

run: build
	${PY} main.py -s -r tetris.gb