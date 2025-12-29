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
        # Tabela de códigos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS codes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_lote INTEGER NOT NULL,
                code TEXT NOT NULL UNIQUE,
                read BOOLEAN NOT NULL DEFAULT 0,
                qa_check BOOLEAN NOT NULL DEFAULT 0
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
        """Tenta salvar um código. Retorna False se o código já existir em QUALQUER lote."""
        conn = self.connect()
        cursor = conn.cursor()
        try:
            # Agora verificamos na tabela inteira se esse código já foi cadastrado
            cursor.execute('SELECT id FROM codes WHERE code = ?', (code,))
            
            if cursor.fetchone():
                print(f"Tentativa de duplicidade global: Código {code} já existe no sistema.")
                return False  # Código já existe (em algum lugar)

            cursor.execute('''
                    INSERT INTO codes (id_lote, code, read, qa_check)
                    VALUES (?, ?, ?, ?)
                ''', (id_lote, code, 1, 0))
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

    # Buscar dados de um lote
    def get_lote_details(self, op_number):
        conn = self.connect()
        cursor = conn.cursor()

        try:
            # Consulta unificada para pegar códigos e dados do lote pela OP
            
            cursor.execute('''
                SELECT c.code, c.read, c.qa_check, l.status, l.creation_date, l.id
                FROM codes c
                JOIN lotes l ON c.id_lote = l.id
                WHERE l.op_number = ?
            ''', (op_number,))
            
            resultados = cursor.fetchall()

            if resultados:
                # Monta a lista de códigos
                lista_codigos = []
                for linha in resultados:
                    lista_codigos.append((linha[0], linha[1], linha[2]))

                return {
                    "id": "Múltiplos", # Não usarei mais um ID único aqui
                    "status": resultados[0][3], # Status do primeiro lote encontrado
                    "data": resultados[0][4],   # Data do primeiro lote
                    "codes": lista_codigos 
                }
            
            return None 
            
        except Exception as e:
            print(f"Erro ao buscar OP unificada: {e}")
            return None
        finally:
            conn.close()
    
    # Método para "tickar" os códigos do lote como lidos
    def mark_code_checked(self, id_lote_ignorado, code):
        """Marca código como revisado usando apenas o código de barras (que é único)"""
        conn = self.connect()
        cursor = conn.cursor()
        try:
            # Atualiza direto pelo código, independente de qual lote/operador seja
            cursor.execute('''
                UPDATE codes 
                SET qa_check = 1 
                WHERE code = ?
            ''', (code,))
            
            if cursor.rowcount > 0:
                conn.commit()
                return True
            return False
            
        except Exception as e:
            print(f"Erro ao checar código: {e}")
            return False
        finally:
            conn.close()
        
    
 