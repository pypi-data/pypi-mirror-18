#!/bin/bash

set -e

FILE="README.md"

# convert markdown to reStructured Text
if [ $(which pandoc) ]; then
	pandoc -f markdown -t rst $FILE > ${FILE%.md}.rst
else
	if [ $(which notify-send) ]; then
		notify-send -t 5000 "Error gendocs.sh" "Run: sudo apt-get install -y pandoc"
	else
		echo "*******************************************************************"
		echo "Error gendocs.sh! Run: sudo apt-get install -y pandoc"
		echo "*******************************************************************"
	fi
fi
