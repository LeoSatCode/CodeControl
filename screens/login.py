from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel

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
        """Lógica para verificar usuário e senha"""
        user = self.input_user.text
        password = self.input_password.text
        
        # Cadeia de Decisão Única
        if user == "admin" and password == "admin":
            self.manager.current = 'admin'
            print("Logado como Admin")
            
        elif user == "review" and password == "review": # ELIF = Else If (Senão Se)
            self.manager.current = 'review'
            print("Logado como Revisão")
            
        else:
            
            print("Acesso negado: Usuário ou senha incorretos")