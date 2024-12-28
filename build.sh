#!/bin/bash

cd "$(dirname "$0")" || exit
source .venv/bin/activate
pyinstaller -F -n chord-chart-creator main.py
