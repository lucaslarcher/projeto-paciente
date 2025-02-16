import pandas as pd
from src.utils.pipeline import pipeline_entrada_chat

def carregar_client_id_chat(id_chat):
    df_clientes = carregar_clientes()
    cliente = df_clientes[df_clientes['chat_message_id'] == id_chat]
    if not cliente.empty:
        return cliente.iloc[0]["client_id"]
    else:
        return None

def carregar_clientes(arquivo_csv = "../data/clients.csv"):
    df = pd.read_csv(arquivo_csv)
    return df

def carregar_chats(arquivo_csv = "../data/chat_history.csv"):
    df = pd.read_csv(arquivo_csv)
    return df

def carregar_client_conditions(arquivo_csv = "../data/client_conditions.csv"):
    df = pd.read_csv(arquivo_csv)
    return df


def processar_chat_menssagens(messages_df):
    # Ordenar por chat_channel_id e created_date_brt
    messages_df = messages_df.sort_values(by=['chat_channel_id', 'created_date_brt'])

    # Lista para armazenar os chats concatenados por chat_channel_id
    chats = []

    # Iterar por chat_channel_id único
    for channel_id, group in messages_df.groupby('chat_channel_id'):
        chat = ''

        # Iterar pelas mensagens de cada chat_channel_id
        for _, row in group.iterrows():
            if row['sender'] == 'user':
                chat += f'a: {row["message_text"]}\n'
            elif row['sender'] == 'client':
                chat += f'p: {row["message_text"]}\n'

        # Adicionar o chat completo à lista
        chats.append({'chat_channel_id': channel_id, 'chat': chat.strip()})

    # Criar DataFrame com os chats processados
    chats_df = pd.DataFrame(chats)

    return chats_df

def gerar_dados_iniciais():
    clientes = carregar_clientes()
    chats = processar_chat_menssagens(carregar_chats())
    condicoes = carregar_client_conditions()

    merged_df = pd.merge(clientes, condicoes, on='client_id', how='left')
    merged_df = pd.merge(merged_df, chats, left_on='chat_message_id', right_on='chat_channel_id', how='left')
    merged_df = merged_df.drop(columns='chat_channel_id')

    if 'client_id' in merged_df.columns and 'chat_message_id' in merged_df.columns and 'chat' in merged_df.columns:
        merged_df['pipeline_result'] = merged_df.apply(
            lambda row: pipeline_entrada_chat(row['chat'], row['chat_message_id'], str(row['client_id'])),
            axis=1
        )
    else:
        print("As colunas necessárias não estão presentes no DataFrame.")