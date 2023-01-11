#!/bin/bash
if [ -z "$1" ]; then
  python3 -m unittest discover -s ./tests/integration -t ./
else
  python3 -m unittest discover -s ./tests/integration -t $1
fi