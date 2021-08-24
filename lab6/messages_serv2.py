from flask import Flask, request, Response
from flask_restful import Resource, Api
import sys
import os
import uuid
import requests
import json


app = Flask(__name__)
api = Api(app)
port = 5510

@app.route('/', methods = ['GET'])
def user():
    if request.method == 'GET':
        with open('sample2.txt', 'r') as file:
            data = file.read().replace('\n', '')
      
        msg = data #'Not implemented yet'
        return {
            "msg": msg,
        }

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=port)

