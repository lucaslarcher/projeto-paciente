import json
import os
from typing import Optional

import pandas as pd
from service.data_models import Paciente, Doencas, Doenca


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


def salvar_paciente_json(paciente: Paciente, arquivo: str = "../data/paciente.json"):

    # Verificar se o arquivo já existe
    if os.path.exists(arquivo):
        with open(arquivo, "r", encoding="utf-8") as f:
            pacientes = json.load(f)
    else:
        pacientes = {}

    # Se o paciente já existir, atualizar dados
    if paciente.id in pacientes:
        paciente_existente = pacientes[paciente.id]

        # Atualizar lista de chats sem duplicatas
        paciente_existente["chats"] = list(set(paciente_existente["chats"] + paciente.chats))

        # Atualizar doenças, garantindo que não haja duplicatas
        doencas_existentes = {d["cid"]: d for d in paciente_existente["doencas"]}
        for doenca in paciente.doencas.doencas:
            doencas_existentes[doenca.cid] = doenca.model_dump()

        paciente_existente["doencas"] = list(doencas_existentes.values())
    else:
        # Novo paciente
        pacientes[paciente.id] = {
            "chats": paciente.chats,
            "doencas": [doenca.model_dump() for doenca in paciente.doencas.doencas]
        }

    # Salvar o JSON atualizado
    with open(arquivo, "w", encoding="utf-8") as f:
        json.dump(pacientes, f, indent=4, ensure_ascii=False)

    print(f"Paciente {paciente.id} salvo/atualizado com sucesso no arquivo {arquivo}!")

def carregar_paciente_json(paciente_id: str, arquivo: str = "../data/paciente.json") -> Optional[Paciente]:
    if os.path.exists(arquivo):
        with open(arquivo, "r", encoding="utf-8") as f:
            pacientes = json.load(f)
            if paciente_id in pacientes:
                paciente_data = pacientes[paciente_id]
                return Paciente(
                    id=paciente_id,
                    chats=paciente_data["chats"],
                    doencas=Doencas(doencas=[Doenca(**d) for d in paciente_data["doencas"]])
                )
    print(f"Paciente {paciente_id} não encontrado no arquivo {arquivo}.")
    return None