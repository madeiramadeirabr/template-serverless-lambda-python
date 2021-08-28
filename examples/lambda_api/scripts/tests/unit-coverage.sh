#python -m xmlrunner discover -t ./ --output-file ./target/unit/junit-report.xml
coverage run -m unittest discover -s ./tests/unit -t ./
coverage report
coverage xml
coverage html
coverage2clover -i ./target/unit/report.xml -o ./target/unit/clover.xml
echo 'results generated in ./target/unit/coverage_html/'
