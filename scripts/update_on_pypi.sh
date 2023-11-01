#!/bin/bash

python3 setup.py test
python3 setup.py sdist
pip wheel --no-deps -w dist .
twine upload dist/*
