import pytest
from src.utils.pipeline import pipeline_processamento, pipeline_entrada_chat
from src.models.paciente import DoencaPaciente

@pytest.mark.parametrize("chat_input", [
    "paciente: estou sentindo hiperidrose, suores noturnos e problemas de transpiração",
    "paciente: estou com febre e tosse",
])
def test_pipeline_processamento(chat_input):
    resultado = pipeline_processamento(chat_input)

    # Verificar se o resultado é uma lista
    assert isinstance(resultado, list), "O resultado não é uma lista"

    # Verificar se todos os elementos da lista são instâncias de DoencaPaciente
    assert all(isinstance(doenca, DoencaPaciente) for doenca in
               resultado), "Os elementos da lista não são instâncias de DoencaPaciente"

@pytest.mark.parametrize("chat_input, id_chat, id_cliente", [
    ("paciente: estou sentindo hiperidrose, suores noturnos e problemas de transpiração", "122", "333333"),
    ("paciente: tenho dores musculares", "999", "555555"),
])
def test_pipeline_entrada_chat(chat_input, id_chat, id_cliente):
    resultado = pipeline_entrada_chat(chat_input, id_chat, id_cliente)

    assert isinstance(resultado, bool), "O resultado não é um booleano"
    assert resultado is True, "O pipeline de entrada do chat deveria retornar True indicando sucesso"