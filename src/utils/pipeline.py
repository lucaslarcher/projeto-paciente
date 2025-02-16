from src.models.paciente import Sintomas, DoencaPaciente, Paciente
from src.preprocessing.gen_ai_classifier import extrair_sintomas, extrair_doencas
from src.utils.functions import limpar_texto, carregar_doencas
from src.utils.database import inserir_paciente

def pipeline_processamento(chat: str) -> list[DoencaPaciente] | None:
    #Processa o chat para extrair sintomas e doenças relacionadas.
    try:
        chat_limpo = limpar_texto(chat)
        sintomas: Sintomas = extrair_sintomas(chat_limpo)
        if not sintomas:
            return None
        doencas: list[DoencaPaciente] = extrair_doencas(sintomas, carregar_doencas())
        if not doencas:
            return None

        return doencas
    except Exception as e:
        return None


def pipeline_entrada_chat(chat: str, id_chat: str, id_cliente: str) -> bool:
    try:
        doencas = pipeline_processamento(chat)
        if not doencas:
            return False
        paciente = Paciente(
            id=id_cliente,
            chats=[id_chat],
            doencas=doencas
        )
        inserir_paciente(paciente)
        return True
    except Exception as e:
        return False




