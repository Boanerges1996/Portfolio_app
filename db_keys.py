import os


class Configuration:
    def __init__(self):
        if os.environ.get("SERVER_DB_KEY")=="dortheaInc.":
            self.MYSQL_HOST = "remotemysql.com"
            self.MYSQL_USER = "ZiKOlPWNCS"
            self.MYSQL_PASSWORD = "beAvaSOcbC"
            self.MYSQL_DB = "ZiKOlPWNCS"
        else:
            self.MYSQL_HOST = "localhost"
            self.MYSQL_USER = "root"
            self.MYSQL_PASSWORD = os.environ.get("DB_PASS")
            self.MYSQL_DB = "portfolio_db"
