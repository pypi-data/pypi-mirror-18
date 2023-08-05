#!/usr/bin/env make
# Makefile - handy shortcuts for building, installing, etc

.PHONY: build clean upload install test benchmark flamegraph mac

install: build
	pip install -e .

build:
	python setup.py build

mac:
	./build.sh

clean:
	rm -rf *.so *.egg-info build *.png *.log *.svg

upload: clean
	python setup.py sdist
	# TODO: twine upload dist/*

test: install
	nose2 -v

benchmark: install
	python -m flamegraph -o libvnc.log test/benchmark.py
	python -m flamegraph -o govnc.log test/benchmark.py go

flamegraph: benchmark
	flamegraph.pl --title "LibVNC" libvnc.log > libvnc.svg
	flamegraph.pl --title "GoVNC" govnc.log > govnc.svg
