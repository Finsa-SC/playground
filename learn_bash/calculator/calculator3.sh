#!/bin/bash

function validate()
{
	$1="Hello"
	echo "$1"
}

name="Agus"
validate "$name"

echo "$name"
