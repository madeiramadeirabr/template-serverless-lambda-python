if [ -z "$1" ]; then
  autopep8 --in-place --recursive --aggressive
else
  autopep8 --global-config .pep8 --in-place --aggressive --verbose $1
fi
