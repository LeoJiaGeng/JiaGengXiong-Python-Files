#!/bin/bash

# 检查是否提供了文件夹路径作为参数
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <directory>"
    exit 1
fi

# 要清理的目录
DIR=$1

# 检查目录是否存在
if [ ! -d "$DIR" ]; then
    echo "Error: Directory $DIR does not exist."
    exit 1
fi

# 找到并删除所有后缀为 .chk 的文件
find "$DIR" -type f -name "*.chk" -exec rm -v {} \;

echo "All .chk files in $DIR and its subdirectories have been deleted."