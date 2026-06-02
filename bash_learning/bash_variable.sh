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


declare -A student

student[name]="rikka"
student[age]=17
student[gender]="female"

if [ "${student[age]}" -lt 18 ]; then
  if [ "${student[gender]}" = "male" ]; then
    suffix="kun"
  else
    suffix="chan"
  fi
else
  suffix="san"
fi

echo "Hello ${student[name]}-${suffix}"


#
#echo "Hello ${name} ${if gender == "male" then "kun" else "chan"},"