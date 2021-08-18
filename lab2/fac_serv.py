from flask import Flask, request
from flask_restful import Resource, Api
import sys
import os
import uuid
import requests

app = Flask(__name__)
api = Api(app)
port = 5009


@app.route('/', methods = ['POST','GET'])
def user():
    if request.method == 'POST':
        data = request.args["msg"]
        id = str(uuid.uuid1())
        dictToSend = {"message": data, "uuid":id}
        print(dictToSend)
        res = requests.post('http://127.0.0.1:5506/', params=dictToSend)
        return "recieved"
    if request.method == 'GET':
        responce_messages = requests.get('http://127.0.0.1:5508/')
        print(responce_messages.json())

        responce_log = requests.get('http://127.0.0.1:5506/')
        print(responce_log.json())

        return {
            "final_answer" : responce_messages.json()["msg"] + " " + responce_log.json()["msg"] 
        }

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=port)
