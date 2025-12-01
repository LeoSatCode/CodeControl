from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.button import MDRectangleFlatButton
from database import Database
from screens.login import LoginScreen
from screens.admin import AdminScreen
from screens.review import ReviewScreen

class CodeControlApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"  # Podemos mudar a cor depois
        self.theme_cls.theme_style = "Light"
        
        # Inicializa o banco de dados ao abrir o app
        self.db = Database()
        self.db.create_tables()

        # Gerenciador de Telas
        sm = MDScreenManager()
        
        # Adiciona as telas ao gerenciador (dando um nome para cada uma)
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(AdminScreen(name='admin'))
        sm.add_widget(ReviewScreen(name='review'))
        
        return sm

if __name__ == "__main__":
    CodeControlApp().run()