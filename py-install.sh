#!/bin/sh

path=$(cd "$(dirname "$0")" && pwd)
cd $path

# Install any needed packages specified in requirements.txt
rm -rf $path/venv && \
python3 -m venv venv && \
. venv/bin/activate && \
python3 -m pip install --upgrade pip && \
python3 -m pip install --trusted-host pypi.python.org -r $path/requirements.txt && \
sed -i 's/false/true/g' $path/venv/pyvenv.cfg

# nothing
# python3 -m venv --system-site-packages venv
# python3 -m pip install --trusted-host pypi.python.org -r $path/requirements.txt
