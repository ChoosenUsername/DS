import time

import pika
from flask import Flask, request, jsonify

from facade import queue_name
from multiprocessing import Process, Manager
global total_str2
total_str2 = list()
app = Flask(__name__)


def consume(final_list):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue=queue_name)
    def callback_(ch, method, properties, body):
        print(" [x] Received {}".format(body))
        final_list.append(str(body))
    channel.basic_consume(queue=queue_name, on_message_callback=callback_, auto_ack=True)
    channel.start_consuming()

@app.route('/', methods=['GET', 'POST'])
def message_f():
    global total_str2
    if request.method == 'POST':
        manager = Manager()
        final_list = manager.list()
        p1 = Process(target=consume, args=(final_list,))
        p1.start()
        time.sleep(3)
        p1.terminate()
        total_str2 += final_list
        return jsonify({"is_success": True})

    if request.method == 'GET':
        return " ".join(total_str2)


if __name__ == "__main__":
    app.run(port=5005)