import pytest
from src.utils.pipeline import pipeline_processamento, pipeline_entrada_chat


@pytest.mark.parametrize("chat_input, expected_substring", [
    ("paciente: estou sentindo hiperidrose, suores noturnos e problemas de transpiração", "hiperidrose"),
    ("paciente: estou com febre e tosse", "febre"),
])
def test_pipeline_processamento(chat_input, expected_substring):
    resultado = pipeline_processamento(chat_input)

    assert isinstance(resultado, str), "O resultado não é uma string"
    assert expected_substring in resultado, f"O resultado esperado deveria conter '{expected_substring}'"


@pytest.mark.parametrize("chat_input, id_chat, id_cliente", [
    ("paciente: estou sentindo hiperidrose, suores noturnos e problemas de transpiração", "122", "333333"),
    ("paciente: tenho dores musculares", "999", "555555"),
])
def test_pipeline_entrada_chat(chat_input, id_chat, id_cliente):
    resultado = pipeline_entrada_chat(chat_input, id_chat, id_cliente)

    assert isinstance(resultado, dict), "O resultado não é um dicionário"
    assert "chat" in resultado and resultado["chat"] == chat_input, "O campo 'chat' não foi processado corretamente"
    assert "id_chat" in resultado and resultado["id_chat"] == id_chat, "O campo 'id_chat' não corresponde"
    assert "id_cliente" in resultado and resultado["id_cliente"] == id_cliente, "O campo 'id_cliente' não corresponde"
