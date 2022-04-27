from flask import Flask, redirect, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import requests
import json
import os
import jwt

app = Flask(__name__)
api = Api(app)

class Cart(Resource):            
    admin_api_host = os.environ['ADMIN_API']
    signing_key = os.environ['SECRET']
    
    def getCollection(self):
        CONNECTION_STRING = os.environ['MONGO_CONN_STR']
        client = MongoClient(CONNECTION_STRING)
        return client['elephant_cart']["cart"]
    
    def getUserId(self, cookie_auth):
        jwt_token = str.encode(cookie_auth)
        payload = jwt.decode(jwt_token, self.signing_key, algorithms=["HS256"])
        return payload.get('id')
    
    def getProductFromAdmin(self, product_id):
        return requests.get(self.admin_api_host + 'api/catalog/'+product_id).content
    
    def get(self):
        user_id = self.getUserId(request.headers['Authorization'])
        coll = self.getCollection()
        return json.dumps(coll.find_one({"User_Id": user_id}, {'_id': False}))
    
    def post(self, product_id):
        user_id = self.getUserId(request.headers['Authorization'])
        product = self.getProductFromAdmin(product_id)
        cart = self.getCollection()
        user_cart = cart.find_one({"User_Id": user_id}, {'_id': False})
        if len(user_cart) < 1:
            json_str = {
                "User_Id" : user_id,
                "Total" : product.get('Price'),
                "Products": [
                    { 
                        "Id" : product.get('Id'),
                        "Name" : product.get('Name'),
                        "Price" : product.get('Price'),
                        "Quantity_in_cart" : 1,
                        },
                    ],
                }
            cart.insert_one(json_str)
        else:
            flag = False
            for i in user_cart.get('Products'):
                if i.get('Id') == product.get('Id'):
                    flag = True
                    i['Quantity_in_cart'] += 1
                    user_cart['Total'] += i.get('Price')
                    break
            if not flag:
                json_pr = { 
                        "Id" : product.get('Id'),
                        "Name" : product.get('Name'),
                        "Price" : product.get('Price'),
                        "Quantity_in_cart" : 1,
                    }
                user_cart.get('Products').append(json_pr)
                user_cart['Total'] += product.get('Price')
            
            cart.replace_one({"User_Id" : user_id}, user_cart)
        return redirect("http://localhost/cart", code=302)
    
    def delete(self, product_id):
        user_id = self.getUserId(request.headers['Authorization'])
        cart = self.getCollection()
        user_cart = cart.find_one({"User_Id" : user_id}, {'_id': False})
        for i in user_cart.get('Products'):
            if i.get('Id') == product_id:
                if i.get("Quantity_in_cart") == 1:
                    user_cart.get('Products').remove(i)
                else:
                    i["Quantity_in_cart"] -= 1
                user_cart['Total'] -= i.get('Price')
                if len(user_cart.get('Products')) == 0:
                   cart.delete_one({"User_Id" : user_id})
                else:
                   cart.replace_one({"User_Id" : user_id}, user_cart) 
                break
            
        return redirect("http://localhost/cart", code=302)

api.add_resource(Cart, "/api/cart", "/api/cart", "/api/cart/<string:id>")
