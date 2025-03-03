import pytest
from src.preprocessing.gen_ai_classifier import extrair_doencas, extrair_sintomas
from src.utils.functions import limpar_texto, carregar_doencas
from src.models.paciente import Sintomas

@pytest.fixture
def string_chat():
    return "paciente: estou com dor no corpo e dor de cabeça. Meu estômago dói também."

@pytest.fixture
def sintomas_exemplo():
    return Sintomas(sintomas=["febre", "tosse", "fadiga", "dor de cabeça"])

def test_extrair_sintomas(string_chat):
    chat_limpo = limpar_texto(string_chat)
    sintomas = extrair_sintomas(chat_limpo)

    assert isinstance(sintomas, Sintomas)  # Verifica se retorna um objeto Sintomas
    assert isinstance(sintomas.sintomas, list)  # Verifica se sintomas.sintomas é uma lista
    assert len(sintomas.sintomas) > 0  # Garante que encontrou sintomas

def test_extrair_doencas(sintomas_exemplo):
    info_doencas = carregar_doencas()
    doencas = extrair_doencas(sintomas_exemplo, info_doencas)

    assert isinstance(doencas, list)  # Verifica se retorna uma lista
    assert len(doencas) > 0  # Garante que encontrou doenças relevantes
