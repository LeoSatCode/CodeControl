from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.app import MDApp

class AddOperatorScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Layout
        layout = MDBoxLayout(orientation='vertical', padding=50, spacing=20)
        self.add_widget(layout)
        
        # Título
        layout.add_widget(MDLabel(text="Novo Operador", font_style="H5", halign="center"))
        
        # Inputs
        self.input_name = MDTextField(
            hint_text="Nome Completo", 
            pos_hint={"center_x": 0.5}
        )
        layout.add_widget(self.input_name)
        
        self.input_office = MDTextField(
            hint_text="Cargo", 
            text="Op. Maq. Costura", # Já vem preenchido pra agilizar
            pos_hint={"center_x": 0.5}
        )
        layout.add_widget(self.input_office)
        
        # Botões
        btn_save = MDRaisedButton(
            text="Salvar Cadastro", 
            pos_hint={"center_x": 0.5},
            on_release=self.save_data
        )
        layout.add_widget(btn_save)
        
        btn_cancel = MDRaisedButton(
            text="Cancelar", 
            md_bg_color="red",
            pos_hint={"center_x": 0.5},
            on_release=self.back_to_admin
        )
        layout.add_widget(btn_cancel)

    def save_data(self, instance):
        name = self.input_name.text
        office = self.input_office.text
        
        if name and office:
            # Chama o banco
            app = MDApp.get_running_app()
            app.db.add_operator(name, office)
            
            # Limpa e volta
            self.input_name.text = ""
            print(f"Operador {name} salvo!")
            self.manager.current = 'admin'
            
    def back_to_admin(self, instance):
        self.manager.current = 'admin'