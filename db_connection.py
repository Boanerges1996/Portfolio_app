from flask import current_app as app,g
import MySQLdb

def get_db()-> MySQLdb.Connection:
    if not hasattr(g, 'db'):
        db_connection = MySQLdb.connect(
            host = app.config["MYSQL_HOST"],
            user = app.config["MYSQL_USER"],
            passwd = app.config["MYSQL_PASSWORD"],
            db = app.config["MYSQL_DB"]
        )
        setattr(g, 'db',db_connection)
    db_connection = getattr(g, 'db',None)
    return db_connection

def close_db():
    db_connection = get_db()
    db_connection.close()
    setattr(g, 'db',None) 

