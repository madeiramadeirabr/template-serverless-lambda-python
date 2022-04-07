import app
import serverless_wsgi

def handler(event, context):
    """Lambda event handler, invokes the WSGI wrapper and handles command invocation"""
    return serverless_wsgi.handle_request(app.APP, event, context)