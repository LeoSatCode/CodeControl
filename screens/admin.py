from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout

class AdminScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Area do Cadastrador
        layout = MDBoxLayout(orientation='vertical', padding=50, spacing=20) # Layout principal
        self.add_widget(layout)
        
        titulo = MDLabel(text ="Area do Cadastrador", font_style="H4", halign="center")
        botao_voltar = MDRaisedButton(text="Voltar", pos_hint={"center_x": 0.5})
        layout.add_widget(titulo)
        layout.add_widget(botao_voltar)
        
        # Botão para voltar à tela de login
        botao_voltar.bind(on_release=lambda x: setattr(self.manager, 'current', 'login'))
    
    def add_code_to_table(self):
        """Lógica ao bipar um código na tela de admin"""
        pass