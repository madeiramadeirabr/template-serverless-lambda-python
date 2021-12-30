if [ -z "$1" ]; then
  autopep8 --in-place --recursive
else
  autopep8 --in-place $1
fi
