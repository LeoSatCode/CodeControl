from datetime import datetime
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
                access_level INTEGER NOT NULL
            )
        ''')
        conn.commit()
        
        #Tabelas Lotes (50 códigos por lote)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS lotes (
                op_number TEXT NOT NULL,
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
        
        #Tabela de Operadores (Costura da Alça)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS operators (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                office TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()
        
    
    
    def add_user(self, name, office, password, access_level):
        """Adiciona um novo funcionário ao banco"""
        conn = self.connect()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO users (name, office, password, access_level)
                VALUES (?, ?, ?, ?)
            ''', (name, office, password, access_level))
            conn.commit()
            print("Usuário cadastrado com sucesso")
        except Exception as e:
            print(f"Erro ao cadastrar: {e}")
            
        finally:
            conn.close()
            
    def add_operator(self, name, office):
        """Adiciona um novo operador ao banco"""
        conn = self.connect()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO operators (name, office)
                VALUES (?, ?)
            ''', (name, office))
            conn.commit()
            print("Operador cadastrado com sucesso")
        except Exception as e:
            print(f"Erro ao cadastrar operador: {e}")
        finally:
            conn.close()
            
    def add_code(self, id_lote, code):
        """Tenta salvar um código. Retorna True se conseguir, False se já existir"""
        conn = self.connect()
        cursor = conn.cursor()
        try:
            cursor.execute('SELECT id FROM codes WHERE code = ? AND id_lote = ?', (code, id_lote))
            if data := cursor.fetchone():
                return False  # Código já existe
            cursor.execute('''
                    INSERT INTO codes (id_lote, code, read)
                    VALUES (?, ?, ?)
                ''', (id_lote, code, 1))
            conn.commit()
            return True

        except Exception as e:
            print(f"Erro ao adicionar código: {e}")
            return False
        finally:
            conn.close()
        
    def check_user(self, name, password):
        """Verifica se o usuário existem"""
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT access_level FROM users
            WHERE name = ? AND password = ?
        ''', (name, password))
        user = cursor.fetchone()
        conn.close()
        return user[0] if user else None
    
    def get_operators(self):
        """Retorna a lista de operadores cadastrados"""
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM operators')
        operators = cursor.fetchall()
        conn.close()
        return operators
    
    def create_lote(self, operator_id, op_number):
        """Cria um novo lote/tabela e retorna o ID dele"""
        conn = self.connect()
        cursor = conn.cursor()
        
        # 1. Gera os dados automáticos aqui dentro
        data_atual = datetime.now().strftime("%d/%m/%Y %H:%M")
        status_inicial = "Aberto"
        
        try:
            # 2. Insere os dados no banco
            cursor.execute('''
                INSERT INTO lotes (op_number, id_user, creation_date, status)
                VALUES (?, ?, ?, ?)
            ''', (op_number, operator_id, data_atual, status_inicial))
            
            conn.commit()
            
            # 3. Pega o ID e RETORNA ele
            novo_id = cursor.lastrowid
            print(f"Lote {novo_id} criado para a OP {op_number}")
            return novo_id
            
        except Exception as e:
            print(f"Erro ao criar lote: {e}")
            return None
        finally:
            conn.close()
            
    # Metodo para fechar um lote
    def close_lote(self, id_lote):
        conn = self.connect()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                UPDATE lotes
                SET status = ?
                WHERE id = ?
            ''', ("Concluído", id_lote))
            conn.commit()
        except Exception as e:
            print(f"Erro ao fechar lote: {e}")
        finally:
            conn.close()