#!/usr/bin/bash

num1 = $1
op = $2
num2 = $3

if [ -z num1 || -z num2 || -z op ]; then
	echo "Missing argument!"
	return 1
fi

if [ op]
