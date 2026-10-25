#!/bin/bash

num1=$1
op=$2
num2=$3

if [[ -z $op || -z $num1 || -z $num2 ]]; then
	echo "Missing argument."
  exit 1
fi

if [[ ! $num1 =~ ^[0-9]+$ || ! $num2 =~ ^[0-9]+$ ]]; then
	echo "Invalid input, please input only digit character."
	exit 1
fi

if [[ $op == "+" ]]; then
	echo "$(( num1 + num2 ))"
elif [[ $op == "-" ]]; then
	echo "$(( num1 - num2 ))"
elif [[ $op == "x" ]]; then
	echo "$(( num1 * num2 ))"
elif [[ $op == ":" ]]; then
	if [[ $num2 == "0" ]]; then
		echo "Cannot divided by zero."
		exit 1
	fi
	echo "$(( $num1 / $num2 ))"

elif [[ $op == "%" ]]; then
	echo "$(( num1 % num2 ))"
else
	echo "Invalid operation input."
fi

exit 0
