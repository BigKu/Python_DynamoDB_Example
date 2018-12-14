#!/bin/sh

path=$(cd "$(dirname "$0")" && pwd)
cd $path

. venv/bin/activate

export FLASK_APP=app.py
flask run --host=0.0.0.0
