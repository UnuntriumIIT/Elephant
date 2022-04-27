from flask import Flask, redirect, make_response, request
import requests
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2 import Error
from psycopg2.extras import RealDictCursor
import os
import jwt
import uuid;
import logging

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
initDB()
@app.route('/auth/register', methods=['POST'])
def register():
    login = request.form.get('login')
    passwordHash = request.form.get('password1')
    if isExistLogin(login):
        return redirect(os.environ['FRONTEND_HOST']+'login/registration')
    try:
        conn = psycopg2.connect(dbname=os.environ['DB_NAME'], 
                                user=os.environ['DB_USER'], 
                                password=os.environ['DB_PASS'], 
                                host=os.environ['DB_HOST'])
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        q = '''
                       INSERT INTO public."User" VALUES (%s, %s, %s);
            '''
            
        q2 = '''
                       INSERT INTO public."Role" VALUES (%s, 'U');
             '''
        user_id = str(uuid.uuid4())
        cursor.execute(q, (user_id, login, passwordHash))
        cursor.execute(q2, (user_id, ))
        return redirect(os.environ['FRONTEND_HOST']+'login/index')        
    except (Exception, Error) as error:
           logging.warning("Ошибка при работе с PostgreSQL " + str(error))
           return redirect(os.environ['FRONTEND_HOST']+'login/registration')
    finally:
        if conn:
            cursor.close()
            conn.close()
            print("Соединение с PostgreSQL закрыто") 
      
@app.route('/auth/login', methods=['POST'])      
def login():
    login = request.form.get('login')
    passwordHash = request.form.get('password1')
    if isCorrectCredentials(login, passwordHash):
        logging.warning('login: '+login+', role: '+str(getRoleByLogin(login))+', id: '+ str(getIdByLogin(login)))
        payload = {"id": getIdByLogin(login), "login" : login, "role" : getRoleByLogin(login)}
        jwtForUser = jwt.encode(payload, signing_key, algorithm="HS256")
        response = make_response(redirect(os.environ['FRONTEND_HOST']))
        response.set_cookie('auth', jwtForUser)
        response.headers['location'] = os.environ['FRONTEND_HOST']
        return response
    return redirect(os.environ['FRONTEND_HOST']+'login/index')

@app.route('/auth/logout')
def logout():
    response = make_response(redirect(os.environ['FRONTEND_HOST']))
    response.set_cookie('auth', '', expires=0)
    response.headers['location'] = os.environ['FRONTEND_HOST']
    return response

@app.route('/api/<direction>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def handleRequest(direction):
    endpoint = request.args.get('endpoint')
    parameter = request.args.get('parameter')
    other_parameter = request.args.get('other_parameter')
    cookie_auth = request.args.get('token')
    logging.warning(cookie_auth)
    method = request.method
    role = 'U'
    if cookie_auth:
        jwt_token = str.encode(cookie_auth)
        payload = jwt.decode(jwt_token, signing_key, algorithms=["HS256"])
        logging.warning(payload)
        role = payload.get('role')
    
    if role == 'A':
        if direction == 'admin':
            resp = handleAdmin(endpoint, parameter, method)
            return resp
        return redirect(os.environ['FRONTEND_HOST']+'error/not_found')
    
    if role == 'U':
        if direction == 'admin':
            return redirect(os.environ['FRONTEND_HOST']+'error/forbidden')
    
    if direction == 'user':
        resp = handleUser(endpoint, parameter, other_parameter)
        return resp
    
    if direction == 'cart' and cookie_auth:
        resp = handleCart(parameter, method, cookie_auth)
        return resp
        

def handleAdmin(endpoint, parameter, method):
    host = os.environ['API_ADMIN_HOST']
    if method == 'GET':    
        if endpoint and parameter:
            return requests.get(host+'api/'+endpoint+'/'+parameter).content
        elif endpoint and not parameter:
            return requests.get(host+'api/'+endpoint).content
    elif method == 'POST':
        if endpoint and parameter:
            return requests.post(host+'api/'+endpoint+'/'+parameter).content
        elif endpoint and not parameter:
            return requests.post(host+'api/'+endpoint).content
    elif method == 'PUT':
        if endpoint and parameter:
            return requests.put(host+'api/'+endpoint+'/'+parameter).content
        elif endpoint and not parameter:
            return requests.put(host+'api/'+endpoint).content
    elif method == 'DELETE':
        if endpoint and parameter:
            return requests.delete(host+'api/'+endpoint+'/'+parameter).content
        elif endpoint and not parameter:
            return requests.delete(host+'api/'+endpoint).content

def handleUser(endpoint, parameter, other_parameter):
    host = os.environ['API_CATALOG_HOST']
    if endpoint and parameter and other_parameter:
        return requests.get(host+'api/'+endpoint+'/'+parameter+'/'+other_parameter).content
    elif endpoint and parameter and not other_parameter:
        return requests.get(host+'api/'+endpoint+'/'+parameter).content
    
def handleCart(parameter, method, cookie_auth):
    host = os.environ['API_CART_HOST']
    if method == 'GET':
        return requests.get(host+'api/cart', headers={'Authorization': cookie_auth}).content
    elif method == 'POST':
        return requests.post(host+'api/cart/'+parameter, headers={'Authorization': cookie_auth}).content
    elif method == 'DELETE':
        return requests.delete(host+'api/cart/'+parameter, headers={'Authorization': cookie_auth}).content
    
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
        return result[0].get('RoleValue')
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
        return result[0].get('Id')
    except (Exception, Error) as error:
           print("Ошибка при работе с PostgreSQL", error)
    finally:
        if conn:
            cursor.close()
            conn.close()
            print("Соединение с PostgreSQL закрыто")
