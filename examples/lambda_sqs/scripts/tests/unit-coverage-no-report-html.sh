#!/bin/bash
if [ -z "$1" ]; then
  python3 -m coverage run -m unittest discover -s ./tests/unit -t ./
else
  python3 -m coverage run -m unittest discover -s ./tests/unit -t $1
fi
python3 -m coverage report
python3 -m coverage xml
coverage2clover -i ./target/unit/report.xml -o ./target/unit/clover.xml