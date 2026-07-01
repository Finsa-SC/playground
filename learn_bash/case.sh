#!/usr/bin/bash

if [[ -z $1 || -z $2 || -z $3 ]]; then
  echo "Missing argument"
  exit 1
elif [[ ! $1 =~ ^[0-9]+$ || ! $3 =~ ^[0-9]+$ ]]; then
  echo "Invalid input, please input digit"
  exit 1
fi

case $2 in
  "+")
    echo $(( $1 + $3 ))
    ;;
  "-")
    echo $(( $1 - $3 ))
    ;;
  "x")
    echo $(( $1 * $3 ))
    ;;
  "/")
    if (( $3 != 0 )); then
      echo $(( $1 / $3 ))
    else
      echo "Cannot divide with zero"
    fi
    ;;
  "xx")
    echo $(( $1**$3 ))
    ;;
  "%") 
    echo $(( $1 % $3 ))
    ;;
  *)
    echo "Invalid operator"
esac
