import sqlite3

class Database:
    def __init__(self):
        self.db_name = "conterbag.db"
    
    def connect(self):
        """Cria conexão com o banco"""
        return sqlite3.connect(self.db_name)

    def create_tables(self):
        """Cria as tabelas se não existirem"""
        
        conn = self.connect()
        
        #Tabela de usuários
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                office TEXT NOT NULL ,
                password TEXT NOT NULL,
                acess_level INTEGER NOT NULL
            )
        ''')
        conn.commit()
        
        #Tabelas Lotes (50 códigos por lote)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS lotes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_user INTEGER NOT NULL,
                creation_date TEXT NOT NULL,
                status TEXT NOT NULL
            )
        ''')
        conn.commit()
        
        #Tabela de códigos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS codes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_lote INTEGER NOT NULL,
                code TEXT NOT NULL,
                read BOOLEAN NOT NULL DEFAULT 0
            )
        ''')
        conn.commit()
        conn.close()
        
    
    # Futuramente teremos métodos como:
    # def add_user(self, ...):
    # def check_code(self, ...):