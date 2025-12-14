from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.list import MDList, OneLineListItem
from kivymd.uix.scrollview import MDScrollView
from kivymd.app import MDApp
from kivy.clock import Clock
from kivymd.app import MDApp # Para acessar o banco de dados
from kivymd.toast import toast # Para mensagens rápidas na tela

class ScanningScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Variáveis que receberão dados da tela anterior
        self.lote_id = None
        self.op_number = ""
        self.counter = 0
        self.max_codes = 50
        
        # Layout Principal
        layout = MDBoxLayout(orientation='vertical', padding=20, spacing=10)
        self.add_widget(layout)
        
        # --- 1. O HUD (Topo) ---
        self.label_info = MDLabel(
            text="Carregando...", 
            halign="center", 
            font_style="H5",
            size_hint_y=None, height=50
        )
        layout.add_widget(self.label_info)
        
        self.label_counter = MDLabel(
            text="0 / 50", 
            halign="center", 
            font_style="H2", # Bem grande
            theme_text_color="Custom",
            text_color=(0, 0, 1, 1), # Azul
            size_hint_y=None, height=80
        )
        layout.add_widget(self.label_counter)
        
        # --- 2. A Lista de Códigos (Meio) ---
        scroll = MDScrollView()
        self.list_codes = MDList()
        scroll.add_widget(self.list_codes)
        layout.add_widget(scroll)
        
        # --- 3. Área de Bipagem (Rodapé) ---
        self.input_scanner = MDTextField(
            hint_text="Aguardando Bipe...",
            mode="fill",
            font_size="24sp",
            multiline=False, # Importante: Scanner dá Enter, não queremos pular linha
            on_text_validate=self.process_code # Chama a função quando der Enter
        )
        layout.add_widget(self.input_scanner)
        
        # Botão Finalizar
        self.btn_finish = MDRaisedButton(
            text="Finalizar Tabela",
            pos_hint={"center_x": 0.5},
            disabled=True, # Começa travado até bipar algo
            on_release=self.finish_table
        )
        layout.add_widget(self.btn_finish)

    def on_enter(self):
        """Prepara a tela quando ela abre"""
        # Atualiza o HUD
        self.label_info.text = f"OP: {self.op_number} | Lote ID: {self.lote_id}"
        self.counter = 0
        self.update_counter_visual()
        self.list_codes.clear_widgets()
        
        # Foca no input automaticamente após meio segundo (truque do Kivy)
        Clock.schedule_once(self.refocus_input, 0.5)

    def refocus_input(self, dt):
        """Força o foco no campo de texto"""
        self.input_scanner.focus = True

    def update_counter_visual(self):
        self.label_counter.text = f"{self.counter} / {self.max_codes}"
        
        # Habilita o botão de finalizar se tiver pelo menos 1 código
        if self.counter > 0:
            self.btn_finish.disabled = False

    def process_code(self, instance):
        """Lógica ao receber um ENTER do leitor"""
        code = self.input_scanner.text.strip()
        
        # Se estiver vazio, só foca de volta
        if not code:
            self.refocus_input(None)
            return

        # 1. Trava de Quantidade
        if self.counter >= self.max_codes:
            toast("Limite de 50 atingido! Finalize a tabela.")
            self.input_scanner.text = ""
            return

        # 2. CHAMA O BANCO
        app = MDApp.get_running_app()
        salvou = app.db.add_code(self.lote_id, code)

        if salvou:
            # SUCESSO: Adiciona na Lista Visual
            display_text = f"#{self.counter + 1} | ...{code[-6:]}" 
            item = OneLineListItem(text=display_text)
            self.list_codes.add_widget(item, index=0)
            
            # Atualiza contadores
            self.counter += 1
            self.update_counter_visual()
            
            # Feedback sonoro ou visual sutil (Toast opcional)
            # toast("Bipado!") 
            
        else:
            # ERRO: Código Duplicado
            toast(f"ERRO: Código ...{code[-6:]} JÁ FOI LIDO!")
            # Futuramente adicionarei som de erro aqui
        
        # 3. Limpa e Foca de novo (Sempre, dando certo ou errado)
        self.input_scanner.text = ""
        Clock.schedule_once(self.refocus_input, 0.1)

    def finish_table(self, instance):
        # Chamar a função do banco antes de mudar de tela
        app = MDApp.get_running_app()
        app.db.close_lote(self.lote_id)
        
        # Muda de tela
        toast(f"Tabela finalizada com {self.counter} códigos.")
        self.manager.current = 'admin' # Volta pro início