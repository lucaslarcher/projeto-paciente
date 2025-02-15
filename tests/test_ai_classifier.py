from src.preprocessing.gen_ai_classifier import extrair_doencas,extrair_sintomas
from src.utils.functions import limpar_texto,carregar_doencas
from src.models.paciente import Sintomas

def test_extrair_sintomas(chat):
    chat = limpar_texto(chat)
    sintomas = extrair_sintomas(chat)
    print(sintomas)

def teste_extrair_doencas(sintomas: Sintomas):
    info_doencas = carregar_doencas()
    doencas = extrair_doencas(sintomas,info_doencas)
    print(doencas)

string_chat = "paciente: estou sentindo hiperidrose, suores noturnos e problemas de transpiração"
sintomas_exemplo = Sintomas(sintomas=["febre", "tosse", "fadiga", "dor de cabeça"])

#test_extrair_sintomas(string_chat)
teste_extrair_doencas(sintomas_exemplo)