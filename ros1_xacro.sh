#!/bin/bash

cd urdf
find . -iname "*.urdf" | xargs sed -i '/<property/d'
