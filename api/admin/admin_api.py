from flask import Flask, redirect, request
from flask_restful import Api, Resource
import json
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2 import Error
from psycopg2.extras import RealDictCursor
import os

app = Flask(__name__)
api = Api(app)

# Класс отвечающий за api категорий
class Category(Resource):

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
            cursor.execute('''
                           SELECT t.*
                           FROM public."Category_Major" t
                           WHERE id = '%s'
                           '''%(id))
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
            cursor.execute('''
                           INSERT INTO public."Category_Major" (id, "Name", "ParentId")
                           VALUES ('%s'::text, '%s'::text, %s);'''%(id, name, parentId))
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
            cursor.execute('''
                           UPDATE public."Category_Major"
                           SET "Name" = '%s'::text, "ParentId" = %s
                           WHERE id LIKE '%s' ESCAPE '#';'''%(name, parentId, id))
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
            cursor.execute('''
                           DELETE
                           FROM public."Category_Major"
                           WHERE id LIKE '%s' ESCAPE '#';'''%(id))
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
        if (parentId != 'NULL'):
                parentId = "'"+ parentId +"'"
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
            cursor.execute('''
                           SELECT t.*
                           FROM public."Category_Major" t
                           WHERE "ParentId" = '%s' '''%(id))
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

    def delete_record_by_id(self, id):
        try:
            conn = psycopg2.connect(dbname=os.environ['DB_NAME'], 
                                    user=os.environ['DB_USER'], 
                                    password=os.environ['DB_PASS'], 
                                    host=os.environ['DB_HOST'])
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute('''
                           DELETE
                           FROM public."Product"
                           WHERE id LIKE '%s' ESCAPE '#';'''%(id))
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
            cursor.execute('''
                           SELECT t.*
                           FROM public."Product" t
                           WHERE id = '%s'
                           '''%(id))
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
            cursor.execute('''
                            INSERT INTO public."Product" (id, name, image_src, price, quantity, category_id)
                            VALUES ('%s'::text, '%s'::text, '%s'::text, %s::numeric, %s::integer, %s);'''%(id, name, image_src, price, quantity, category_id))
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
            cursor.execute('''
                            UPDATE public."Product"
                            SET
                                name        = '%s'::text,
                                image_src   = '%s'::text,
                                price       = %s::numeric,
                                quantity    = %s::integer,
                                category_id = %s
                            WHERE id LIKE '%s' ESCAPE '#';'''%(name, image_src, price, quantity, category_id, id))
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
        if (category_id != 'NULL'):
                category_id = "'"+ category_id +"'"
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
		                    constraint product_category_id_fk
			                    references "Category_Major"
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
