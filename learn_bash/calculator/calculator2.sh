#!/bin/bash

num1=$1
op=$2
num2=$3

# Validate number
if [[ ! $num1 =~ ^[0-9]+$ || ! $num2 =~ ^[0-9]+$ ]]; then
	echo "Invalid number."
	exit 1
fi
if [[ $num1 =~ ^0[0-9]+$ || $num2 =~ ^0[0-9]+$ ]]; then
	echo "Invalid number, zero cannnot be the first number."
	exit 1
fi

case $op in
	"+")
		echo "$(( num1 + num2 ))"
		;;
	"-")
		echo "$(( num1 - num2 ))"
		;;
	"*" | "x")
		echo "$(( num1 * num2 ))"
		;;
	"/")
		[[ $num2 == "0" ]] && echo "Cannot divided by zero." && exit 1
		echo "$(( num1 / num2 ))"
		;;
	"%")
		echo "$(( num1 % num2 ))"
		;;
	*)
		echo "Invalid operation."
		exit 1
esac

exit 0
