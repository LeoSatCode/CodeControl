from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField

class LoginScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Aqui depois vamos construir os widgets (botões, inputs)
        pass
    
    def try_login(self):
        """Lógica para verificar usuário e senha"""
        pass