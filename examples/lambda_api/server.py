from gevent.pywsgi import WSGIServer
from app import app

# Não remover do projeto, muito útil para executar o debug via IDE Pycharm
http_server = WSGIServer(('0.0.0.0', 5000), app)
http_server.serve_forever()
