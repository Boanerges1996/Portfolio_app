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


def get_user_id(username):
    cursor = get_db().cursor()
    query = '''
        SELECT user_id FROM user_info WHERE user_name=%s
    '''
    cursor.execute(query,(username,))
    data = cursor.fetchall()[0]
    return data[0]



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



#Token verification for the rest of the routes
def verify_token(decoded_token):
    cursor = get_db().cursor()
    query = '''
        SELECT user_name FROM user_info WHERE user_name=%s
    '''
    cursor.execute(query,(decoded_token,))
    data = cursor.fetchall()
    if data == tuple():
        return None
    else:
        return True



def personal_info(firstname,lastname,othername,age,sex,status,date_of_birth,user_id):
    cursor = get_db().cursor()
    query = '''
        INSERT INTO personal_info (firstname,lastname,othername,age,sex,m_status,date_of_birth,user_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
    '''
    try:
        print((firstname,lastname,othername,age,sex,status,date_of_birth,user_id))
        cursor.execute(query,(firstname,lastname,othername,int(age),sex,status,date_of_birth,int(user_id),))
        get_db().commit()
        query_two = '''
            SELECT id FROM personal_info WHERE user_id=%s
        '''
        cursor.execute(query_two,(int(user_id),))
        data = cursor.fetchall()
        return {
            "personal_id":data[0][0]
        }
    except Exception as error:
        print(error)
        return {
            "message":"Errors in DB connection"
        }
    

def get_personal(username):
    user_id = get_user_id(username)
    cursor = get_db().cursor()
    query = '''
        SELECT 
            id,
            firstname,
            lastname,
            othername,
            age,
            sex
            ,m_status, 
            date_of_birth 
        FROM personal_info 
        WHERE user_id=%s
    '''
    try:
        cursor.execute(query,(user_id,))
        data = cursor.fetchall()[0]
        return {
            "id":data[0],
            "firstname":data[1],
            "lastname":data[2],
            "othername":data[3],
            "age":data[4],
            "sex":data[5],
            "marriage_status":data[6],
            "date_of_birth":data[7]
        }
    except Exception as err:
        print(err)
        return {
            "message":"Dont have a personal account yet"
        }


def personal_update(firstname,lastname,othername,age,sex,status,date_of_birth,username):
    user_id = get_user_id(username)
    cursor = get_db().cursor()
    query = '''
        UPDATE personal_info SET
            firstname=%s,
            lastname=%s,
            othername=%s,
            age=%s,
            sex=%s,
            m_status=%s,
            date_of_birth=%s
        WHERE user_id=%s
    '''
    try:
        cursor.execute(query,(firstname,lastname,othername,age,sex,status,date_of_birth,user_id,))
        get_db().commit()
        data = get_personal(username)
        return data

    except Exception as err:
        print(err)
        return {
            "message":"You have not registered any personal account yet"
        }


def delete_personal(username):
    user_id = get_user_id(username)
    cursor = get_db().cursor()
    query = '''
        DELETE FROM personal_info WHERE user_id=%s
    '''
    try:
        cursor.execute(query,(int(user_id),))
        get_db().commit()
        return {
            "message":"Account successfully deleted"
        }

    except Exception as err:
        print(err)
        return {
            "message":"No personal account found"
        }

 

# Occupation info
def register_occ(occ_name,prev_occ,comp_name,position,username):
    user_id = get_user_id(username)
    cursor = get_db().cursor()
    query = '''
        INSERT INTO occupation (occ_name,prev_occ,comp_name,position,user_id) VALUES(%s,%s,%s,%s,%s)
    '''
    try:
        cursor.execute(query,(occ_name,prev_occ,comp_name,position,int(user_id),))
        get_db().commit()
        return {
            "message":"Registration successfull"
        }
    except Exception as err:
        print(err)
        return {
            "message":"Error in DB connection"
        }


def get_occ(username):
    user_id = get_user_id(username)
    cursor = get_db().cursor()
    query = '''
        SELECT id,occ_name,prev_occ,comp_name,position FROM occupation WHERE user_id=%s 
    '''
    try:
        cursor.execute(query,(int(user_id),))
        data = cursor.fetchall()
        if data == tuple():
            return {
                "message":"User hasn't registered any ocuupation yet"
            }
        else:
            return {
                "id":data[0][0],
                "occ_name":data[0][1],
                "prev_occ":data[0][2],
                "comp_name":data[0][3],
                "position":data[0][4],
                "user_id":user_id
            }

    except Exception as err:
        print(err)
        return {
            "message":"Connection Error"
        }


def update_occ(occ_name,prev_occ,comp_name,position,username):
    user_id = get_user_id(username)
    cursor = get_db().cursor()
    query = '''
        UPDATE occupation SET
            occ_name=%s,
            prev_occ=%s,
            comp_name=%s,
            position=%s
        WHERE user_id=%s
    '''
    try:
        cursor.execute(query,(occ_name,prev_occ,comp_name,position,int(user_id),))
        get_db().commit()
        return {
            "message":"Successfully updated"
        }

    except Exception as err:
        print(err)
        return {
            "message":"User id doesnt exist"
        }

def delete_occ(username):
    user_id = get_user_id(username)
    cursor = get_db().cursor()
    query = '''
        DELETE FROM occupation WHERE user_id=%s
    '''
    try:
        cursor.execute(query,(int(user_id),))
        get_db().commit()
        return {
            "message":"Occupation info deleted successfully"
        }


    except Exception as err:
        print(err)
        return {
            "message":"No occupation info was found Or Database connection error"
        }


# Addresses and contacts
def reg_address(home_add,work_add,postal_add,telephone,username): 
    user_id = get_user_id(username)
    cursor = get_db().cursor()
    query = '''
        INSERT INTO addresses (home_address,work_address,postal_address,phone,user_id) VALUES (%s,%s,%s,%s,%s)
    '''
    try:
        cursor.execute(query,(home_add,work_add,postal_add,telephone,int(user_id),))
        get_db().commit()
        return {
            "message":"Registration successful"
        }
    except Exception as err:
        print(err)
        return {
            "message":"DB connection error"
        }


def get_add(username):
    user_id = get_user_id(username)
    cursor = get_db().cursor()
    query = '''
        SELECT id,home_address,work_address,postal_address,phone FROM addresses WHERE user_id=%s
    '''
    try:
        cursor.execute(query,(int(user_id),))
        data = cursor.fetchall()[0]
        return {
            "id":data[0],
            "home_add":data[1],
            "work_add":data[2],
            "postal_add":data[3],
            "phone":data[4],
            "user_id":user_id
        }
    except Exception as err:
        print(err)
        return {
            "message":"DB connection errors"
        }


def update_add(home_add,work_add,postal_add,telephone,username):
    user_id = get_user_id(username)
    cursor = get_db().cursor()
    query = '''
        UPDATE addresses SET
            home_address=%s,
            work_address=%s,
            postal_address=%s,
            phone=%s
        WHERE user_id=%s
    '''
    try:
        cursor.execute(query,(home_add,work_add,postal_add,telephone,int(user_id),))
        get_db().commit()
        return {
            "message":"Update of addresses successfull"
        }

    except Exception as err:
        print(err)
        return {
            "message":"Databse connection problem"
        }


def delete_add(username):
    user_id = get_user_id(username)
    cursor = get_db().cursor()
    query = '''
        DELETE FROM addresses WHERE user_id=%s
    '''
    try:
        cursor.execute(query,(int(user_id),))
        get_db().commit()
        return {
            "message":"Deletion successful"
        }
    except Exception as err:
        print(err)
        return {
            "message":"DB Connection Error"
        }