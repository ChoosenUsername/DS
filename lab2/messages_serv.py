from flask import Flask, request, Response
from flask_restful import Resource, Api
import sys
import os
import uuid
import requests
import json


app = Flask(__name__)
api = Api(app)
port = 5508

@app.route('/', methods = ['GET'])
def user():
    if request.method == 'GET':
        msg = 'Not implemented yet'
        return {
            "msg": msg,
        }

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=port)

