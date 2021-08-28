from flask import Flask

from lambda_app.decorators import LambdaDecorator


class LambdaApp(Flask, LambdaDecorator):
    pass
