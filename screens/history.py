from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.list import MDList, ThreeLineListItem, OneLineAvatarIconListItem, IconRightWidget
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.toast import toast 
from utils.exporter import export_history_to_excel

class HistoryScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.operator_id = None
        self.operator_name = ""
        self.dialog = None

        # Layout Principal
        layout = MDBoxLayout(orientation='vertical', padding=20, spacing=10)
        
        # Título Dinâmico
        self.lbl_title = MDLabel(
            text="Histórico do Operador", 
            font_style="H5", 
            halign="center", 
            size_hint_y=None, height=50
        )
        
        # Lista com Scroll
        scroll = MDScrollView()
        self.lista_historico = MDList()
        scroll.add_widget(self.lista_historico)
        
        # Botão Voltar
        btn_voltar = MDRaisedButton(
            text="Voltar", pos_hint={"center_x": 0.5}
        )
        btn_voltar.bind(on_release=lambda x: setattr(self.manager, 'current', 'admin'))

        # Botão de Exportar
        from kivymd.uix.button import MDIconButton
        
        botoes_layout = MDBoxLayout(orientation='horizontal', size_hint_y=None, height=50, spacing=10, padding=[50, 0])
        
        btn_voltar = MDRaisedButton(
            text="Voltar", 
            pos_hint={"center_y": 0.5}
        )
        btn_voltar.bind(on_release=lambda x: setattr(self.manager, 'current', 'admin'))
        
        btn_exportar = MDRaisedButton(
            text="Exportar Excel",
            icon="file-excel",
            md_bg_color=(0, 0.7, 0, 1), # Verde Excel
            pos_hint={"center_y": 0.5}
        )
        btn_exportar.bind(on_release=self.fazer_exportacao)

        botoes_layout.add_widget(btn_voltar)
        botoes_layout.add_widget(btn_exportar)

        layout.add_widget(self.lbl_title)
        layout.add_widget(scroll)
        layout.add_widget(botoes_layout)
        self.add_widget(layout)

    def load_history(self, operator_id, operator_name):
        """Chamado pelo Admin ao entrar nessa tela"""
        self.operator_id = operator_id
        self.operator_name = operator_name
        self.lbl_title.text = f"Histórico: {operator_name}"
        self.lista_historico.clear_widgets()
        
        app = MDApp.get_running_app()
        lotes = app.db.get_lotes_by_operator(operator_id)
        
        if not lotes:
            self.lista_historico.add_widget(OneLineAvatarIconListItem(text="Nenhum lote encontrado."))
            return

        for lote in lotes:
            # lote = (id, op_number, date, status)
            lote_id, op, data, status = lote
            
            # Cria o item da lista
            item = ThreeLineListItem(
                text=f"OP: {op}",
                secondary_text=f"Data: {data}",
                tertiary_text=f"Status: {status}",
                on_release=lambda x, lid=lote_id, lop=op: self.show_lote_details(lid, lop)
            )
            # Pinta de verde se estiver concluído
            if status == "Concluído":
                item.bg_color = (0, 1, 0, 0.05)
                
            self.lista_historico.add_widget(item)

    def show_lote_details(self, lote_id, op_number):
        """Abre um Popup com os códigos daquele lote"""
        app = MDApp.get_running_app()
        codes = app.db.get_lote_codes_only(lote_id)
        
        # Monta o conteúdo do Dialog
        content = MDBoxLayout(orientation="vertical", size_hint_y=None, height=300)
        scroll = MDScrollView()
        list_view = MDList()
        
        total = len(codes)
        revisados = 0
        
        for c in codes:
            code_text = c[0]
            is_checked = c[2] 
            
            item_text = f"{code_text}"
            if is_checked:
                item_text += " [OK]"
                revisados += 1
                
            li = OneLineAvatarIconListItem(text=item_text)
            if is_checked:
                icon = IconRightWidget(icon="check-circle", theme_text_color="Custom", text_color=(0, 0.6, 0, 1))
                li.add_widget(icon)
            
            list_view.add_widget(li)
            
        scroll.add_widget(list_view)
        content.add_widget(scroll)
        
        self.dialog = MDDialog(
            title=f"Detalhes OP {op_number} ({revisados}/{total})",
            type="custom",
            content_cls=content,
            buttons=[MDFlatButton(text="FECHAR", on_release=lambda x: self.dialog.dismiss())]
        )
        self.dialog.open()

    def fazer_exportacao(self, instance):
        # Pega os dados atuais do banco
        app = MDApp.get_running_app()
        lotes = app.db.get_lotes_by_operator(self.operator_id)
        
        if not lotes:
            toast("Nada para exportar!")
            return
        
        dados_para_excel = [] # Super lista para o Excel

        # 1. Varre os lotes
        for lote in lotes:
            lote_id = lote[0]
            op_number = lote[1]
            data = lote[2]
            status_lote = lote[3]

            # 2. Busca os códigos SÓ desse lote
            codigos = app.db.get_lote_codes_only(lote_id)

            # 3. Varre os códigos
            for codigo in codigos:
                nome_codigo = codigo[0]
                status_revisao = "OK" if codigo[2] == 1 else "Pendente"

                linha = {
                    "OP": op_number,
                    "Data Criação": data,
                    "Status do Lote": status_lote,
                    "Código de Barras": nome_codigo,
                    "Revisado?": status_revisao
                }
                
               
                dados_para_excel.append(linha)

        
        sucesso, mensagem = export_history_to_excel(self.operator_name, dados_para_excel)
        
        if sucesso:
            toast(f"Sucesso! Salvo em: {mensagem}")
        else:
            toast(f"Erro: {mensagem}")