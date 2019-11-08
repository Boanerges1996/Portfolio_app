from flask import Flask,request,make_response,session,jsonify
import os
from flask_mysqldb import MySQL
from db_connection import get_db,close_db
from passlib.hash import sha256_crypt
from functools import wraps
import jwt
from logging import error
from db_keys import Configuration
import db_queries


app = Flask(__name__)
app.config["SECRET_KEY"] = "BoanergesKwakuSamson"
mysql = MySQL(app)


# Setting the DB instance on this app
myKeys = Configuration()
app.config["MYSQL_HOST"] = myKeys.MYSQL_HOST
app.config["MYSQL_USER"] = myKeys.MYSQL_USER
app.config["MYSQL_PASSWORD"] = myKeys.MYSQL_PASSWORD
app.config["MYSQL_DB"] = myKeys.MYSQL_DB


def loggin_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        token = None
        if 'myToken' in request.headers:
            token = request.headers['myToken']
            
        if not token:
            return jsonify({
                "message":"login to access this route"
            }),401
        try:
            decode_token = jwt.decode(token,app.config['SECRET_KEY'])
            username = decode_token["user"]
            verify_token = db_queries.verify_token(username)
        except Exception as exc:
            print(exc)
            return jsonify({    
                "user-token":"invalid"
            }),401
        return f(*args,**kwargs)      
    return wrap 



# User registration endpoint
@app.route('/user_registration',methods=["POST"])
def sign_up():
    username = request.json["username"]
    email  = request.json["email"]
    password = sha256_crypt.encrypt(request.json["password"]) 
    api_data = jsonify(db_queries.sign_up(username,email,password))
    return api_data


@app.route('/sign_in',methods=['POST'])
def sign_in():
    username = request.json['username']
    password = request.json['password']
    api_data = jsonify(db_queries.sign_in(username,password))
    return api_data




@app.route('/images',methods=["PUT","GET"])
@loggin_required
def updateImage():
    if request.method=="PUT":
        token = request.headers["myToken"]
        decode_token = jwt.decode(token,app.config["SECRET_KEY"])
        imageUrl = request.json["URL"]
        username = decode_token["user"]
        user_id = db_queries.get_user_id(username)
        data = db_queries.updatingAvatar(imageUrl,user_id)
        return jsonify(data)
    elif request.method=="GET":
        token = request.headers["myToken"]
        decode_token = jwt.decode(token,app.config["SECRET_KEY"])
        username = decode_token["user"]
        user_id = db_queries.get_user_id(username)
        image = db_queries.getImageUrl(user_id)
        return jsonify(image)
    


# Personal information Endpoints
@app.route('/personal',methods=["POST","GET","DELETE","PUT"])
@loggin_required
def personal():
    if request.method=="POST":
        data = request.json
        token = request.headers["myToken"]
        decode_token = jwt.decode(token,app.config["SECRET_KEY"])
        firstname = request.json["firstname"]
        lastname = request.json["lastname"]
        othername = request.json["othernames"]
        age = request.json["age"]
        sex = request.json["sex"]
        marriage_status = request.json["status"]
        date_of_birth = request.json["date_of_birth"]
        username = decode_token["user"]
        user_id = db_queries.get_user_id(username)
        api_data = db_queries.personal_info(firstname,lastname,othername,age,sex,marriage_status,date_of_birth,user_id)
        api_data = {**api_data, **data,"user_id":user_id}
        return jsonify(api_data)
    
    elif request.method == "GET":
        token = request.headers["myToken"]
        decode_token = jwt.decode(token,app.config["SECRET_KEY"])
        username = decode_token["user"]
        api_data = db_queries.get_personal(username)
        return jsonify(api_data)

    elif request.method == "PUT":
        token = request.headers["myToken"]
        decode_token = jwt.decode(token,app.config["SECRET_KEY"])
        username = decode_token["user"]

        firstname = request.json["firstname"]
        lastname = request.json["lastname"]
        othername = request.json["othernames"]
        age = request.json["age"]
        sex = request.json["sex"]
        marriage_status = request.json["status"]
        date_of_birth = request.json["date_of_birth"]

        api_data = db_queries.personal_update(firstname,lastname,othername,age,sex,marriage_status,date_of_birth,username)
        return jsonify(api_data)

    elif request.method == "DELETE":
        token = request.headers["myToken"]
        decode_token = jwt.decode(token,app.config["SECRET_KEY"])
        username = decode_token["user"]
        api_data = db_queries.delete_personal(username)
        return jsonify(api_data)


@app.route('/occupation',methods=["POST","GET","DELETE","PUT"])
@loggin_required
def occupation():
    if request.method == "POST":
        token = request.headers["myToken"]
        decode_token = jwt.decode(token,app.config["SECRET_KEY"])
        username = decode_token["user"]

        occ_name = request.json["occ_name"]
        prev_occ = request.json["prev_occ"]
        comp_name = request.json["comp_name"]
        position = request.json["position"]

        api_data = db_queries.register_occ(occ_name,prev_occ,comp_name,position,username)
        return jsonify(api_data)

    elif request.method == "GET":
        token = request.headers["myToken"]
        decode_token = jwt.decode(token,app.config["SECRET_KEY"])
        username = decode_token["user"]
        api_data = db_queries.get_occ(username)
        return jsonify(api_data)

    elif request.method == "PUT":
        token = request.headers["myToken"]
        decode_token = jwt.decode(token,app.config["SECRET_KEY"])
        username = decode_token["user"]

        occ_name = request.json["occ_name"]
        prev_occ = request.json["prev_occ"]
        comp_name = request.json["comp_name"]
        position = request.json["position"]

        api_data = db_queries.update_occ(occ_name,prev_occ,comp_name,position,username)
        return jsonify(api_data)


    elif request.method == "DELETE":
        token = request.headers["myToken"]
        decode_token = jwt.decode(token,app.config["SECRET_KEY"])
        username = decode_token["user"]

        api_data = db_queries.delete_occ(username)
        return jsonify(api_data)


@app.route('/address',methods=["POST","GET","PUT","DELETE"])
def address():
    if request.method == "POST":
        token = request.headers["myToken"]
        decode_token = jwt.decode(token,app.config["SECRET_KEY"])
        username = decode_token["user"]

        home_add = request.json["home_add"]
        work_add = request.json["work_add"]
        postal_add = request.json["postal_add"]
        telephone = request.json["telephone"]

        api_data = db_queries.reg_address(home_add,work_add,postal_add,telephone,username)
        return jsonify(api_data)
    elif request.method == "GET":
        token = request.headers["myToken"]
        decode_token = jwt.decode(token,app.config["SECRET_KEY"])
        username = decode_token["user"]
        api_data = db_queries.get_add(username)
        return jsonify(api_data)

    elif request.method=="PUT":
        token = request.headers["myToken"]
        decode_token = jwt.decode(token,app.config["SECRET_KEY"])
        username = decode_token["user"]

        home_add = request.json["home_add"]
        work_add = request.json["work_add"]
        postal_add = request.json["postal_add"]
        telephone = request.json["telephone"]
        api_data = db_queries.update_add(home_add,work_add,postal_add,telephone,username)
        return jsonify(api_data)

    elif request.method == "DELETE":
        token = request.headers["myToken"]
        decode_token = jwt.decode(token,app.config["SECRET_KEY"])
        username = decode_token["user"]

        api_data = db_queries.delete_add(username)
        return jsonify(api_data)



@app.after_request
def _close_db(res):
    res.headers.add('Access-Control-Allow-Origin','*')
    res.headers.add('Access-Control-Allow-Methods','POST,GET,PUT,DELETE')
    res.headers.add('Access-Control-Allow-Headers', '*')
    close_db()
    return res

if __name__ == "__main__":
    app.run(debug=True)