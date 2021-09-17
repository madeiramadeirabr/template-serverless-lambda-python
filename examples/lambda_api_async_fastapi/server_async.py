import uvicorn
from app import app

##http_server = WSGIServer(('0.0.0.0', 5000), app)
#http_server.serve_forever()


uvicorn.run(app, host="0.0.0.0", port=5000, log_level="info")