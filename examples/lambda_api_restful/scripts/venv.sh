python3 -m venv venv
source ./venv/bin/activate

if test -f "./scripts/install.sh"; then
  bash ./scripts/install.sh
fi

if test -f "./scripts/tests/install-tests.sh"; then
  bash ./scripts/tests/install-tests.sh
fi