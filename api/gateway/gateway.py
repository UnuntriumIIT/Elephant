from flask import Flask, redirect, make_response, request
import requests
import json
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2 import Error
from psycopg2.extras import RealDictCursor
import os
import jwt
import uuid;

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

@app.route('/auth/register/<login>/<passwordHash>')
def register(login, passwordHash):
    if isExistLogin(login):
        return json.dumps({"message" : "This Login is exists!"}), 409
    try:
        conn = psycopg2.connect(dbname=os.environ['DB_NAME'], 
                                user=os.environ['DB_USER'], 
                                password=os.environ['DB_PASS'], 
                                host=os.environ['DB_HOST'])
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        q = '''
                       INSERT INTO "User" VALUES (%s, %s, %s);
            '''
            
        q2 = '''
                       INSERT INTO "Role" VALUES (%s, 'U');
             '''
        user_id = uuid.uuid4()
        cursor.execute(q, (user_id, login, passwordHash))
        cursor.execute(q2, (user_id, ))
        return redirect(os.environ['FRONTEND_HOST']+'login/index', code=302)        
    except (Exception, Error) as error:
           print("Ошибка при работе с PostgreSQL", error)
    finally:
        if conn:
            cursor.close()
            conn.close()
            print("Соединение с PostgreSQL закрыто") 
    return ''
      
@app.route('/auth/login/<login>/<passwordHash>')      
def login(login, passwordHash):
    if isCorrectCredentials(login, passwordHash):
        payload = {"id": '\"'+getIdByLogin(login)+'\"', "login" : '\"'+login+'\"', "role" : '\"'+getRoleByLogin(login)+'\"'}
        jwtForUser = jwt.encode(payload, signing_key, algorithm="HS256")
        response = make_response(redirect(os.environ['FRONTEND_HOST']))
        response.set_cookie('auth', jwtForUser)
        return response
    return redirect(os.environ['FRONTEND_HOST']+'login/index')

@app.route('/auth/logout')
def logout():
    response = make_response(redirect(os.environ['FRONTEND_HOST']))
    response.set_cookie('auth', '', expires=0)
    return response

@app.route('/api/<direction>/<endpoint>/<parameter>')
def handleRequest(direction, endpoint, parameter):
    jwt_token = request.cookies.get('auth')
    payload = jwt.decode(jwt_token, signing_key, algorithms=["HS256"])
    if payload.get('role') == 'A':
        if direction == 'admin':
            resp = handleAdmin(endpoint, parameter)
            return resp
        return 'Forbidden', 403
    
    if payload.get('role') == 'U':
        if direction == 'admin':
            return 'Forbidden', 403
    
    if direction == 'user':
        resp = handleUser(endpoint, parameter)
        return resp
        

def handleAdmin(endpoint, parameter):
    host = os.environ['API_ADMIN_HOST']    
    return requests.get(host+endpoint+'/'+parameter).content

def handleUser(endpoint, parameter):
    host = os.environ['API_CATALOG_HOST']
    return requests.get(host+endpoint+'/'+parameter).content

def isCorrectCredentials(login, password):
    try:
        conn = psycopg2.connect(dbname=os.environ['DB_NAME'], 
                                user=os.environ['DB_USER'], 
                                password=os.environ['DB_PASS'], 
                                host=os.environ['DB_HOST'])
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        q = '''
                       SELECT *
                       FROM public."User" u
                       WHERE u."Login" = %s AND u."PasswordHash" = %s;
            '''
        cursor.execute(q, (login, password))
        result = cursor.fetchall()
        if len(result) == 1:
            return True
        return False
    except (Exception, Error) as error:
           print("Ошибка при работе с PostgreSQL", error)
    finally:
        if conn:
            cursor.close()
            conn.close()
            print("Соединение с PostgreSQL закрыто") 

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
                       FROM public."Role" r JOIN public."User" u ON r."UserID" = u."Id"
                       WHERE u."Login" = %s
            '''
        cursor.execute(q, (login,))
        result = cursor.fetchall()
        if result.get("RoleValue") == "A":
            return True
        return False
    except (Exception, Error) as error:
           print("Ошибка при работе с PostgreSQL", error)
    finally:
        if conn:
            cursor.close()
            conn.close()
            print("Соединение с PostgreSQL закрыто") 

def isExistLogin(login):
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
                       "Login" = %s;
            '''
        cursor.execute(q, (login, ))
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

def getRoleByLogin(login):
    try:
        conn = psycopg2.connect(dbname=os.environ['DB_NAME'], 
                                user=os.environ['DB_USER'], 
                                password=os.environ['DB_PASS'], 
                                host=os.environ['DB_HOST'])
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        q = '''
                       SELECT r."RoleValue"
                       FROM public."Role" r JOIN public."User" u ON r."UserID" = u."Id"
                       WHERE u."Login" = %s
            '''
        cursor.execute(q, (login,))
        result = cursor.fetchall()
        return result.get("RoleValue")
    except (Exception, Error) as error:
           print("Ошибка при работе с PostgreSQL", error)
    finally:
        if conn:
            cursor.close()
            conn.close()
            print("Соединение с PostgreSQL закрыто") 

def getIdByLogin(login):
    try:
        conn = psycopg2.connect(dbname=os.environ['DB_NAME'], 
                                user=os.environ['DB_USER'], 
                                password=os.environ['DB_PASS'], 
                                host=os.environ['DB_HOST'])
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        q = '''
                       SELECT u."Id"
                       FROM public."User" u
                       WHERE u."Login" = %s
            '''
        cursor.execute(q, (login,))
        result = cursor.fetchall()
        return result.get("Id")
    except (Exception, Error) as error:
           print("Ошибка при работе с PostgreSQL", error)
    finally:
        if conn:
            cursor.close()
            conn.close()
            print("Соединение с PostgreSQL закрыто")
