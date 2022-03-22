#!/bin/bash
echo "输入路径,例如/root/example"
read -p" :" path
cd $path
echo "行数"
find -name "*_gt.json" | wc -l
