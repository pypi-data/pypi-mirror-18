#!/bin/bash

# TODO: Also need to add doctests...?

python -m pip install pytest numpy
python -m pip install -e ./

make -C tests >/dev/null

export PYTHONPATH="$PWD:$PYTHONPATH"
py.test $@ tests/
