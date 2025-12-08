from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.app import MDApp # <--- Precisamos disso pra chamar o banco

class OperatorMenuScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.operator_id = None # <--- Importante: Vai receber o ID vindo da tela anterior
        self.operator_name = "" 
        
        layout = MDBoxLayout(orientation='vertical', padding=50, spacing=20)
        self.add_widget(layout)
        
        # Título
        self.label_titulo = MDLabel(text="Carregando...", halign="center", font_style="H4")
        layout.add_widget(self.label_titulo)
        
        # Input da OP
        self.input_op_number = MDTextField(
            hint_text="Digite o número da OP", 
            size_hint_x=None,
            width=400,
            pos_hint={"center_x": 0.5},
            font_size="32sp"
            # Removemos o on_text_validate, vamos pegar o texto direto no botão
        )
        layout.add_widget(self.input_op_number)
        
        # Botão Nova Tabela
        btn_nova_tabela = MDRaisedButton(
            text="Iniciar Nova Tabela", 
            pos_hint={"center_x": 0.5},
            on_release=self.create_table_logic # Mudamos o nome pra ficar mais claro
        )
        layout.add_widget(btn_nova_tabela)
        
        # Botão Voltar
        btn_voltar = MDRaisedButton(
            text="Voltar", 
            pos_hint={"center_x": 0.5},
            on_release=self.voltar
        )
        layout.add_widget(btn_voltar)

    def on_enter(self):
        # Atualiza o título e LIMPA o campo da OP anterior
        self.label_titulo.text = f"Gestão: {self.operator_name}"
        self.input_op_number.text = "" 

    def create_table_logic(self, instance):
        """A Mágica: Cria o lote no banco e prepara a próxima tela"""
        op_digitada = self.input_op_number.text
        
        if op_digitada:
            app = MDApp.get_running_app()
            
            # 1. Chama o banco para criar o lote
            # Passamos o ID do operador (que veio da tela anterior) e a OP digitada
            novo_id_lote = app.db.create_lote(self.operator_id, op_digitada)
            
            if novo_id_lote:
                print(f"Sucesso! Lote {novo_id_lote} criado. Vamos bipar!")
                
                # AQUI FUTURAMENTE VAMOS MUDAR DE TELA
                # self.manager.current = 'bip_screen'
            else:
                print("Erro ao criar lote no banco.")
        else:
            print("Erro: Digite o número da OP antes de iniciar.")

    def voltar(self, instance):
        self.manager.current = 'admin'