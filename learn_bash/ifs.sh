#!/usr/bin/bash

FILE_PATH="dummy.txt"

if [[ ! -f $FILE_PATH ]]; then
  echo "File not found"
  exit 1
fi

i=1
while IFS= read -r line; do
  echo "${i}. $line"
  (( i++ ))
done < "$FILE_PATH"
