from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField

class ReviewScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # 1. Criar o Layout Principal
        layout = MDBoxLayout(orientation='vertical', padding=50, spacing=20) 
        self.add_widget(layout)
        
        # 2. Criar TODOS os Widgets primeiro
        titulo = MDLabel(text="Area de Revisão", font_style="H4", halign="center")
        
        self.input_code = MDTextField(
            hint_text="Bipe o código da bag aqui",
            size_hint_x=None,
            width=400,
            pos_hint={"center_x": 0.5},
            font_size="32sp"
        )
        
        botao_voltar = MDRaisedButton(text="Voltar", pos_hint={"center_x": 0.5})
        
        # 3. Adicionar ao Layout na ordem visual desejada
        layout.add_widget(titulo)         # Topo
        layout.add_widget(self.input_code) # Meio (agora ele existe!)
        layout.add_widget(botao_voltar)    # Baixo
        
        # 4. Configurar ações dos botões
        botao_voltar.bind(on_release=lambda x: setattr(self.manager, 'current', 'login'))

    def check_bag(self):
        """Lógica ao bipar um código na tela de revisão"""
        pass