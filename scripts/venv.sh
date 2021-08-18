python3 -m venv venv
source ./venv/bin/activate

if test -f "./scripts/install.sh"; then
  sh ./scripts/install.sh
fi