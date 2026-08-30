#!/bin/bash

echo "Lower case"
NAME="HeLLo"
echo "$NAME"
NAME_LOWER="${NAME,,}"
echo "$NAME_LOWER"

echo "Upper case"
NAME_UPPER="${NAME^^}"
echo "$NAME_UPPER"

echo "Default value"
read -p "Input name: " NAME
echo "${NAME:-noname}"
echo "$NAME"

echo "Necesary value"
read -p "Necesary input name: " NAME
echo "${NAME:?you must input your name!}"
echo "$NAME"

NAME=""
echo "${NAME:=suzuka}"
echo "$NAME"
