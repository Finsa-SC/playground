#!/usr/bin/bash

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
    echo "Can't devine with zero"
  fi
elif [[ $2 == "xx" ]]; then
  echo $(( $1**$3))
else
  echo "invalid operation input"
fi