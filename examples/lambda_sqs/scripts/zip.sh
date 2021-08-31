if test -f .projectrc; then
  source .projectrc
elif test -f ./bin/.projectrc; then
  source ./bin/.projectrc
fi

if [ -z "$PROJECT_NAME" ]; then
  echo 'PROJECT_NAME not defined'
  exit 1
else
  zip -r $PROJECT_NAME.zip ./ -x '*.git*' -x './zip.sh*' -x './venv/*' -x './.idea/*'  -x './node_modules/*'
fi
