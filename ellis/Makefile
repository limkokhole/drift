# Makefile for SAcC/calc_sbpca/python
#
# 2013-10-01 Dan Ellis dpwe@ee.columbia.edu

# Compile rules for C-extension version of aucotorr

# darwinports
#PYDIR=/opt/local/Library
# homebrew
#PYDIR=/usr/local/Cellar/python/2.7.8_1
PYDIR=/System/Library

CFLAGS=-I${PYDIR}/Frameworks/Python.framework/Versions/2.7/include/python2.7 -I${PYDIR}/Frameworks/Python.framework/Versions/2.7/Extras/lib/python/numpy/core/include/numpy


# ---- Link ---------------------------
_autocorr_py.so: autocorr_py.o
	gcc -bundle -flat_namespace -undefined suppress -o _autocorr_py.so autocorr_py.o

# ---- gcc C compile ------------------
autocorr_py.o: autocorr_py.c
	gcc ${CFLAGS} -O3 -c autocorr_py.c


# Unit tests for python code

test: test_sacc test_audftr

test_sacc:
	python2.7 SAcC.py input8k.wav tmp.txt
	diff tmp.txt output-input8k-sacc-ref.txt

test_audftr:
	python2.7 audftrs.py input8k.wav tmp.txt
	diff tmp.txt output-input8k-audftr-ref.txt
