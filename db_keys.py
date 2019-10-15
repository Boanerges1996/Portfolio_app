import os

class Configuration:
    def __init__(self):
        self.MYSQL_HOST = "localhost"
        self.MYSQL_USER = "root"
        self.MYSQL_PASSWORD = os.environ.get("DB_PASS")
        self.MYSQL_DB = "portfolio_db"