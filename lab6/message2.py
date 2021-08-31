import pika
from flask import Flask

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

@app.route('/', methods=['GET'])
def message_f():

    print(" ".join(total_str2))
    return " ".join(total_str2)


if __name__ == "__main__":
    
    manager = Manager()
    final_list = manager.list()
    p1 = Process(target=consume, args=(final_list,))
    p1.start()


    total_str2 = final_list
    
    p2 = Process(app.run(port=5005))
    p2.start()
