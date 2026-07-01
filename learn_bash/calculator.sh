#!/usr/bin/bash

#Input validation
if [[ -z $1 || -z $2 || -z $3 ]]; then
  echo "Missing argument detected!"
  exit 0
elif [[ $1 =~ ^[0-9]*$ ]]; then
  echo "Invalid number, please input digit only"
  exit 0
fi

# Input value when call this script [./calculator 2 + 3]
if [[ $2 == "+" ]]; then
  echo $(( $1 + $3 ))
elif [[ $2 == "-" ]]; then
  echo $(( $1 - $3 ))
elif [[ $2 == "x" ]]; then
  echo $(( $1 * $3 ))
elif [[ $2 == "/" || $2 == ":" ]]; then
  if (( $3 != 0 )); then
    echo $(( $1 / $3 ))
  else
    echo "Can't divide with zero"
  fi
elif [[ $2 == "xx" ]]; then
  echo $(( $1**$3 ))
else
  echo "invalid operation input"
fi