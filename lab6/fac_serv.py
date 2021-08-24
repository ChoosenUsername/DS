from flask import Flask, request
from flask_restful import Resource, Api
import sys
import os
import uuid
import requests
import random
import pika

app = Flask(__name__)
api = Api(app)
port = 5001

ports1 = ["5506", "5507", "5508"]
ports2 = ["5509", "5510"]

@app.route('/', methods = ['POST','GET'])
def user():
    if request.method == 'POST':
        data = request.args["msg"]
        id = str(uuid.uuid1())
        dictToSend = {"message": data, "uuid":id}
        print(dictToSend)
        res1 = requests.post('http://127.0.0.1:'+random.choice(ports1)+'/', params=dictToSend)

        connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()


        channel.queue_declare(queue='task_queue', durable=True)

        message = data
        channel.basic_publish(
            exchange='',
            routing_key='task_queue',
            body=message,
            properties=pika.BasicProperties(
            delivery_mode=2,  # make message persistent
        ))
        print(" [x] Sent %r" % message)
        connection.close()

        return "recieved"
    
    if request.method == 'GET':
        responce_messages = requests.get('http://127.0.0.1:' + random.choice(ports2) + '/')
        print(responce_messages.json())

        responce_log = requests.get('http://127.0.0.1:5506/')
        print(responce_log.json())

        return {
            "final_answer" : responce_messages.json()["msg"] + " and " + responce_log.json()["msg"] 
        }

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=port)
