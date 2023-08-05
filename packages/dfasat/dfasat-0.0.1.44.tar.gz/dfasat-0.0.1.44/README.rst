# dfasat python package: flexible state-merging for python

This package brings a scikit-learn like interface for the dfasat tool. dfasat is a C++ program implementing a red-blue state-merging approach with flexibly exchangable merge heuristics.

## usage

Create a dfasat.DFASATEstimator object, call fit() and predict() on it. plot() requires graphviz and will output a rendering of the automaton.
A short introduction using ipython notebooks is available on automatonlearning.net.


## building

dfasat is a container package that currently does not include the binary, but the toolchain to build it. The setup.py file automatically clones and and builds the latest version from the current dfasat repository.
For this to work, it requires all the dependencies of dfasat (libgsl, libpopt) as well as lib-boost-python and a working castxml installation.

## copyright and thanks

dfasat was originally written by Marijn Heule and Sicco Verwer. The Python wrapper was written by Benjamin Loos under supervision of Chris Hammerschmidt.

