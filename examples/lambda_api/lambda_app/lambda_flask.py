from flask import Flask

from lambda_app.decorators import LambdaDecorator


class LambdaFlask(Flask, LambdaDecorator):
    pass
