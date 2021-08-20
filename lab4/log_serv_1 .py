from flask import Flask, request
from flask_restful import Resource, Api
import sys
import os
import uuid
import requests
import json
import hazelcast


app = Flask(__name__)
api = Api(app)
port = 5506


client = hazelcast.HazelcastClient(
        cluster_members=["192.168.1.102:5701"]
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
