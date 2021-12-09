#python -m xmlrunner discover -t ./ --output-file ./target/unit/junit-report.xml
python3 -m coverage run -m unittest discover -s ./tests/unit -t ./
python3 -m coverage report
python3 -m coverage xml
coverage2clover -i ./target/unit/report.xml -o ./target/unit/clover.xml