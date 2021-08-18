from flask import Flask, request
from flask_restful import Resource, Api
import sys
import os
import uuid
import requests
import json


app = Flask(__name__)
api = Api(app)
port = 5506

info = {}

@app.route('/', methods = ['POST','GET'])
def user():
    if request.method == 'POST':
        msg = request.args["message"]
        id = request.args["uuid"]
        print(msg,id)
        info[msg] = id
        print(info)
        return "done"
    if request.method == 'GET':
        msg = ' '.join(map(str, info.keys()))
        return {
            "msg":msg
        }

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=port)

