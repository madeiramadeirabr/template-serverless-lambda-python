from fastapi import FastAPI
from lambda_app.decorators import LambdaDecorator

class LambdaFastAPI(FastAPI, LambdaDecorator):
    # def __init__(self, name):
    #     self.name = name
    #     super.__init__()
    pass
