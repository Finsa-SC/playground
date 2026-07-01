#!/bin/bash

greetings(){
  echo "Hello, $*"
}

greetings "agus" "Ridwan"


calculator() {
  if [[ $2 == "+" ]]; then
    echo $(( $1 + $3))
  fi
}

calculator 2 + 2