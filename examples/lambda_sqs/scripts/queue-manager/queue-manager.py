"""
Queue Manager
Version: 1.0.0
"""
from flask import Flask

APP = Flask(__name__)

@APP.route('/')
def index():
    return "<html><head></head><body>Queue Manager</body></html>"
