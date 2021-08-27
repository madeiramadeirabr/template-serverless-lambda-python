from flask import Flask

from flask_app.decorators import LambdaDecorator


class LambdaApp(Flask, LambdaDecorator):
    pass