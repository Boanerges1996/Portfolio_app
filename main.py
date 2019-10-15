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
app.config["MYSQL_PASSWORD"] = "Boanergesrhobbie1996"
app.config["MYSQL_DB"] = myKeys.MYSQL_DB





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



if __name__ == "__main__":
    app.run(debug=True)