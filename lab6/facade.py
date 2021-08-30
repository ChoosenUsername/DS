import copy
import json
import random
import uuid

from flask import Flask, request, jsonify
import requests as rq
import pika
queue_name = 'main_queue'
app = Flask(__name__)


ports1 = ["5003", "5002", "5001"]
ports2 = ["5010", "5005"]


global unique_id
unique_id = 0



@app.route('/', methods=['GET', 'POST'])
def user():
    if request.method == 'POST':

        data = request.args["msg"]

        #logging logic
        id = str(uuid.uuid1())
        dictToSend = {"message": data, "uuid":id}
        print(dictToSend)
        res = rq.post('http://127.0.0.1:'+random.choice(ports1)+'/', params=dictToSend)

        #messaging logic
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        channel.queue_declare(queue=queue_name)

        message_http = 'http://localhost:' +  random.choice(ports2) + '/'
        channel.basic_publish(exchange="", routing_key=queue_name, body=data)
        rq.post(message_http, json=None)

        return "done"
    
    if request.method == 'GET':
        
        #get messages from logs
        responce_log = rq.get('http://127.0.0.1:5001/')
        print("from logs: " + responce_log.json()["msg"])

        # get messages from message servers
        results_message1 = rq.get("http://localhost:5010/")
        results_message2 = rq.get("http://localhost:5005/")
        print("from message1 " + results_message1.text)
        print("from message2 " + results_message2.text)

        results_message = results_message1.text + results_message2.text + responce_log.json()["msg"]
        return results_message


if __name__ == "__main__":
    app.run(port=5000)
