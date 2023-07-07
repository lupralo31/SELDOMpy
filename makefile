all: src/*.c setup.py
	python3 setup.py build_ext --inplace
test: all
	python3 test_mod.py