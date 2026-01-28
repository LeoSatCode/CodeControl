import pandas as pd
import os
from datetime import datetime

def export_history_to_excel(operator_name, data_list):
    """
    Recebe uma lista de DICIONÁRIOS prontos (OP, Data, Código, Status).
    Gera o Excel direto.
    """
    try:
        # 1. Como a lista já vem pronta (dicionários), o Pandas entende direto!
        # Não precisamos mais daquele loop de conversão manual.
        df = pd.DataFrame(data_list)

        # 2. Define nome do arquivo
        data_hoje = datetime.now().strftime("%Y-%m-%d_%H-%M")
        nome_arquivo = f"Relatorio_{operator_name}_{data_hoje}.xlsx"
        
        # 3. Define pasta (Documents)
        pasta_destino = os.path.join(os.path.expanduser("~"), "Documents")
        
        if not os.path.exists(pasta_destino):
            os.makedirs(pasta_destino)
            
        caminho_completo = os.path.join(pasta_destino, nome_arquivo)

        # 4. Salva
        df.to_excel(caminho_completo, index=False)
        
        return True, caminho_completo

    except Exception as e:
        print(f"Erro ao exportar: {e}")
        return False, str(e)