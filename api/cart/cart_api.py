from flask import Flask, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import requests
import json
import os
import jwt
import logging

app = Flask(__name__)
api = Api(app)

class Cart(Resource):            
    admin_api_host = os.environ['ADMIN_API']
    signing_key = os.environ['SECRET']
    
    def getCollection(self):
        CONNECTION_STRING = os.environ['MONGO_CONN_STR']
        client = MongoClient(CONNECTION_STRING)
        db = client['elephant_cart']
        return db["cart"]
    
    def getUserId(self, cookie_auth):
        jwt_token = str.encode(cookie_auth)
        payload = jwt.decode(jwt_token, self.signing_key, algorithms=["HS256"])
        return payload.get('id')
    
    def getProductFromAdmin(self, product_id):
        return requests.get(self.admin_api_host + 'api/catalog/'+product_id).content
    
    def get(self):
        user_id = self.getUserId(request.headers['Authorization'])
        coll = self.getCollection()
        logging.warning(json.dumps(coll.find_one({"User_Id": user_id}, {'_id': False})))
        return coll.find_one({"User_Id": user_id}, {'_id': False})
    
    def post(self, product_id):
        user_id = self.getUserId(request.headers['Authorization'])
        product = json.loads(json.loads(self.getProductFromAdmin(product_id)))[0]
        logging.warning(str(product))
        cart = self.getCollection()
        user_cart = cart.find_one({"User_Id": user_id}, {'_id': False})
        if not user_cart:
            json_str = {
                "User_Id" : user_id,
                "Total" : product.get('price'),
                "Products": [
                    { 
                        "Id" : product.get('id'),
                        "Name" : product.get('name'),
                        "Price" : product.get('price'),
                        "Quantity_in_cart" : 1,
                        },
                    ],
                }
            cart.insert_one(json_str)
        else:
            flag = False
            for i in user_cart.get('Products'):
                if i.get('Id') == product.get('id'):
                    flag = True
                    i['Quantity_in_cart'] += 1
                    user_cart['Total'] = str(float(user_cart['Total']) + float(i.get('Price')))
                    break
            if not flag:
                json_pr = { 
                        "Id" : product.get('id'),
                        "Name" : product.get('name'),
                        "Price" : product.get('price'),
                        "Quantity_in_cart" : 1,
                    }
                user_cart.get('Products').append(json_pr)
                user_cart['Total'] = str(float(user_cart['Total']) + float(product.get('price')))
            
            cart.replace_one({"User_Id" : user_id}, user_cart)
        return ""
    
    def delete(self, product_id):
        user_id = self.getUserId(request.headers['Authorization'])
        cart = self.getCollection()
        deleteall = request.args.get('deleteall')
        user_cart = cart.find_one({"User_Id" : user_id}, {'_id': False})
        if (deleteall == 'Y'):
            for i in user_cart.get('Products'):
                if i.get('Id') == product_id:
                    user_cart['Total'] = float(user_cart['Total']) - (float(i.get('Price'))*int(i.get('Quantity_in_cart')))
                    user_cart.get('Products').remove(i)
                    if len(user_cart.get('Products')) == 0:
                       cart.delete_one({"User_Id" : user_id})
                    else:
                       cart.replace_one({"User_Id" : user_id}, user_cart) 
                    break
        else:
            for i in user_cart.get('Products'):
                if i.get('Id') == product_id:
                    if i.get("Quantity_in_cart") == 1:
                        user_cart.get('Products').remove(i)
                    else:
                        i["Quantity_in_cart"] -= 1
                    user_cart['Total'] = str(float(user_cart['Total']) - float(i.get('Price')))
                    if len(user_cart.get('Products')) == 0:
                       cart.delete_one({"User_Id" : user_id})
                    else:
                       cart.replace_one({"User_Id" : user_id}, user_cart) 
                    break
            
        return ""

api.add_resource(Cart, "/api/cart", "/api/cart", "/api/cart/<string:product_id>")
