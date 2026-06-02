#!/bin/bash

#Aritmathic
#angka1=3
#angka2=5
#
#result=$((angka1 + $angka2))
#
#echo $result
#
#echo ""
#
#declare -i port=80
#echo $port
#port="ambatukam"
#echo $port

## Declare

#declare -A name
#
#name=rikka
#echo $name


declare -A name
declare -A name

student[name]=rikka
student[age]=17
student[gender]=famale

if [ student[gender] == "male" ] then;



echo "Hello ${name} ${if gender == "male" then "kun" else "chan"},"