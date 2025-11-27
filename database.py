import sqlite3

class Database:
    def __init__(self):
        self.db_name = "conterbag.db"
    
    def connect(self):
        """Cria conexão com o banco"""
        pass

    def create_tables(self):
        """Cria as tabelas se não existirem"""
        pass
    
    # Futuramente teremos métodos como:
    # def add_user(self, ...):
    # def check_code(self, ...):