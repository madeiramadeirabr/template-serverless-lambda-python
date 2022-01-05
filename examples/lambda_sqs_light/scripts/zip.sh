if test -f .projectrc; then
  source .projectrc
elif test -f ./scripts/.projectrc; then
  source ./scripts/.projectrc
fi

if [ -z "$PROJECT_NAME" ]; then
  echo 'PROJECT_NAME not defined'
  exit 1
else
  zip -r $PROJECT_NAME.zip ./ -x '*.git*' -x './zip.sh*' -x './venv/*' -x './.idea/*'  -x './node_modules/*'
fi
