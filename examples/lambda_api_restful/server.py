from gevent.pywsgi import WSGIServer
from app import APP

# Não remover do projeto, muito útil para executar o debug via IDE Pycharm
http_server = WSGIServer(('0.0.0.0', 5000), APP)
http_server.serve_forever()
