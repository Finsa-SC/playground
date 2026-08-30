#!/bin/bash

greeting() {
  echo "Hello $1, how are you today?"
}

NAME=$1
if [[ -n $NAME ]]; then
  echo "True"
  greeting "$NAME"
else
  greeting "noname"
fi
