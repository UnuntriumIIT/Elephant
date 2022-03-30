from flask import Flask, redirect, request
from flask_restful import Api, Resource
import json
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2 import Error
from psycopg2.extras import RealDictCursor

app = Flask(__name__)
api = Api(app)

# Класс отвечающий за api категорий
class Category(Resource):
    
    # Возвращает все записи из базы данных для отображения в таблице
    def get_all_records(self):
        try:
            conn = psycopg2.connect(dbname='elephant', user='postgres', password='admin', host='postgres')
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute('''
                           SELECT t.*
                           FROM public."Category" t
                           ''')
            result = cursor.fetchall()
            print(result)
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
            conn = psycopg2.connect(dbname='elephant', user='postgres', password='admin', host='postgres')
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute('''
                           SELECT t.*
                           FROM public."Category" t
                           WHERE id = '%s'
                           '''%(id))
            result = cursor.fetchall()
            print(result)
            return result
        except (Exception, Error) as error:
               print("Ошибка при работе с PostgreSQL", error)
        finally:
            if conn:
                cursor.close()
                conn.close()
                print("Соединение с PostgreSQL закрыто") 
                
    def post_new_record(self, id, name):
        try:
            conn = psycopg2.connect(dbname='elephant', user='postgres', password='admin', host='postgres')
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute('''
                           INSERT INTO public."Category" (id, "Name")
                           VALUES ('%s'::text, '%s'::text);'''%(id, name))
        except (Exception, Error) as error:
               print("Ошибка при работе с PostgreSQL", error)
        finally:
            if conn:
                cursor.close()
                conn.close()
                print("Соединение с PostgreSQL закрыто")    
    
    def put_record_by_id(self, id, name):
        try:
            conn = psycopg2.connect(dbname='elephant', user='postgres', password='admin', host='postgres')
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute('''
                           UPDATE public."Category"
                           SET "Name" = '%s'::text
                           WHERE id LIKE '%s' ESCAPE '#';'''%(name, id))
        except (Exception, Error) as error:
               print("Ошибка при работе с PostgreSQL", error)
        finally:
            if conn:
                cursor.close()
                conn.close()
                print("Соединение с PostgreSQL закрыто") 
    
    def delete_record_by_id(self, id):
        try:
            conn = psycopg2.connect(dbname='elephant', user='postgres', password='admin', host='postgres')
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute('''
                           DELETE
                           FROM public."Category"
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
    
    def put(self, id):
        name = request.form.get('name')
        if(not self.get_record_by_id(id)):
            return "Category with id %s does not exists"%(id), 400
        self.put_record_by_id(id, name)
        return redirect("http://localhost/admin/categories"), 200 
    
    def post(self, id):
        if (request.form.get('_method') == 'put'):
            self.put(id)
        else:
            name = request.form.get('name')
            if(self.get_record_by_id(id)):
                return "Category with id %s already exists"%(id), 400
            self.post_new_record(id, name)
        return redirect("http://localhost/admin/categories"), 200
  
    def delete(self, id):
        self.delete_record_by_id(id)
        return redirect("http://localhost/admin/categories"), 200

api.add_resource(Category, "/api/category", "/api/category", "/api/category/<string:id>")
if __name__ == '__main__':
    app.run(debug=True)