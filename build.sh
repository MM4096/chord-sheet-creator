#!/bin/bash

cd "$(dirname "$0")" || exit
source .venv/bin/activate
pyinstaller -F -n "chord-chart-creator" --add-data "fonts:fonts" --add-data "style.css:." main.py
