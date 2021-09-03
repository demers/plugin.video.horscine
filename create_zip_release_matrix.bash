#!/bin/bash

cd ..
rm -f plugin.video.horscine.zip
zip -r plugin.video.horscine.zip plugin.video.horscine/* -x "*tests-venv*" -x "*tests*" -x "*.bash" -x "*__pycache__*"