from kivy.clock import Clock 
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.scrollview import MDScrollView
# Mudamos o tipo de lista para aceitar ícones na direita
from kivymd.uix.list import MDList, OneLineAvatarIconListItem, IconRightWidget

class ReviewScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.lote_atual_id = None 
        
        # Layout Principal
        layout = MDBoxLayout(orientation='vertical', padding=20, spacing=10) 
        self.add_widget(layout)
        
        # Título
        titulo = MDLabel(
            text="Area de Revisão", 
            font_style="H5", 
            halign="center",
            size_hint_y=None, 
            height=50
        )
        
        # Input
        self.input_code = MDTextField(
            hint_text="Bipe a OP aqui (Enter para buscar)",
            size_hint_x=0.9,
            pos_hint={"center_x": 0.5},
            multiline=False
        )
        self.input_code.bind(on_text_validate=self.check_bag)

        # Label Status
        self.lbl_info = MDLabel(
            text="Aguardando busca...",
            halign="center",
            theme_text_color="Secondary",
            size_hint_y=None,
            height=30
        )

        # Lista
        scroll = MDScrollView()
        self.lista_codigos = MDList()
        scroll.add_widget(self.lista_codigos)
        
        # Botão Voltar
        botao_voltar = MDRaisedButton(
            text="Voltar", 
            pos_hint={"center_x": 0.5},
            size_hint_y=None, 
            height=50
        )
        botao_voltar.bind(on_release=self.limpar_e_sair)
        
        layout.add_widget(titulo)         
        layout.add_widget(self.input_code) 
        layout.add_widget(self.lbl_info)      
        layout.add_widget(scroll)             
        layout.add_widget(botao_voltar)

    def set_focus(self, dt):
        """Força o foco voltar para o input (usado pelo Clock)"""
        self.input_code.focus = True

    def check_bag(self, instance):
        texto_digitado = self.input_code.text.strip()
        
        if not texto_digitado:
            return

        app = MDApp.get_running_app()

        # --- MODO 1: BUSCAR OP ---
        if self.lote_atual_id is None:
            dados = app.db.get_lote_details(texto_digitado)
            
            if dados:
                self.lote_atual_id = dados['id']
                
                status = dados['status']
                total = len(dados['codes'])
                self.lbl_info.text = f"OP: {texto_digitado} | Status: {status} | Qtd: {total}"
                self.lbl_info.theme_text_color = "Primary"
                
                self.lista_codigos.clear_widgets()
                for item in dados['codes']:
                    codigo = item[0]
                    revisado = item[2]
                    
                    list_item = OneLineAvatarIconListItem(text=f"Código: {codigo}")
                    list_item.code_number = str(codigo)
                    
                    if revisado:
                        list_item.bg_color = (0, 1, 0, 0.2)
                        icon = IconRightWidget(icon="check-circle", theme_text_color="Custom", text_color=(0, 0.6, 0, 1))
                        list_item.add_widget(icon)
                        list_item.text += " ✅" # Marca textual para ajudar na contagem
                    
                    self.lista_codigos.add_widget(list_item)
                
                self.input_code.text = ""
                self.input_code.hint_text = "AGORA BIPE AS PEÇAS AQUI..." 
                Clock.schedule_once(self.set_focus, 0.1)
                
            else:
                self.lbl_info.text = "OP não encontrada!"
                self.lbl_info.theme_text_color = "Error"
                self.input_code.text = ""
                Clock.schedule_once(self.set_focus, 0.1)

        # --- MODO 2: CONFERIR PEÇA ---
        else:
            sucesso = app.db.mark_code_checked(self.lote_atual_id, texto_digitado)
            
            if sucesso:
                self.lbl_info.text = f"Peça {texto_digitado} revisada com sucesso!"
                self.lbl_info.theme_text_color = "Primary"
                
                # 1. ATUALIZA VISUALMENTE O ITEM ATUAL
                for widget in self.lista_codigos.children:
                    if hasattr(widget, 'code_number') and widget.code_number == texto_digitado:
                        widget.bg_color = (0, 1, 0, 0.2)
                        
                        # Adiciona ícone se não tiver
                        has_icon = False
                        for child in widget.children:
                            if isinstance(child, IconRightWidget):
                                has_icon = True
                                break
                        
                        if not has_icon:
                            icon = IconRightWidget(icon="check-circle", theme_text_color="Custom", text_color=(0, 0.6, 0, 1))
                            widget.add_widget(icon)
                        
                        # Adiciona marca textual se não tiver 
                        if "✅" not in widget.text:
                            widget.text += " ✅"

                # 2. CONTAGEM E FECHAMENTO AUTOMÁTICO 
                total_itens = len(self.lista_codigos.children)
                itens_prontos = 0
                
                for widget in self.lista_codigos.children:
                    # Conta quantos têm a marca de revisado
                    if "✅" in widget.text:
                        itens_prontos += 1
                
                # Verifica se acabou
                if itens_prontos == total_itens:
                    app.db.close_lote(self.lote_atual_id)
                    
                    self.lbl_info.text = f"LOTE CONCLUÍDO COM SUCESSO! ({itens_prontos}/{total_itens})"
                    self.lbl_info.theme_text_color = "Custom"
                    self.lbl_info.text_color = (0, 0.7, 0, 1) # Verde Vitória
                
                self.input_code.text = ""
                Clock.schedule_once(self.set_focus, 0.1)
                
            else:
                self.lbl_info.text = f"Erro: Código {texto_digitado} inválido ou de outra OP!"
                self.lbl_info.theme_text_color = "Error"
                self.input_code.text = ""
                Clock.schedule_once(self.set_focus, 0.1)

    def limpar_e_sair(self, instance):
        self.lote_atual_id = None
        self.input_code.text = ""
        self.input_code.hint_text = "Bipe a OP aqui (Enter para buscar)"
        self.lista_codigos.clear_widgets()
        self.lbl_info.text = "Aguardando busca..."
        self.lbl_info.theme_text_color = "Secondary"
        if hasattr(self.manager, 'current'):
            self.manager.current = 'login'