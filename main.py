import sys
import os
from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.button import MDRectangleFlatButton
from database import Database
from screens.login import LoginScreen
from screens.admin import AdminScreen
from screens.review import ReviewScreen
from screens.add_operator import AddOperatorScreen
from screens.operator_menu import OperatorMenuScreen
from screens.scanning import ScanningScreen
from screens.history import HistoryScreen



def load_db_path(self):
    # Detecta o caminho da aplicação
    if getattr(sys, 'frozen', False):
        pasta_do_app = os.path.dirname(sys.executable)
    else:
        pasta_do_app = os.path.dirname(os.path.abspath(__file__))
        
    # Monta o caminho do config.txt
    caminho_config = os.path.join(pasta_do_app, "config.txt")
    
    # Tenta ler
    if os.path.exists(caminho_config):
        with open(caminho_config, "r") as f:
            path = f.read().strip()
            if path: return path
            
    return "lotes.db" # Padrão se não achar config

class CodeControlApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Dark"

        caminho_banco = load_db_path(self)
        print(f"🔌 Conectando no banco em: {caminho_banco}")
        
        # Inicializa o banco de dados ao abrir o app
        self.db = Database(caminho_banco)
        self.db.create_tables()
        
        # Verifica se existe um usuário admin, se não existir cria um padrão
        if not self.db.check_user("admin", "admin"):
            print("Banco vazio, criando usuário admin padrão...")
            # Níveis: 3=Admin, 2=Revisora
            self.db.add_user("admin", "Gerente", "admin0433", 3)
            self.db.add_user("analise", "Qualidade", "analise8042", 2)

        # Gerenciador de Telas
        sm = MDScreenManager()
        
        # Adiciona as telas ao gerenciador (dando um nome para cada uma)
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(AdminScreen(name='admin'))
        sm.add_widget(ReviewScreen(name='review'))
        sm.add_widget(AddOperatorScreen(name='add_operator'))
        sm.add_widget(OperatorMenuScreen(name='operator_menu'))
        sm.add_widget(ScanningScreen(name='scanning'))
        sm.add_widget(HistoryScreen(name='history'))    
        
        return sm

if __name__ == "__main__":
    CodeControlApp().run()