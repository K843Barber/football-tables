#!/bin/bash

function create_venv
{
    python3 -m venv .venv
    . .venv/bin/activate
    python3 -m pip install pip -U --quiet
    pip3 install -e . --quiet
}

if test -d .venv/; then
    . .venv/bin/activate
    echo "Directory Exists!"
    python3 --version --version
else
    echo "Missing venv, will create now!"
    create_venv &
    python3 --version --version
fi
