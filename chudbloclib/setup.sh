#!/bin/bash

VIRTUAL_ENV=venv

if [[ ! -d $VIRTUAL_ENV ]]; then
    python3.7 -m $VIRTUAL_ENV $VIRTUAL_ENV
fi

source $VIRTUAL_ENV/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
