coverage run -m unittest discover -s ./tests/component -t ./
coverage report
coverage xml -o ./target/component/report.xml
coverage html --omit="*/test*,venv/*,vendor/*" -d ./target/component/coverage_html/
coverage2clover -i ./target/component/report.xml -o ./target/component/clover.xml
echo 'results generated in ./target/component/coverage_html/'
