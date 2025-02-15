from src.models.paciente import Sintomas, DoencaPaciente, Paciente
from src.preprocessing.gen_ai_classifier import extrair_sintomas, extrair_doencas
from src.utils.functions import limpar_texto, carregar_doencas
from src.utils.database import inserir_paciente

def pipeline_processamento(chat):
    try:
        chat_limpo = limpar_texto(chat)
        sintomas: Sintomas = extrair_sintomas(chat_limpo)
        doencas: list[DoencaPaciente]  = extrair_doencas(sintomas, carregar_doencas())
        return doencas
    except:
        return None

def pipeline_entrada_chat(chat, id_chat, id_cliente):
    try:
        doencas: list[DoencaPaciente] = pipeline_processamento(chat)
        if not doencas:
            return  False
        paciente = Paciente(
            id=id_cliente,
            chats=[id_chat],
            doencas=doencas
        )
        inserir_paciente(paciente)
        return True
    except:
        return False
