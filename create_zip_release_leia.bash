#!/bin/bash

cd ..
rm -f plugin.video.horscine.zip
mv addon.xml addon-matrix.xml
mv addon-leia.xml addon.xml
zip -r plugin.video.horscine_leia.zip plugin.video.horscine/* -x "*tests-venv*" -x "*tests*" -x "*.bash" -x "*__pycache__*"
mv addon.xml addon-leia.xml
mv addon-matrix.xml addon.xml