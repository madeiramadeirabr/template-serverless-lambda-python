#!/bin/bash
if [ -z "$1" ]; then
  python3 -m unittest discover -s ./tests/component -t ./
else
  python3 -m unittest discover -s ./tests/component -t $1
fi