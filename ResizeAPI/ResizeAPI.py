from flask import Flask, redirect
import pika
import uuid
import time

api = Flask(__name__)

@api.route('/resize/<id>/<width>/<height>', methods=['GET'])
def handleRequest(id,width,height):
    connection = pika.BlockingConnection(pika.ConnectionParameters('127.0.0.1'))
    channel = connection.channel()
    channel.queue_declare(queue='resizequeue' , durable=True, exclusive=False, auto_delete=False)
    channel.confirm_delivery()
    newid = str(uuid.uuid4())
    
    try:
        channel.basic_publish(exchange='',
                      routing_key='resizequeue',
                      body=id+";"+width+";"+height+";"+newid,
                      properties=pika.BasicProperties(content_type='text/plain',
                                                          delivery_mode=1))
        print('publish: '+id+";"+width+";"+height+";"+newid)        
    except pika.exceptions.UnroutableError:
        print('fuck')
        handleRequest(id, width, height)
    time.sleep(1);
    return redirect("http://localhost?id="+id+"&newid="+newid, code=302)
    

if __name__ == '__main__':
    api.run() 