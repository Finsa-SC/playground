#!/bin/bash

CURRENT_DIR=$(pwd)
TARGET="belajar.sh"

FILE_PATH="$CURRENT_DIR/$TARGET"


echo -e "\n\n=============CHeck IS File and executeable=========="
## CHeck is file and executeable
if [[ -f $FILE_PATH && -x $FILE_PATH ]]; then
    echo -e "$FILE_PATH \nis file and executeable"
else
    echo -e "$FILE_PATH \nis not executeable"
fi

echo -e "\n\n=============CHeck IS Directory=========="
## Check is directory
DIRECTORY_NAME="test"
if [[ -d $DIRECTORY_NAME ]]; then
    echo "$DIRECTORY_NAME Is a Directory"
else
    echo -e "$DIRECTORY_NAME is not a directory"
fi


echo -e "\n\n=============CHeck None=========="
## CHeck None
SECRET_TEXT=$(cat "$FILE_PATH")
if [[ -z $SECRET_TEXT ]]; then
    echo "File already write yet"
else 
    echo -e "File already write \n $SECRET_TEXT"
fi