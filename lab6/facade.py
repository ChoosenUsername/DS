import random
import uuid

from flask import Flask, request
import requests as rq
import pika
queue_name = 'main_queue'
app = Flask(__name__)


ports1 = ["5003", "5002", "5001"]
ports2 = ["5010", "5005"]


global unique_id
unique_id = 0



@app.route('/', methods=['POST'])
def send():

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

    channel.basic_publish(exchange="", routing_key=queue_name, body=data)

    return "done"


@app.route('/', methods=['GET'])
def receive():

    #get messages from logs
    responce_log = rq.get('http://127.0.0.1:5001/')
    print("from logs: " + responce_log.json()["msg"])

    # get messages from message servers
    results_message = rq.get("http://localhost:" + random.choice(ports2) + "/") 
    print("from message " + results_message.text)
        
    results_message = results_message.text + responce_log.json()["msg"]
    return results_message


if __name__ == "__main__":
    app.run(port=5000)
