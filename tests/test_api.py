import json
import pytest
import requests

BASE_URL = "http://127.0.0.1:8000"


@pytest.fixture
def paciente_id():
    return 123


@pytest.fixture
def chat_data():
    return {
        "chat": "paciente: dor de cabeça, febre, espirro",
        "id_chat": "12345",
        "id_cliente": "67890"
    }


def test_recuperando_paciente_id_api(paciente_id):
    url = f"{BASE_URL}/recuperar_paciente/{paciente_id}"
    response = requests.get(url)

    assert response.status_code == 200, f"Erro ao recuperar paciente. Status: {response.status_code}"
    assert "id" in response.json(), "Resposta da API não contém ID do paciente"


def test_processar_chat_api(chat_data):
    url = f"{BASE_URL}/processar_chat/"
    headers = {'Content-Type': 'application/json'}

    response = requests.post(url, data=json.dumps(chat_data), headers=headers)

    assert response.status_code == 200, f"Erro {response.status_code}: {response.text}"
    response_json = response.json()

    assert isinstance(response_json, dict), "A resposta da API deve ser um dicionário"
    assert "resultado" in response_json, "A resposta da API deve conter a chave 'resultado'"