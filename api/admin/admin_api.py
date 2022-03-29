from flask import Flask
from flask_restful import Api, Resource, reqparse
import json
app = Flask(__name__)
api = Api(app)
ai_quotes = [
    {
        "id": 0,
        "name": "Kevin Kelly",
        "quantity": "47"
    },
    {
        "id": 1,
        "name": "Stephen Hawking",
        "quantity": "99"
    },
    {
        "id": 2,
        "name": "Claude Shannon",
        "quantity": "48"
    },
    {
        "id": 3,
        "name": "Elon Musk",
        "quantity": "11"
    },
    {
        "id": 4,
        "name": "Geoffrey Hinton",
        "quantity": "66"
    },
    {
        "id": 5,
        "name": "Pedro Domingos",
        "quantity": "51"
    },
    {
        "id": 6,
        "name": "Alan Turing",
        "quantity": "23"
    },
    {
        "id": 7,
        "name": "Ray Kurzweil",
        "quantity": "9"
    },
    {
        "id": 8,
        "name": "Sebastian Thrun",
        "quantity": "31"
    },
    {
        "id": 9,
        "name": "Andrew Ng",
        "quantity": "74"
    }
]

class Category(Resource):
    def get(self, id=0):
        global ai_quotes
        if id == 0:
            return ai_quotes, 200
        for quote in ai_quotes:
            if(quote["id"] == id):
                return quote, 200
        return "Category not found with id = "+ str(id), 404
    
    def post(self, id):
        global ai_quotes
        parser = reqparse.RequestParser()
        parser.add_argument("name")
        parser.add_argument("quantity")
        params = parser.parse_args()
        for quote in ai_quotes:
            if(id == quote["id"]):
                return f"Category with id {id} already exists", 400
        quote = {
            "id": int(id),
            "name": params["name"],
            "quantity": params["quantity"]
        }
        ai_quotes.append(quote)
        return quote, 201
  
    def put(self, id):
        global ai_quotes
        parser = reqparse.RequestParser()
        parser.add_argument("name")
        parser.add_argument("quantity")
        params = parser.parse_args()
        for quote in ai_quotes:
            if(id == quote["id"]):
                quote["name"] = params["name"]
                quote["quantity"] = params["quantity"]
                return quote, 200
        
        quote = {
            "id": id,
            "name": params["name"],
            "quantity": params["quantity"]
        }
        
        ai_quotes.append(quote)
        return quote, 201
  
    def delete(self, id):
        global ai_quotes
        ai_quotes = [qoute for qoute in ai_quotes if qoute["id"] != id]
        return f"Category with id {id} is deleted.", 200

api.add_resource(Category, "/api/category", "/api/category", "/api/category/<int:id>")
if __name__ == '__main__':
    app.run(debug=True)