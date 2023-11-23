#!/bin/bash

cd urdf
find ./ -type f -name "*.urdf" -exec bash -c 'cp "$0" "${0/urdf/urdf.xacro}"' {} \;
find . -iname "*urdf.xacro" | xargs sed -i '2s|>| xmlns:xacro="http://wiki.ros.org/xacro">|' 
find . -iname "*urdf.xacro" | xargs sed -i '/<property/d'

