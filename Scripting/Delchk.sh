#!/bin/bash

# ����Ƿ��ṩ���ļ���·����Ϊ����
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <directory>"
    exit 1
fi

# Ҫ�����Ŀ¼
DIR=$1

# ���Ŀ¼�Ƿ����
if [ ! -d "$DIR" ]; then
    echo "Error: Directory $DIR does not exist."
    exit 1
fi

# �ҵ���ɾ�����к�׺Ϊ .chk ���ļ�
find "$DIR" -type f -name "*.chk" -exec rm -v {} \;

echo "All .chk files in $DIR and its subdirectories have been deleted."