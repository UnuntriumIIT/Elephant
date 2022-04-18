from flask import Flask
from flask_restful import Api, Resource
from pymongo import MongoClient
import os
import json

app = Flask(__name__)
api = Api(app)

class Products(Resource):
    
    def getDatabase(self):
        CONNECTION_STRING = os.environ['MONGO_CONN_STR']
        client = MongoClient(CONNECTION_STRING)
        return client['elephant']
    
    def findDataAsTrueJSON(self, id):
        dbname = self.getDatabase()
        collection_union = dbname["union"]
        return collection_union.find_one({"Id": id}, {'_id': False})
    
    def get(self, id=0): 
        if (id == 0):
            return "Not Found", 404
        return json.dumps(self.findDataAsTrueJSON(id)), 200
    
class Categories(Resource):
    
    def getDatabase(self):
        CONNECTION_STRING = os.environ['MONGO_CONN_STR']
        client = MongoClient(CONNECTION_STRING)
        return client['elephant']
    
    def findDataAsTrueJSON(self):
        dbname = self.getDatabase()
        collection_category = dbname["category"]
        return list(collection_category.find({}, {'_id': False}))
    
    def get(self): 
        return json.dumps(self.findDataAsTrueJSON()), 200
    
api.add_resource(Products, "/api/catalog/products/<string:id>")
api.add_resource(Categories, "/api/catalog/categories")
