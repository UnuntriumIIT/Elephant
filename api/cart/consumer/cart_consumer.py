import pika
import os
import json
from pymongo import MongoClient

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

def getDatabase():
    CONNECTION_STRING = os.environ['MONGO_CONN_STR']
    client = MongoClient(CONNECTION_STRING)
    return client['elephant_cart']

def callback(ch, method, properties, body):
    bodystr = json.loads(body.decode())
    dbname = getDatabase()
    collection_cart = dbname["cart"]

channel.basic_consume(queue=os.environ['RABBIT_QUEUE'], on_message_callback=callback)

try:
    channel.start_consuming()
except KeyboardInterrupt:
    channel.stop_consuming()
    
if (channel.is_open):
    channel.stop_consuming()
connection.close()
