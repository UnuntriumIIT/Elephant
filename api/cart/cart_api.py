from flask import Flask, redirect, request
from flask_restful import Api, Resource
import json
import os
import pika

app = Flask(__name__)
api = Api(app)

class Cart(Resource):
    def send_message(self, header, body):
        credentials = pika.PlainCredentials(os.environ['RABBIT_USER'], 
                                            os.environ['RABBIT_PASSWORD'])
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(os.environ['RABBIT_HOST'], 
                                      os.environ['RABBIT_PORT'], 
                                      '/', 
                                      credentials))
        
        channel = connection.channel()
        channel.queue_declare(queue=os.environ['RABBIT_QUEUE'] , 
                              durable=True, 
                              exclusive=False, 
                              auto_delete=False)
        channel.confirm_delivery()
        try:
            channel.basic_publish(exchange='',
                          routing_key=os.environ['RABBIT_QUEUE'],
                          body=json.dumps(body),
                          properties=pika.BasicProperties(content_type='text/plain',
                                                              delivery_mode=1,
                                                              headers={'event': header}))
            print('publish: '+header+ " " + body)        
        except pika.exceptions.UnroutableError as error:
            print(error)
    
    def get(self):
        return ''
    
    def post(self):
        return ''
    
    def put(self):
        return ''
    
    def delete(self):
        return ''

api.add_resource(Cart, "/api/cart", "/api/cart", "/api/cart/<string:id>")
