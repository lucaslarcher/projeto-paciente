import pandas as pd

def carregar_clientes(arquivo_csv = "../data/clients.csv"):
    df = pd.read_csv(arquivo_csv)
    return df

def carregar_client_id_chat(id_chat):
    df_clientes = carregar_clientes()
    cliente = df_clientes[df_clientes['chat_message_id'] == id_chat]
    if not cliente.empty:
        return cliente.iloc[0]["client_id"]
    else:
        return None

def carregar_chats(arquivo_csv = "../data/chat_history.csv"):
    df = pd.read_csv(arquivo_csv)
    return df