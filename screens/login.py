from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.app import MDApp

class LoginScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Layout principal
        layout = MDBoxLayout(orientation='vertical', padding=50, spacing=20)
        self.add_widget(layout)
        
        # Widgets
        titulo = MDLabel(text ="Code Control", font_style="H3", halign="center")

        self.input_user = MDTextField(
            hint_text="Usuário",
            helper_text="Digite seu nome de usuário",
            helper_text_mode="on_focus",
            icon_right="account",
            size_hint_x=None,
            width=300,
            pos_hint={"center_x": 0.5}
        )

        self.input_password = MDTextField(
            hint_text="Senha",
            mode="rectangle",
            password=True,
            helper_text="Digite sua senha",
            helper_text_mode="on_focus",
            icon_right="eye-off",
            size_hint_x=None,
            width=300,
            pos_hint={"center_x": 0.5},
        )

        self.button_login = MDRaisedButton(
            text="Login",
            pos_hint={"center_x": 0.5},
            on_release=lambda x: self.try_login()
        )

        # Adiciona os widgets ao layout
        layout.add_widget(titulo)
        layout.add_widget(self.input_user)
        layout.add_widget(self.input_password)
        layout.add_widget(self.button_login)
        layout.add_widget(
            MDLabel(
                text="© 2025 Code Control by Leonardo Saturnino",
                halign="center",
                theme_text_color="Secondary"            
        )
        )
        
    def try_login(self):
        """Lógica REAL para verificar usuário e senha"""
        user_text = self.input_user.text
        password_text = self.input_password.text
        
        # Acessa o banco de dados principal
        app = MDApp.get_running_app()
        access_level = app.db.check_user(user_text, password_text)
        
        if access_level:
            # Se retornou um numero, o usuário existe! Agora vemos o nível:
            
            if access_level == 3: # Admin
                print(f"Bem-vindo Admin! Nível {access_level}")
                self.manager.current = 'admin'
                
            elif access_level == 2: # Revisora
                print(f"Bem-vinda Revisora! Nível {access_level}")
                self.manager.current = 'review'
                
            else:
                print("Este usuário não tem permissão de acesso ao sistema (Apenas Operador).")
                
        else:
            # Se retornou None
            print("Acesso negado: Usuário ou senha incorretos")