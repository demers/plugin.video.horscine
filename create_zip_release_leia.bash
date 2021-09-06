#!/bin/bash

cd ..
rm -f plugin.video.horscine_leia.zip
cd plugin.video.horscine
cp -f addon.xml addon-matrix.xml
cp -f addon-leia.xml addon.xml
cd ..
zip -r plugin.video.horscine_leia.zip plugin.video.horscine/* -x "*tests-venv*" -x "*tests*" -x "*.bash" -x "*.pyo" -x "*__pycache__*" -x "*addon-matrix.xml" -x "*addon-leia.xml"
cd plugin.video.horscine
rm -f addon.xml
cp -f addon-matrix.xml addon.xml
mv -f addon-matrix.xml /tmp