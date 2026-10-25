#!/bin/bash

## 1 =============================
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

## 2 =======================
## Declare

#declare -A name
#
#name=rikka
#echo $name


## 3 ==========================
#declare -A student
#
#student[name]="rikka"
#student[age]=17
#student[gender]="female"
#
#if [ "${student[age]}" -lt 18 ]; then
#  if [ "${student[gender]}" = "male" ]; then
#    suffix="kun"
#  else
#    suffix="chan"
#  fi
#else
#  suffix="san"
#fi
#
#echo "Hello ${student[name]}-${suffix}"



## 4 ==========================
# Learn input

declare -A student

read -p "Nama  : " student[name]
read -p "Age   : " student[age]
read -p "Gender: " student[gender]

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