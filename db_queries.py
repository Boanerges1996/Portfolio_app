from db_connection import get_db,close_db
from passlib.hash import sha256_crypt
import gc
from flask import jsonify,Flask
import jwt
from flask import current_app as app


def sign_up(username,email,password):
    cursor = get_db().cursor()
    query = '''
        INSERT INTO user_info (user_name,email,user_password) VALUES (%s,%s,%s)
    '''
    try:
        cursor.execute(query,(username,email,password,))
        get_db().commit()
        query_second = '''
            SELECT user_id,user_name,email,user_avatar FROM user_info WHERE user_name=%s
        '''
        cursor.execute(query_second,(username,))
        user_info = cursor.fetchall()[0]
        myToken = jwt.encode({"user":username},app.config["SECRET_KEY"])
        
        return {
            "id":user_info[0],
            "username":user_info[1],
            "email":user_info[2],
            "user_avatar":user_info[3],
            "token" :myToken.decode("UTF-8")
        }

    except Exception as error:
        print(error)
        return {
            "message":"Username or Email is already exist"
        }


def verify_username(username):
    cursor = get_db().cursor()
    query = '''
        SELECT * FROM user_info WHERE user_name=%s
    '''
    cursor.execute(query,(username,))
    data = cursor.fetchall()
    print(data)
    if data == tuple():
        return False
    return True


def sign_in(username,password):
    cursor = get_db().cursor()
    query = '''
        SELECT user_id,user_name,email,user_avatar,user_password FROM user_info WHERE user_name=%s
    '''
    value = verify_username(username)
    if value:
        cursor.execute(query,(username,))
        data = cursor.fetchall()[0]
        if sha256_crypt.verify(password,data[4]):
            mytoken = jwt.encode({"user":username},app.config["SECRET_KEY"])
            return {
                "user_id":data[0],
                "username":data[1],
                "email":data[2],
                "user_avatar":data[3],
                "token":mytoken.decode("UTF-8")
            }
        else:
            return {
                "message":"Invalid password"
            }
    else:
        return {
            "message":"You dont have an account"
        }
