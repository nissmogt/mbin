#!/bin/bash
module load MATLAB/2021a
cd /opt/apps/software/MATLAB/2021a/extern/engines/python/
#python setup.py build --build-base=$HOME/.cache install --prefix=$HOME/.conda/envs/bio
# Workaround for cloud-based licensing issue
python setup.py build --build-base=$(mktemp -d) install --user

