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
channel.queue_declare(queue='cart' , 
                      durable=True, 
                      exclusive=False, 
                      auto_delete=False)
channel.exchange_declare('shop', durable=True)
channel.queue_bind('cart', 'shop', routing_key='k')

def getCollection():
    CONNECTION_STRING = os.environ['MONGO_CONN_STR']
    client = MongoClient(CONNECTION_STRING)
    db = client['elephant_cart']
    return db["cart"]

def edit_product(collection, data):
    carts = collection.find({}, {'_id': False})
    for cart in carts:
        for pr in cart.get('Products'):
            if data.get('Id') == pr.get('Id'):
                cart['Total'] = str(float(cart['Total'])- (float(pr.get('Price')) * int(pr.get('Quantity_in_cart'))))
                cart['Total'] = str(float(cart['Total'])+ (float(data.get('Price')) * int(pr.get('Quantity_in_cart'))))
                pr['Name'] = data.get('Name')
                pr['Price'] = data.get('Price')
                collection.replace_one({"User_Id": cart.get("User_Id")}, cart)

def delete_product(collection, data):
    carts = collection.find({}, {'_id': False})
    for cart in carts:
        for pr in cart.get('Products'):
            if data.get('Id') == pr.get('Id'):
                cart['Total'] = str(float(cart['Total'])- (int(pr.get('Price')) * int(pr.get('Quantity_in_cart'))))
                cart.get('Products').remove(pr)
                collection.replace_one({"User_Id": cart.get("User_Id")}, cart)

def callback(ch, method, properties, body):
    bodystr = json.loads(body.decode())
    collection = getCollection()
    
    if (properties.headers['event'] == 'ProductChanged'):
        edit_product(collection, {
            "Id" : bodystr[0].get("Id"), 
            "Name" : bodystr[0].get("Name"), 
            "Price": bodystr[0].get("Price")
            })
        ch.basic_ack(delivery_tag=method.delivery_tag, multiple=False)
        
    elif (properties.headers['event'] == 'ProductDeleted'):
        delete_product(collection, {"Id" : bodystr[0].get("Id")})
        ch.basic_ack(delivery_tag=method.delivery_tag, multiple=False)
    else:
        ch.basic_reject(delivery_tag=method.delivery_tag, requeue=False)
        
channel.basic_consume(queue='cart', on_message_callback=callback)

try:
    channel.start_consuming()
except KeyboardInterrupt:
    channel.stop_consuming()
    
if (channel.is_open):
    channel.stop_consuming()
connection.close()
