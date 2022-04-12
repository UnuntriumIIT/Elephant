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
    return client['elephant']

def callback(ch, method, properties, body):
    bodystr = json.loads(body.decode())
    
    dbname = getDatabase()
    collection_category = dbname["category"]
    collection_product = dbname["product"]
    
    if (properties.headers['event'] == 'CategoryCreated'):
        collection_category.insert_one(bodystr[0])
    elif (properties.headers['event'] == 'CategoryChanged'):
        collection_category.replace_one({"Id" : bodystr[0]["Id"]}, bodystr[0])
    elif (properties.headers['event'] == 'CategoryDeleted'):
        collection_category.delete_many(bodystr[0])
    elif (properties.headers['event'] == 'ProductCreated'):
        collection_product.insert_one(bodystr[0])
    elif (properties.headers['event'] == 'ProductChanged'):
        collection_product.replace_one({"Id" : bodystr[0]["Id"]}, bodystr[0])
    elif (properties.headers['event'] == 'ProductDeleted'):
        collection_product.delete_many(bodystr[0])
    else:
        print("Error in events")
    ch.basic_ack(method.delivery_tag, False)
    
channel.basic_consume(queue=os.environ['RABBIT_QUEUE'], on_message_callback=callback)

try:
    channel.start_consuming()
except KeyboardInterrupt:
    channel.stop_consuming()
    
if (channel.is_open):
    channel.stop_consuming()
connection.close()