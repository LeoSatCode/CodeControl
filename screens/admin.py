from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.scrollview import MDScrollView # <--- Novo
from kivymd.uix.list import MDList, TwoLineListItem # <--- Novo
from kivymd.uix.button import MDRaisedButton, MDFloatingActionButton # <--- Novo (O botão +)
from kivymd.uix.label import MDLabel
from kivymd.app import MDApp

class AdminScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # 1. Layout Principal
        layout = MDBoxLayout(orientation='vertical')
        self.add_widget(layout)
        
        # 2. Título
        header = MDLabel(
            text="Operadores", 
            halign="center", 
            theme_text_color="Primary",
            font_style="H5",
            size_hint_y=None, 
            height=50
        )
        layout.add_widget(header)
        
        # 3. A Área de Rolagem 
        scroll = MDScrollView()
        layout.add_widget(scroll)
        
        # 4. A Lista 
        self.list_operators = MDList()
        scroll.add_widget(self.list_operators)
        
        # 5. O Botão Flutuante (+)
        btn_novo = MDRaisedButton(
            text="Novo Operador (+)",
            pos_hint={"center_x": 0.5},
            on_release=self.go_to_add_operator
        )
        layout.add_widget(btn_novo)

    def go_to_add_operator(self, instance):
        self.manager.current = 'add_operator'

    
    def on_enter(self):
        """Este método roda AUTOMATICAMENTE toda vez que a tela abre"""
        self.load_data()

    def load_data(self):
        # 1. Limpa a lista anterior para não duplicar
        self.list_operators.clear_widgets()
        
        # 2. Busca os dados atualizados
        app = MDApp.get_running_app()
        operators = app.db.get_operators()
        
        for operator in operators:
            # operator[1] é o nome, operator[2] é o cargo
            item = TwoLineListItem(
                text=operator[1],
                secondary_text=operator[2]
            )
            self.list_operators.add_widget(item)
        
    
    def add_code_to_table(self):
        """Lógica ao bipar um código na tela de admin"""
        pass