from service.data_models import Sintomas, Doencas
from model.gen_ai_classifier import extrair_sintomas, extrair_doencas
from service.functions import limpar_texto, carregar_doencas

def pipeline_dos_dados(chat):
    chat_limpo = limpar_texto(chat)
    sintomas: Sintomas = extrair_sintomas(chat_limpo)
    doencas: Doencas = extrair_doencas(sintomas, carregar_doencas())
    return doencas
