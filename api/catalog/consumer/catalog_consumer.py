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
    collection_union = dbname["union"]
    collection_product = dbname["product"]
    jsonString = {}
    
    if (properties.headers['event'] == 'CategoryCreated'):
        jsonString = {"Id" : bodystr[0].get("Id"),
                      "Name" : bodystr[0].get("Name"),
                      "ChildCategories" : [],
                      "Products" : []}
        
        collection_category.insert_one(bodystr[0])
        collection_union.insert_one(jsonString)
        
        parent = collection_union.find_one({"Id" : bodystr[0].get("ParentId")}, {'_id': False})
        if (parent):
            del bodystr[0]['_id']
            parent.get("ChildCategories").append(bodystr[0])
            collection_union.replace_one({"Id" : bodystr[0].get("ParentId")}, parent)
        
    elif (properties.headers['event'] == 'CategoryChanged'):
        chcats = collection_category.find({"ParentId" : "'"+bodystr[0].get("Id")+"'"}, {'_id': False})
        prdcts = collection_product.find({"Category_id": "'"+bodystr[0].get("Id")+"'"}, {'_id': False})                               
        jsonString = {"Id" : bodystr[0].get("Id"),
                      "Name" : bodystr[0].get("Name"),
                      "ChildCategories" : list(chcats),
                      "Products" : list(prdcts)}
        collection_category.replace_one({"Id" : bodystr[0].get("Id")}, bodystr[0])
        collection_union.replace_one({"Id" : bodystr[0].get("Id")}, jsonString)
        
        parent = collection_union.find_one({"Id" : bodystr[0].get("ParentId")}, {'_id': False})
        if (parent):
            for old in list(collection_union.find({}, {'_id': False})):
                for cat in old.get("ChildCategories"):
                    if cat.get("Id") == bodystr[0].get("Id"):
                        old.get("ChildCategories").remove(cat)
                        upd = old
                        collection_union.replace_one({"Id" : upd.get("Id")}, upd)
            parent.get("ChildCategories").append(bodystr[0])
            collection_union.replace_one({"Id" : bodystr[0].get("ParentId")}, parent)
        
        
    elif (properties.headers['event'] == 'CategoryDeleted'):
        for old in list(collection_union.find({}, {'_id': False})):
                for cat in old.get("ChildCategories"):
                    if cat.get("Id") == bodystr[0].get("Id"):
                        old.get("ChildCategories").remove(cat)
                        upd = old
                        collection_union.replace_one({"Id" : upd.get("Id")}, upd)
        collection_union.delete_many(bodystr[0])
        collection_category.delete_many(bodystr[0])
        
    elif (properties.headers['event'] == 'ProductCreated'):
        if bodystr[0].get("Category_id") != 'NULL':
            union = collection_union.find_one({"Id" : bodystr[0].get("Category_id")}, {'_id': False})
            union.get("Products").append(bodystr[0])
            collection_union.replace_one({"Id" : union.get("Id")}, union)
        else:
            jsonString = {"Id" : 'NULL',
                      "Name" : 'NULL',
                      "ParentId" : 'NULL'}
            collection_category.insert_one(jsonString)
            js = {"Id" : 'NULL',
                  "Name" : 'NULL',
                  "ChildCategories" : [],
                  "Products" : [ bodystr[0] ]
                }
            collection_union.insert_one(js)
        collection_product.insert_one(bodystr[0])
        
    elif (properties.headers['event'] == 'ProductChanged'):
        
        oldcat = collection_product.find_one({"Id": bodystr[0].get("Id")},{'_id': False}).get("Category_id")
        
        if bodystr[0].get("Category_id") == oldcat:
            if bodystr[0].get("Category_id") != 'NULL':
                union = collection_union.find_one({"Id" : bodystr[0].get("Category_id")}, {'_id': False})
                for p in union.get("Products"):
                    if p.get("Id") == bodystr[0].get("Id"):
                        union.get("Products").remove(p)
                        union.get("Products").append(bodystr[0])
                        collection_union.replace_one({"Id" : union.get("Id")}, union)
            else:
                union = collection_union.find({"Id" : 'NULL'})
                for u in list(union):
                    for p in u.get("Products"):
                        if p.get("Id") == bodystr[0].get("Id"):
                            u.get("Products").remove(p)
                            u.get("Products").append(bodystr[0])
                            collection_union.replace_one({"_id" : u.get("_id")}, u)
        else:
            if oldcat == 'NULL':
                union = collection_union.find({"Id" : oldcat})
                for u in list(union):
                    for p in u.get("Products"):
                        if p.get("Id") == bodystr[0].get("Id"):
                            collection_union.delete_one({"_id": u.get("_id")})
                            if (list(collection_union.find({"Id":"NULL"})).count() < 1):
                                collection_category.delete_many({"Id": "NULL"})
                union = collection_union.find_one({"Id" : bodystr[0].get("Category_id")}, {'_id': False})
                union.get("Products").append(bodystr[0])
                collection_union.replace_one({"Id" : union.get("Id")}, union)
            else:
                if bodystr[0].get("Category_id") == 'NULL':
                    union = collection_union.find_one({"Id" : oldcat}, {'_id': False})
                    for p in union.get("Products"):
                        if p.get("Id") == bodystr[0].get("Id") :
                            union.get("Products").remove(p)
                            collection_union.replace_one({"Id" : union.get("Id")}, union)
                    js = {"Id" : 'NULL',
                      "Name" : 'NULL',
                      "ChildCategories" : [],
                      "Products" : [ bodystr[0] ]
                    }
                    collection_union.insert_one(js)
                    jsonString = {"Id" : 'NULL',
                      "Name" : 'NULL',
                      "ParentId" : 'NULL'}
                    collection_category.insert_one(jsonString)
                else:
                    union = collection_union.find_one({"Id" : oldcat}, {'_id': False})
                    for p in union.get("Products"):
                        if p.get("Id") == bodystr[0].get("Id") :
                            union.get("Products").remove(p)
                            collection_union.replace_one({"Id" : union.get("Id")}, union)
                    union = collection_union.find_one({"Id" : bodystr[0].get("Category_id")}, {'_id': False})
                    union.get("Products").append(bodystr[0])
                    collection_union.replace_one({"Id" : union.get("Id")}, union)
        collection_product.replace_one({"Id" : bodystr[0].get("Id")}, bodystr[0])
        
    elif (properties.headers['event'] == 'ProductDeleted'):
        catid = collection_product.find_one({"Id": bodystr[0].get("Id")},{'_id': False}).get("Category_id")
        if catid != 'NULL':
            union = collection_union.find_one({"Id" : catid}, {'_id': False})
            for p in union.get("Products"):
                if p.get("Id") == bodystr[0].get("Id") :
                    union.get("Products").remove(p)
                    collection_union.replace_one({"Id" : union.get("Id")}, union)
        else:
            union = collection_union.find({"Id" : catid})   
            for u in list(union):
                for p in u.get("Products"):
                    if p.get("Id") == bodystr[0].get("Id"):
                        collection_union.delete_one({"_id": u.get("_id")})
                        if (list(collection_union.find({"Id":"NULL"})).count() < 1):
                                collection_category.delete_many({"Id": "NULL"})
        collection_product.delete_many({"Id":bodystr[0].get("Id")})
                        
                    
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
