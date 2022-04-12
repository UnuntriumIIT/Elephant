from flask import Flask
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

class Products(Resource):
    
    def get(self, id=0): 
        return "Not Implemented", 200
    
api.add_resource(Products, "/api/catalog/products", "/api/catalog/products", "/api/catalog/products/<string:id>")