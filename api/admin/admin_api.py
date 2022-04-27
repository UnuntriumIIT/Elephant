from flask import Flask, redirect, request
from flask_restful import Api, Resource
import json
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2 import Error
from psycopg2.extras import RealDictCursor
import os
import pika

app = Flask(__name__)
api = Api(app)

# Класс отвечающий за api категорий
class Category(Resource):
    
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

    # Возвращает все записи из базы данных для отображения в таблице
    def get_all_records(self):
        try:
            conn = psycopg2.connect(dbname=os.environ['DB_NAME'], 
                                    user=os.environ['DB_USER'], 
                                    password=os.environ['DB_PASS'], 
                                    host=os.environ['DB_HOST'])
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute('''
                           SELECT t.*
                           FROM public."Category_Major" t''')
            result = cursor.fetchall()
            return result
        except (Exception, Error) as error:
               print("Ошибка при работе с PostgreSQL", error)
        finally:
            if conn:
                cursor.close()
                conn.close()
                print("Соединение с PostgreSQL закрыто") 
    
    # Возвращает инфу о категории по конкретному id
    def get_record_by_id(self, id):
        try:
            conn = psycopg2.connect(dbname=os.environ['DB_NAME'], 
                                    user=os.environ['DB_USER'], 
                                    password=os.environ['DB_PASS'], 
                                    host=os.environ['DB_HOST'])
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            q = '''
                    SELECT t.*
                    FROM public."Category_Major" t
                    WHERE id = %s
                    '''
            cursor.execute(q, (id,))
            result = cursor.fetchall()
            return result
        except (Exception, Error) as error:
               print("Ошибка при работе с PostgreSQL", error)
        finally:
            if conn:
                cursor.close()
                conn.close()
                print("Соединение с PostgreSQL закрыто") 
                
    def post_new_record(self, id, name, parentId):
        try:
            conn = psycopg2.connect(dbname=os.environ['DB_NAME'], 
                                    user=os.environ['DB_USER'], 
                                    password=os.environ['DB_PASS'], 
                                    host=os.environ['DB_HOST'])
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            query = '''INSERT INTO public."Category_Major" (id, "Name", "ParentId")
                           VALUES (%s, %s, %s);'''
            cursor.execute(query, (id, name, parentId))
            body = [{"Id" : id, "Name" : name, "ParentId": parentId}]
            self.send_message('CategoryCreated', body)
        except (Exception, Error) as error:
               print("Ошибка при работе с PostgreSQL", error)
        finally:
            if conn:
                cursor.close()
                conn.close()
                print("Соединение с PostgreSQL закрыто")    
    
    def put_record_by_id(self, id, name, parentId):
        try:
            conn = psycopg2.connect(dbname=os.environ['DB_NAME'], 
                                    user=os.environ['DB_USER'], 
                                    password=os.environ['DB_PASS'], 
                                    host=os.environ['DB_HOST'])
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            q= '''
                    UPDATE public."Category_Major"
                    SET "Name" = %s, "ParentId" = %s
                    WHERE id LIKE %s ESCAPE '#';'''
            cursor.execute(q, (name, parentId, id))
            body = [{"Id" : id, "Name" : name, "ParentId": parentId}]
            self.send_message('CategoryChanged', body)
        except (Exception, Error) as error:
               print("Ошибка при работе с PostgreSQL", error)
        finally:
            if conn:
                cursor.close()
                conn.close()
                print("Соединение с PostgreSQL закрыто") 
    
    def delete_record_by_id(self, id):
        try:
            conn = psycopg2.connect(dbname=os.environ['DB_NAME'], 
                                    user=os.environ['DB_USER'], 
                                    password=os.environ['DB_PASS'], 
                                    host=os.environ['DB_HOST'])
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            q = '''
                DELETE
                FROM public."Category_Major"
                WHERE id LIKE %s ESCAPE '#';'''
            cursor.execute(q, (id, ))
            body = [{"Id" : id}]
            self.send_message('CategoryDeleted', body)
        except (Exception, Error) as error:
               print("Ошибка при работе с PostgreSQL", error)
        finally:
            if conn:
                cursor.close()
                conn.close()
                print("Соединение с PostgreSQL закрыто") 
                   
    def get(self, id=0):        
        if id == 0:
            return json.dumps(self.get_all_records()), 200
        else:
            return json.dumps(self.get_record_by_id(id)), 200
        return "Category not found with id = "+ str(id), 404
    
    def post(self, id):
        name = request.form.get('name')
        parentId = request.form.get('parcats')
        if (request.form.get('_method') == 'put'):
            if(not self.get_record_by_id(id)):
                return "Category with id %s does not exists"%(id), 400
            self.put_record_by_id(id, name, parentId)
        else:
            if(self.get_record_by_id(id)):
                return "Category with id %s already exists"%(id), 400
            self.post_new_record(id, name, parentId)
        return redirect("http://localhost/admin/categories", code=303)
  
    def delete(self, id):
        self.delete_record_by_id(id)
        return 'Success', 200
    
class Childs(Resource):
    def get_all_childs(self, id):
        try:
            conn = psycopg2.connect(dbname=os.environ['DB_NAME'], 
                                    user=os.environ['DB_USER'], 
                                    password=os.environ['DB_PASS'], 
                                    host=os.environ['DB_HOST'])
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            q = '''
                SELECT t.*
                FROM public."Category_Major" t
                WHERE "ParentId" = %s '''
            cursor.execute(q, (id, ))
            result = cursor.fetchall()
            return result
        except (Exception, Error) as error:
               print("Ошибка при работе с PostgreSQL", error)
        finally:
            if conn:
                cursor.close()
                conn.close()
                print("Соединение с PostgreSQL закрыто")

    def get(self, id=0):        
        if id != 0:
            return json.dumps(self.get_all_childs(id)), 200
        return "Category not found with id = "+ str(id), 404

class Product(Resource):
    
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
    
    def notify_cart(self, header, body):
        credentials = pika.PlainCredentials(os.environ['RABBIT_USER'], 
                                            os.environ['RABBIT_PASSWORD'])
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(os.environ['RABBIT_HOST'], 
                                      os.environ['RABBIT_PORT'], 
                                      '/', 
                                      credentials))
        
        channel = connection.channel()
        channel.queue_declare(queue=os.environ['RABBIT_CART_QUEUE'] , 
                              durable=True, 
                              exclusive=False, 
                              auto_delete=False)
        channel.confirm_delivery()
        try:
            channel.basic_publish(exchange='',
                          routing_key=os.environ['RABBIT_CART_QUEUE'],
                          body=json.dumps(body),
                          properties=pika.BasicProperties(content_type='text/plain',
                                                              delivery_mode=1,
                                                              headers={'event': header}))
            print('publish: '+header+ " " + body)        
        except pika.exceptions.UnroutableError as error:
            print(error)

    def delete_record_by_id(self, id):
        try:
            conn = psycopg2.connect(dbname=os.environ['DB_NAME'], 
                                    user=os.environ['DB_USER'], 
                                    password=os.environ['DB_PASS'], 
                                    host=os.environ['DB_HOST'])
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            q = '''
                DELETE
                FROM public."Product"
                WHERE id LIKE %s ESCAPE '#';'''
            cursor.execute(q, (id, ))
            body = [{"Id" : id}]
            self.send_message('ProductDeleted', body)
            self.notify_cart('Deleted', body)
        except (Exception, Error) as error:
               print("Ошибка при работе с PostgreSQL", error)
        finally:
            if conn:
                cursor.close()
                conn.close()
                print("Соединение с PostgreSQL закрыто") 

    def get_all_records(self):
        try:
            conn = psycopg2.connect(dbname=os.environ['DB_NAME'], 
                                    user=os.environ['DB_USER'], 
                                    password=os.environ['DB_PASS'], 
                                    host=os.environ['DB_HOST'])
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute('''
                           SELECT t.*
                           FROM public."Product" t
                           ''')
            result = cursor.fetchall()
            return result
        except (Exception, Error) as error:
               print("Ошибка при работе с PostgreSQL", error)
        finally:
            if conn:
                cursor.close()
                conn.close()
                print("Соединение с PostgreSQL закрыто") 

    def get_record_by_id(self, id):
        try:
            conn = psycopg2.connect(dbname=os.environ['DB_NAME'], 
                                    user=os.environ['DB_USER'], 
                                    password=os.environ['DB_PASS'], 
                                    host=os.environ['DB_HOST'])
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            q = '''
                           SELECT t.*
                           FROM public."Product" t
                           WHERE id = %s
                           '''
            cursor.execute(q, (id,))
            result = cursor.fetchall()
            return result
        except (Exception, Error) as error:
               print("Ошибка при работе с PostgreSQL", error)
        finally:
            if conn:
                cursor.close()
                conn.close()
                print("Соединение с PostgreSQL закрыто") 

    def post_new_record(self, id, name, image_src, price, quantity, category_id):
        try:
            conn = psycopg2.connect(dbname=os.environ['DB_NAME'], 
                                    user=os.environ['DB_USER'], 
                                    password=os.environ['DB_PASS'], 
                                    host=os.environ['DB_HOST'])
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            q = '''
                INSERT INTO public."Product" (id, name, image_src, price, quantity, category_id)
                VALUES (%s, %s, %s, %s, %s, %s);'''
            cursor.execute(q, (id, name, image_src, price, quantity, category_id))
            body = [{"Id": id, "Name": name, "Image_src": image_src, "Price": price, "Quantity": quantity, "Category_id": category_id}]
            self.send_message('ProductCreated', body)
        except (Exception, Error) as error:
               print("Ошибка при работе с PostgreSQL", error)
        finally:
            if conn:
                cursor.close()
                conn.close()
                print("Соединение с PostgreSQL закрыто")  
             
    def put_record_by_id(self, id, name, image_src, price, quantity, category_id):
        try:
            conn = psycopg2.connect(dbname=os.environ['DB_NAME'], 
                                    user=os.environ['DB_USER'], 
                                    password=os.environ['DB_PASS'], 
                                    host=os.environ['DB_HOST'])
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            q= '''
                UPDATE public."Product"
                SET
                    name        = %s,
                    image_src   = %s,
                    price       = %s,
                    quantity    = %s,
                    category_id = %s
                WHERE id LIKE %s ESCAPE '#';'''
            cursor.execute(q, (name, image_src, price, quantity, category_id, id))
            body = [{"Id": id, "Name": name, "Image_src": image_src, "Price": price, "Quantity": quantity, "Category_id": category_id}]
            self.send_message('ProductChanged', body)
            self.notify_cart('Changed', [{"Id": id, "Name": name, "Price": price}])
        except (Exception, Error) as error:
               print("Ошибка при работе с PostgreSQL", error)
        finally:
            if conn:
                cursor.close()
                conn.close()
                print("Соединение с PostgreSQL закрыто") 

    def get(self, id=0):
        if id == 0:
            return json.dumps(self.get_all_records(), default=str), 200
        else:
            return json.dumps(self.get_record_by_id(id), default=str), 200
        return "Category not found with id = "+ str(id), 404
    
    def post(self, id):

        name = request.form.get('name')
        image_src = request.form.get('image_src')
        price = request.form.get('price')
        quantity = request.form.get('quantity')
        category_id = request.form.get('cats')
        if (request.form.get('_method') == 'put'):
            if(not self.get_record_by_id(id)):
                return "Category with id %s does not exists"%(id), 400
            self.put_record_by_id(id, name, image_src, price, quantity, category_id)
        else:
            if(self.get_record_by_id(id)):
                return "Category with id %s already exists"%(id), 400
            self.post_new_record(id, name, image_src, price, quantity, category_id)
        return redirect("http://localhost/admin/catalog", code=302)
  
    def delete(self, id):
        self.delete_record_by_id(id)
        return 'Success', 200

try:
    conn = psycopg2.connect(dbname=os.environ['DB_NAME'], 
                                    user=os.environ['DB_USER'], 
                                    password=os.environ['DB_PASS'], 
                                    host=os.environ['DB_HOST'])
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()
    cursor.execute('''
                    create table if not exists "Category_Major"
                    (
                        id     text not null
                            constraint category_pk
                                primary key,
                        "Name" text not null,
                        "ParentId" text
                        );
                    alter table "Category_Major"
                        owner to postgres;''')
    cursor.execute('''
                    create table if not exists "Product"
                    (
	                    id text
		                    constraint product_pk
			                    primary key,
	                    name text not null,
	                    image_src text not null,
	                    price decimal not null,
                        quantity int default 0 not null,
	                    category_id text
                    );''')
except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
finally:
    if conn:
        cursor.close()
        conn.close()
        print("Соединение с PostgreSQL закрыто")
        
api.add_resource(Category, "/api/category", "/api/category", "/api/category/<string:id>")
api.add_resource(Childs, "/api/categorychilds/<string:id>")
api.add_resource(Product, "/api/catalog", "/api/catalog", "/api/catalog/<string:id>")
