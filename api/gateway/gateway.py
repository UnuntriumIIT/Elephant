from flask import Flask, redirect, request
import json
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2 import Error
from psycopg2.extras import RealDictCursor
import os
import jwt

app = Flask(__name__)

signing_key = os.environ['SECRET']

def initDB():
    try:
        conn = psycopg2.connect(dbname=os.environ['DB_NAME'], 
                                        user=os.environ['DB_USER'], 
                                        password=os.environ['DB_PASS'], 
                                        host=os.environ['DB_HOST'])
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        cursor.execute('''
                        create table if not exists "User"
                        (
                            "Id" text not null PRIMARY KEY,
                            "Login" text not null UNIQUE,
                            "PasswordHash" text not null
                        );''')
        cursor.execute('''
                        create table if not exists "Role"
                        (
    	                    "UserID" text not null,
    	                    "RoleValue" text not null
                        );''')
    except (Exception, Error) as error:
            print("Ошибка при работе с PostgreSQL", error)
    finally:
        if conn:
            cursor.close()
            conn.close()
            print("Соединение с PostgreSQL закрыто")
            
def login(login, passwordHash):
    return ''

def register(login, passwordHash):
    return ''

def logout():
    return ''

def handleRequest():
    return ''

def handleAdmin():
    return ''

def handleUser():
    return ''

def isAdminRole(login):
    try:
        conn = psycopg2.connect(dbname=os.environ['DB_NAME'], 
                                user=os.environ['DB_USER'], 
                                password=os.environ['DB_PASS'], 
                                host=os.environ['DB_HOST'])
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        q = '''
                       SELECT r."RoleValue"
                       FROM Role r JOIN User u ON r."UserID" = u."Id"
                       WHERE u."Login" = %s
            '''
        cursor.execute(q, (login,))
        result = cursor.fetchall()
        
    except (Exception, Error) as error:
           print("Ошибка при работе с PostgreSQL", error)
    finally:
        if conn:
            cursor.close()
            conn.close()
            print("Соединение с PostgreSQL закрыто") 

def isExistCredentialsPair(login, passwordHash):
    try:
        conn = psycopg2.connect(dbname=os.environ['DB_NAME'], 
                                user=os.environ['DB_USER'], 
                                password=os.environ['DB_PASS'], 
                                host=os.environ['DB_HOST'])
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        q = '''
                       SELECT *
                       FROM public."User"
                       WHERE 
                       "Login" = %s AND "PasswordHash" = %s
            '''
        cursor.execute(q, (login, passwordHash))
        result = cursor.fetchall()
        if len(result) > 0:
            return True
        return False
    except (Exception, Error) as error:
           print("Ошибка при работе с PostgreSQL", error)
    finally:
        if conn:
            cursor.close()
            conn.close()
            print("Соединение с PostgreSQL закрыто") 
