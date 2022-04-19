PORT=5001
echo "app port: $PORT"
export FLASK_ENV=development
export FLASK_APP=./scripts/queue-manager/queue-manager.py
# export FLASK_DEBUG=1
# flask run $1 $2
flask run --host=0.0.0.0 --port=$PORT

# ver
# https://www.treinaweb.com.br/blog/retornando-paginas-html-em-requisicoes-flask