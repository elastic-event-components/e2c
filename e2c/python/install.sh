#!/usr/bin/env bash

# build virtual environment
python3.6 -m venv venv

# activate the environment
source venv/bin/activate

# update pip and install wheel.
pip install --upgrade pip
pip install wheel
pip install pylint

# install the packages
pip install -I -r scripts/require.txt
