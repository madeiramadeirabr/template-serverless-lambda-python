#!/bin/bash
if [ -z "$1" ]; then
  coverage run -m unittest discover -s ./tests/integration -t ./
else
  coverage run -m unittest discover -s ./tests/integration -t $1
fi
coverage report
coverage xml -o ./target/integration/report.xml
coverage html --omit="*/test*,venv/*,vendor/*" -d ./target/integration/coverage_html/
coverage2clover -i ./target/integration/report.xml -o ./target/integration/clover.xml
echo 'results generated in ./target/integration/coverage_html/'
