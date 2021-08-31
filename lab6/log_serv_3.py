from flask import Flask, request
from flask_restful import Resource, Api
import hazelcast
import sys
import os
import uuid
import requests
import json


app = Flask(__name__)
api = Api(app)
port = 5003

client = hazelcast.HazelcastClient(
        cluster_members=["192.168.1.102:5703"]
        )
my_map = client.get_map("my-distributed-map").blocking()

@app.route('/', methods = ['POST','GET'])
def user():
    if request.method == 'POST':
        msg = request.args["message"]
        id = request.args["uuid"]
        print(id,msg)
        
        my_map.put(id,msg)

        return "done"
    if request.method == 'GET':

        msg = msg = ' '.join(map(str, my_map.values()))
        
        return {
            "msg":msg
        }

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=port)

