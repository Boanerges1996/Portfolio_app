import os


class Configuration:
    def __init__(self):
        self.MYSQL_HOST = "localhost"
        self.MYSQL_USER = "root"
        self.MYSQL_PASSWORD = os.environ.get("DB_PASS")
        self.MYSQL_DB = "portfolio_db"

        # self.MYSQL_HOST = "remotemysql.com"
        # self.MYSQL_USER = "XBMVALDM8I"
        # self.MYSQL_PASSWORD = "A67P1ISR1j"
        # self.MYSQL_DB = "XBMVALDM8I"