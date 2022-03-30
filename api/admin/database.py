import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2 import Error
import uuid
import random
import string

def init_database():
    try:
        conn = psycopg2.connect(dbname='elephant', user='postgres', password='admin', host='localhost')
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        cursor.execute('''
                       create table if not exists "Category"
                       (
                           id     text not null
                               constraint category_pk
                                   primary key,
                           "Name" text not null
                           );
                       alter table "Category"
                           owner to postgres;''')
    except (Exception, Error) as error:
           print("Ошибка при работе с PostgreSQL", error)
    finally:
        if conn:
            cursor.close()
            conn.close()
            print("Соединение с PostgreSQL закрыто")
            
def insert_test_value():
    try:
        conn = psycopg2.connect(dbname='elephant', user='postgres', password='admin', host='localhost')
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        u = uuid.uuid4()
        n = random.choice(string.ascii_lowercase)
        cursor.execute('''
                       INSERT INTO public."Category" (id, "Name")
                       VALUES ('%s'::text, '%s'::text);'''%(u, n))
    except (Exception, Error) as error:
           print("Ошибка при работе с PostgreSQL", error)
    finally:
        if conn:
            cursor.close()
            conn.close()
            print("Соединение с PostgreSQL закрыто")
            
            
def get_all_records():
        try:
            conn = psycopg2.connect(dbname='elephant', user='postgres', password='admin', host='localhost')
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cursor = conn.cursor()
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

insert_test_value()
insert_test_value()
insert_test_value()
insert_test_value()
insert_test_value()
insert_test_value()
insert_test_value()
insert_test_value()
insert_test_value()
insert_test_value()