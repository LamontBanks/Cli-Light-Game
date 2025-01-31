#!/bin/bash

# Use the standard library's unittest module to
# run all the tests (discover) it can find in the src directory.
# https://coverage.readthedocs.io/en/7.6.10/#:~:text=pytest-,unittest,-nosetest
coverage run -m unittest discover -s src

coverage report -m