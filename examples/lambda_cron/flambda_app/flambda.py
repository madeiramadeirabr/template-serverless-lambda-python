"""
Flambda Framework Module
Version: 1.0.0
"""
from flask import Flask

try:
    """
    If the decorators folder is present
    """
    from flambda_app.decorators import LambdaDecorator

    class Flambda(Flask, LambdaDecorator):
        pass
except Exception as err:
    class Flambda(Flask):
        pass
