from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton

class OperatorMenuScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.operator_id = None # Aqui vou guardar o ID do operador
        self.operator_name = "" 
        
        layout = MDBoxLayout(orientation='vertical', padding=50, spacing=20)
        self.add_widget(layout)
        
        # Título que vai mudar dinamicamente
        self.label_titulo = MDLabel(text="Carregando...", halign="center", font_style="H4")
        layout.add_widget(self.label_titulo)
        
        # Botão só pra voltar por enquanto
        btn_voltar = MDRaisedButton(
            text="Voltar", 
            pos_hint={"center_x": 0.5},
            on_release=self.voltar
        )
        layout.add_widget(btn_voltar)

    def on_enter(self):
        # Quando a tela abrir, atualiza o título com o nome do cara
        self.label_titulo.text = f"Gestão: {self.operator_name}"

    def voltar(self, instance):
        self.manager.current = 'admin'