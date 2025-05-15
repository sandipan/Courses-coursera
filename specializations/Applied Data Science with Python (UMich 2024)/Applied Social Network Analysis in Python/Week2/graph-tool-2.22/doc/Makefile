all:
	sphinx-build -E -b html . build

latex:
	sphinx-build -E -b latex . build

test:
	sphinx-build -b doctest . build

test-noninteractive:
	sphinx-build -b doctest . build *.rst demos/inference/inference.rst

clean:
	rm -rf build

