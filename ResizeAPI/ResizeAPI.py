from flask import Flask, redirect
import pika

api = Flask(__name__)

@api.route('/resize/<id>/<width>/<height>', methods=['GET'])
def handleRequest(id, width,height):
    connection = pika.BlockingConnection(pika.ConnectionParameters('127.0.0.1'))
    channel = connection.channel()
    channel.queue_declare(queue='resizequeue' , durable=True)
    channel.basic_publish(exchange='',
                      routing_key='resizequeue',
                      body=id+";"+width+";"+height)
    return redirect("http://localhost?id="+id, code=302)

if __name__ == '__main__':
    api.run() 